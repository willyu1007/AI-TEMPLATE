# plan.md
- assignee: @bot
- reviewers: [@owner]
- code_paths.lock:
  - modules/example/
- breaking_change: false
- merge_order: after M_Assign_Select
- conflict_resolution:
  - 文件级优先级：agent.md > CONTRACT.md > 其他
  - 自动合并失败 → 人工评审
