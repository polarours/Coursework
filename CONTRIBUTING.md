# 贡献指南 / Contributing

## 新增一道题 / Adding a problem

1. 先按 [选题标准](docs/selection-criteria.md) 确认题目合格 / Check the [selection criteria](docs/selection-criteria.md) first.
2. 在 [路线图](docs/roadmap.md) 登记，避免重复劳动 / Register it in the [roadmap](docs/roadmap.md) to avoid duplicate work.
3. 复制 `templates/problem/` 到 `problems/NNN-课程-题目/`，按模板补全 / Copy the template to `problems/NNN-course-topic/` and fill it in.
4. 参考实现必须实际运行过，`05-调试与测试.md` 中贴真实输出 / Actually run the reference implementation and paste real output in `05`.
5. 所有文档按 [写作规范](docs/writing-guide.md) 写成中英对照 / Write all docs bilingually per the [writing guide](docs/writing-guide.md).
6. 逐项过一遍 [自检清单](docs/writing-guide.md#自检清单--checklist) / Go through the [checklist](docs/writing-guide.md#自检清单--checklist).

## 提交规范 / Commit convention

每次改动立即提交，提交信息用中英双语简述 / Commit every change immediately; use a short bilingual message:

```text
feat(001-raft): 补全 Raft 选举实现 / add Raft election implementation
docs(guide): 明确双语格式 / clarify bilingual format
fix(002-tcp): 修正接收窗口说明 / fix receive-window explanation
```

## 不要做 / Don't

- 不要复制课程官方题目原文或他人的 solution 仓库 / Don't copy official problem statements or other people's solution repos.
- 不要写没有真实运行支撑的结论或数字 / Don't write claims or numbers without real execution.
- 不要提交密钥、个人账号信息 / Don't commit credentials or personal account data.
