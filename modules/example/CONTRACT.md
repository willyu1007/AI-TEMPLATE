# CONTRACT - 接口契约

## 输入
```json
{
  "task": "string - 任务描述",
  "language": "string - 目标语言（可选）",
  "dry_run": "boolean - 是否为演练模式（默认: false）"
}
```

## 输出
```json
{
  "result": "string - 处理结果",
  "status": "success | error",
  "metadata": {
    "duration_ms": "number - 处理时长",
    "version": "string - 版本号"
  }
}
```

## 错误码
- `E001`: 参数验证失败
- `E002`: 处理超时
- `E003`: 内部错误

## 兼容策略
- 向后兼容：不删除现有字段，不改变字段类型
- 版本管理：semver (major.minor.patch)
- 破坏性变更：需创建新的 major 版本

## 示例
### 请求示例
```json
{
  "task": "实现用户登录功能",
  "language": "python",
  "dry_run": false
}
```

### 成功响应示例
```json
{
  "result": "登录功能实现完成",
  "status": "success",
  "metadata": {
    "duration_ms": 1250,
    "version": "1.0.0"
  }
}
```

### 错误响应示例
```json
{
  "result": "参数 task 不能为空",
  "status": "error",
  "error_code": "E001"
}
```
