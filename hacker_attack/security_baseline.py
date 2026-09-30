#!/usr/bin/env python3
"""Low-impact, authorized security baseline checks for a website you own.

This tool only makes a few ordinary HTTPS GET/HEAD requests.  It does not try
passwords, submit forms, enumerate content, exploit a vulnerability, or send
high-volume traffic.
"""

from __future__ import annotations

import argparse
import json
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


RECOMMENDED_HEADERS = {
    "strict-transport-security": "HSTS (HTTPS downgrade protection)",
    "content-security-policy": "CSP (XSS impact reduction)",
    "x-content-type-options": "MIME-sniffing protection",
    "referrer-policy": "referrer privacy control",
    "permissions-policy": "browser feature restrictions",
}


def request(url: str, method: str = "GET") -> tuple[int, dict[str, str]]:
    req = urllib.request.Request(
        url,
        method=method,
        headers={"User-Agent": "AuthorizedSecurityBaseline/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            return response.status, dict(response.headers.items())
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers.items())


def check_tls(host: str) -> str:
    context = ssl.create_default_context()
    # A failed handshake is reported rather than bypassed; certificate checks
    # must stay enabled for a meaningful baseline test.
    try:
        import socket
        with socket.create_connection((host, 443), timeout=12) as sock:
            with context.wrap_socket(sock, server_hostname=host) as tls_sock:
                return tls_sock.version() or "unknown TLS version"
    except OSError as exc:
        return f"unavailable ({exc})"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="HTTPS URL for a site you are authorized to test")
    parser.add_argument(
        "--authorized",
        action="store_true",
        help="confirm you own the target or have explicit permission to test it",
    )
    args = parser.parse_args()

    if not args.authorized:
        parser.error("refusing to run without --authorized")

    parsed = urllib.parse.urlparse(args.url)
    if parsed.scheme != "https" or not parsed.hostname:
        parser.error("only a complete https:// URL is accepted")
    base_url = urllib.parse.urlunparse(("https", parsed.netloc, "/", "", "", ""))

    report: dict[str, object] = {"target": base_url, "checks": []}
    print(f"Target: {base_url}")
    print("Mode: low-impact baseline checks only\n")

    tls = check_tls(parsed.hostname)
    print(f"TLS: {tls}")
    report["tls"] = tls

    try:
        status, headers = request(base_url, "HEAD")
    except urllib.error.URLError:
        # Some sites intentionally reject HEAD; a single GET is the safe fallback.
        try:
            status, headers = request(base_url)
        except urllib.error.URLError as exc:
            print(f"ERROR: target could not be reached: {exc.reason}")
            return 2

    normalized = {key.lower(): value for key, value in headers.items()}
    print(f"HTTP status: {status}")
    for header, description in RECOMMENDED_HEADERS.items():
        value = normalized.get(header)
        outcome = "present" if value else "missing"
        print(f"[{outcome.upper():7}] {header}: {description}")
        report["checks"].append({"check": header, "status": outcome, "value": value})

    for cookie in headers.get("Set-Cookie", "").split("\n"):
        if not cookie:
            continue
        lower = cookie.lower()
        missing = [flag for flag in ("secure", "httponly", "samesite") if flag not in lower]
        print("[COOKIE ] " + ("flags present" if not missing else f"missing {', '.join(missing)}"))

    # These are conventional, explicitly public discovery files; no crawling.
    for path in ("/.well-known/security.txt", "/robots.txt", "/sitemap.xml"):
        time.sleep(0.5)
        try:
            file_status, _ = request(base_url.rstrip("/") + path)
            print(f"[PUBLIC ] {path}: HTTP {file_status}")
        except urllib.error.URLError as exc:
            print(f"[PUBLIC ] {path}: unavailable ({exc.reason})")

    with open("security-baseline-report.json", "w", encoding="utf-8") as output:
        json.dump(report, output, ensure_ascii=False, indent=2)
    print("\nWrote security-baseline-report.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
