# Safety & Quality Gates
- 默认禁止越权写入未声明路径
- 网络/工具调用受 `tools_allowed` 白名单限制
- 测试类型至少包含：unit/contract/e2e
- 变更需记录 `doc/CHANGELOG.md` 并走兼容性检查
