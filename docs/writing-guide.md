# 写作规范 / Writing guide

## 双语格式 / Bilingual format

每个小节先中文、后英文，英文用引用块紧跟中文段落 / Chinese first, English immediately after as a blockquote:

```markdown
## 设计思路 / Design rationale

中文正文……

> **English:** English body...
```

代码注释可只写中文，但关键术语首次出现须给出中英对照 / Code comments may be Chinese-only, but key terms need bilingual gloss on first use.

## 各章要求 / Per-chapter requirements

| 文件 / File | 必须包含 / Must contain |
|---|---|
| `01-题目解读.md` | 用自己的话复述需求、输入输出、边界条件、明确的不做事项 / Restated requirements, I/O, edge cases, explicit non-goals |
| `02-设计思路.md` | 架构图（文本或 Mermaid）、数据结构选型理由、备选方案对比 / Architecture diagram, rationale for data structures, alternatives considered |
| `03-逐步实现.md` | 分阶段，每阶段有可验证的中间产物 + 关键代码 / Stages, each with a verifiable artifact and key code |
| `04-正确性与复杂度.md` | 不变量/证明思路、时间空间复杂度 / Invariants or proof sketch, time and space complexity |
| `05-调试与测试.md` | **真实运行输出**、失败案例、排查过程 / **Real execution output**, failure cases, debugging process |
| `06-踩坑清单.md` | 常见错误、反直觉行为、症状→原因→修复 / Common mistakes, counterintuitive behavior, symptom → cause → fix |
| `07-延伸练习.md` | 至少 2 道自出题，难度递增，附提示 / At least 2 original exercises of increasing difficulty, with hints |

## 实测纪律 / Evidence discipline

- 任何性能数字、测试结果必须来自真实运行，标明环境（语言版本、OS、硬件）/ Every number must come from a real run; state the environment.
- 写不出真实输出时，明确标注 TODO，不得编造 / If you cannot produce real output, mark TODO — never fabricate.
- 参考实现必须能独立编译/运行 / Reference implementations must build and run standalone.

## 自检清单 / Checklist

- [ ] 来源与许可已注明 / Source and license attributed
- [ ] 中英对照完整 / Bilingual throughout
- [ ] 先做后读的阅读引导存在 / "try first" guidance present
- [ ] 设计思路解释了「为什么」/ Rationale explains *why*
- [ ] 测试输出为真实运行 / Test output is from a real run
- [ ] 踩坑清单至少 3 条 / At least 3 pitfalls
- [ ] 延伸练习至少 2 道 / At least 2 original exercises
- [ ] 目录与模板一致 / Layout matches the template
