| 银行 | 学生低资产持有 | 大陆→香港 | 国际支付 | 开户便利 | 对你的定位 |
|---|---|---|---|---|---|
| 中银香港 | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★★★（可尝试手机开户） | 主账户候选 |
| 恒生 | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★★☆ | 主账户候选 |
| 工银亚洲 | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★☆☆ | 跨境备用 |
| 建银亚洲 | ★★★★★ | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | 备用 |
| 汇丰香港 | 视账户/客户条件 | ★★★★☆ | ★★★★★ | ★★★★☆ | 国际化 |
| ZA Bank | ★★★★★ | ★★★☆☆ | ★★★☆☆ | ★★★★☆ | 数字备用 |


- [x] 
- [ ] the 
* [ ] A
+ [ ] B 

```mermaid
gitGraph
    commit id:"init"
    branch master
    checkout master
    branch develop
    checkout develop
    branch feature/nbi-model
    checkout feature/nbi-model
    commit id: "开发模型"
    checkout develop
    merge feature/nbi-model
    branch pre/v1.0
    checkout pre/v1.0
    commit id:"预发布修复bug"
    checkout master
    merge pre/v1.0 tag:"v1.0"
    checkout develop
    merge pre/v1.0
    checkout master
    branch hotfix/fix-bug
    checkout hotfix/fix-bug
    commit id:"线上紧急修复"
    checkout master
    merge hotfix/fix-bug tag:"v1.0.1"
    checkout develop
    merge hotfix/fix-bug
```

