# Authorized website security testing

`security_baseline.py` is deliberately low-impact. It verifies HTTPS, common
security response headers, cookie flags, and the availability of a few public
discovery files. It does not attack endpoints or authentication.

Run it only against a domain you own or have explicit permission to test:

```powershell
python .\security_baseline.py https://janus-qirui-xu.janus-personal-site.workers.dev/ --authorized
```

The script writes `security-baseline-report.json` (ignored by Git, if desired)
and prints findings. A missing header is a review item, not proof of a
vulnerability. Fixes should be assessed against the site's actual routes,
embedded content, and authentication model.

For a deeper assessment, use a staging environment and an authenticated test
account with no production data. Keep testing rate-limited and avoid password
guessing, destructive payloads, or denial-of-service checks.
