# RUNBOOK - 运维手册

## 启动
```bash
# 开发环境
export APP_ENV=dev
python -m example.main

# 使用 docker-compose
docker-compose up
```

## 配置
- 配置文件：`config/dev.yaml` / `config/staging.yaml` / `config/prod.yaml`
- 环境变量：
  - `APP_ENV`: 运行环境（必需）
  - `DATABASE_URL`: 数据库连接（生产必需）

## 调试
### 日志位置
- 开发环境：stdout
- 生产环境：`/var/log/app/example.log`

### 日志级别
```bash
# 临时提高日志级别
export LOG_LEVEL=DEBUG
```

### 常见问题排查
1. **连接数据库失败**
   - 检查 `DATABASE_URL` 配置
   - 验证网络连接：`telnet db-host 5432`
   - 查看数据库日志

2. **性能问题**
   - 检查慢查询：查看 `docs/db/DB_SPEC.yaml` 中的索引配置
   - 监控资源使用：CPU、内存、磁盘 I/O
   - 检查缓存命中率

### 调试工具
- `make dev_check`: 运行所有检查
- `pytest tests/example/ -v`: 详细测试输出
- `python -m pdb`: Python 调试器

## 告警
| 告警名称 | 触发条件 | 严重级别 | 处理步骤 |
|---------|---------|---------|---------|
| HighLatency | P95 延迟 > 2000ms | Warning | 1. 检查数据库连接<br>2. 查看慢日志<br>3. 考虑扩容 |
| ErrorRate | 错误率 > 5% | Critical | 1. 查看错误日志<br>2. 检查依赖服务<br>3. 考虑回滚 |
| DatabaseDown | 数据库不可用 | Critical | 1. 联系 DBA<br>2. 切换到只读模式<br>3. 通知用户 |

## 回滚
```bash
# 1. 代码回滚
git checkout <previous-tag>
git push -f origin main  # 谨慎使用

# 2. 数据库回滚
psql -d app -f migrations/XXX_down.sql

# 3. 重启服务
systemctl restart app-example

# 4. 验证
curl http://localhost:8000/health
```

## 监控指标
### 关键指标
- **吞吐量**: 请求数/秒
- **延迟**: P50, P95, P99 响应时间
- **错误率**: 5xx 错误占比
- **可用性**: Uptime %

### 业务指标
- 任务处理成功率
- 平均处理时长
- 并发任务数

### 仪表板
- Grafana: http://grafana.example.com/dashboard/example
- 日志：http://kibana.example.com/app/discover

## 备份与恢复
### 数据备份
```bash
# 数据库备份（每日自动）
pg_dump app > backup_$(date +%Y%m%d).sql

# 手动备份
make backup
```

### 恢复
```bash
# 从备份恢复
psql app < backup_YYYYMMDD.sql
```

## 安全
- API 密钥轮换周期：90 天
- 访问日志保留期：180 天
- 敏感数据加密：所有 PII 字段

## 扩容
### 水平扩容
```bash
# 增加实例数
docker-compose up --scale example=3
```

### 垂直扩容
- 调整 `docker-compose.yml` 中的资源限制
- 修改 `config/prod.yaml` 中的并发配置
