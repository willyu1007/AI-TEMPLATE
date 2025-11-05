# 运维手册（Runbook）

## 目标
提供模块的完整运维指南，包括部署、监控、故障排查和回滚操作。

## 适用场景
- 服务部署和启动
- 日常运维和监控
- 故障诊断和处理
- 紧急回滚操作

## 前置条件
- 已阅读 `README.md` 了解模块架构
- 已配置环境变量和配置文件
- 具备相应环境的访问权限

---

## 服务管理

### 1. 启动服务

#### 开发环境
```bash
# 方法 1：直接运行
export APP_ENV=dev
export LOG_LEVEL=DEBUG
python -m example.main

# 方法 2：使用 docker-compose
docker-compose up example

# 方法 3：后台运行
docker-compose up -d example
```

#### 生产环境
```bash
# 1. 切换到生产配置
export APP_ENV=prod

# 2. 启动服务
systemctl start app-example

# 3. 验证启动
systemctl status app-example
curl http://localhost:8000/health
```

**验证步骤**:
- [ ] 进程正常运行
- [ ] 健康检查接口返回 200
- [ ] 日志无错误信息
- [ ] 监控指标正常

---

### 2. 停止服务

```bash
# 优雅停止（等待处理完当前请求）
docker-compose stop example

# 立即停止
docker-compose kill example

# 生产环境
systemctl stop app-example
```

**验证步骤**:
- [ ] 进程已终止
- [ ] 无僵尸进程
- [ ] 端口已释放

---

### 3. 重启服务

```bash
# 开发环境
docker-compose restart example

# 生产环境
systemctl restart app-example
```

**重启后验证**:
- [ ] 服务正常启动
- [ ] 配置正确加载
- [ ] 数据库连接正常
- [ ] 冒烟测试通过

---

## 配置管理

### 配置文件
| 环境 | 配置文件 | 说明 |
|------|---------|------|
| 开发 | `config/dev.yaml` | 本地开发配置 |
| 预发布 | `config/staging.yaml` | 预发布环境配置 |
| 生产 | `config/prod.yaml` | 生产环境配置（无密钥）|

### 环境变量
| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `APP_ENV` | 是 | dev | 运行环境 |
| `DATABASE_URL` | 生产必填 | - | 数据库连接字符串 |
| `LOG_LEVEL` | 否 | INFO | 日志级别（DEBUG/INFO/WARNING/ERROR）|
| `API_KEY` | 生产必填 | - | API 密钥 |

### 配置加载顺序
```
1. config/defaults.yaml    （默认值）
2. config/<env>.yaml        （环境特定）
3. 环境变量                 （覆盖）
4. Secrets                  （最高优先级）
```

---

## 监控与告警

### 关键指标

#### 应用指标
- **请求量（QPS）**：每秒请求数
- **响应时间**：P50, P95, P99
- **错误率**：5xx 错误占比
- **可用性**：Uptime 百分比

#### 业务指标
- 任务处理成功率
- 平均处理时长
- 并发任务数

#### 系统指标
- CPU 使用率
- 内存使用率
- 磁盘 I/O
- 网络带宽

### 告警规则

| 告警名称 | 触发条件 | 严重级别 | 响应时间 | 处理步骤 |
|---------|---------|---------|---------|---------|
| HighLatency | P95 > 2000ms | Warning | 30分钟 | 1. 检查数据库慢查询<br>2. 查看系统资源<br>3. 考虑扩容 |
| ErrorRate | 错误率 > 5% | Critical | 15分钟 | 1. 查看错误日志<br>2. 检查依赖服务<br>3. 考虑回滚 |
| DatabaseDown | 数据库不可用 | Critical | 5分钟 | 1. 联系 DBA<br>2. 切换只读模式<br>3. 通知用户 |
| DiskFull | 磁盘使用 > 90% | Warning | 1小时 | 1. 清理日志<br>2. 扩容磁盘 |

### 监控仪表板
- **Grafana**: http://grafana.example.com/dashboard/example
- **日志系统**: http://kibana.example.com/app/discover
- **APM**: http://apm.example.com/services/example

---

## 故障排查

### 1. 服务无法启动

#### 症状
- 进程启动失败
- 健康检查返回 503

#### 排查步骤
```bash
# 1. 检查配置
cat config/prod.yaml
env | grep APP_

# 2. 检查日志
tail -f /var/log/app/example.log

# 3. 检查端口占用
lsof -i:8000

# 4. 检查依赖服务
curl http://database:5432
redis-cli ping
```

#### 解决方案
1. 修复配置错误
2. 释放被占用的端口
3. 启动依赖服务
4. 检查权限和资源

---

### 2. 连接数据库失败

#### 症状
- 日志显示数据库连接错误
- API 返回 500 错误

#### 排查步骤
```bash
# 1. 检查数据库配置
echo $DATABASE_URL

# 2. 测试网络连接
telnet db-host 5432
ping db-host

# 3. 检查数据库状态
psql -h db-host -U user -d dbname -c "SELECT 1"

# 4. 查看数据库日志
docker logs postgres-container
```

#### 解决方案
1. 修复数据库连接字符串
2. 检查网络和防火墙
3. 重启数据库服务
4. 检查数据库用户权限

---

### 3. 性能下降

#### 症状
- 响应时间显著增加
- P95 > 2000ms

#### 排查步骤
```bash
# 1. 检查慢查询
psql -d app -c "SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10"

# 2. 检查系统资源
top
free -h
df -h
iostat

# 3. 检查缓存命中率
redis-cli INFO stats | grep hit_rate

# 4. 查看应用性能分析
py-spy record -o profile.svg -- python -m example.main
```

#### 解决方案
1. 优化慢查询（添加索引）
2. 扩容系统资源
3. 优化缓存策略
4. 代码性能优化

---

### 4. 错误率升高

#### 症状
- 错误率 > 5%
- 大量 5xx 错误

#### 排查步骤
```bash
# 1. 查看错误日志
grep "ERROR" /var/log/app/example.log | tail -100

# 2. 统计错误类型
grep "ERROR" /var/log/app/example.log | awk '{print $NF}' | sort | uniq -c

# 3. 检查依赖服务
curl http://dependency-service/health

# 4. 查看最近变更
git log --oneline -10
```

#### 解决方案
1. 修复已知 Bug
2. 重启依赖服务
3. 考虑回滚到上一版本
4. 限流保护

---

## 回滚操作

### 回滚触发条件
- 错误率 > 10%
- P95 延迟 > 5000ms（基线的 2.5 倍）
- 发现严重安全漏洞
- 数据一致性问题

### 回滚步骤

#### 1. 决策评估（< 15分钟）
```bash
# 评估影响范围
git diff <current-tag> <previous-tag> --stat

# 检查回滚风险
make rollback_check PREV_REF=<previous-tag>

# 决策：回滚 or 修复
```

#### 2. 代码回滚（< 15分钟）
```bash
# 方法 1：Git revert（推荐）
git revert <bad-commit-hash>
git push

# 方法 2：回退到上一标签
git checkout <previous-tag>
git tag -a v1.0.1-rollback -m "Rollback to v1.0.0"
git push --tags

# 方法 3：强制回退（谨慎）
git reset --hard <previous-tag>
git push -f origin main  # 仅紧急情况
```

#### 3. 数据库回滚（< 10分钟）
```bash
# 1. 备份当前数据
pg_dump app > backup_before_rollback_$(date +%Y%m%d_%H%M%S).sql

# 2. 执行回滚脚本
psql -d app -f migrations/<version>_down.sql

# 3. 验证表结构
psql -d app -c "\d+ table_name"
```

#### 4. 配置回滚（< 5分钟）
```bash
# 恢复配置文件
git checkout <previous-tag> -- config/

# 重新加载配置
systemctl reload app-example
```

#### 5. 重新部署（< 20分钟）
```bash
# 停止当前版本
systemctl stop app-example

# 部署上一版本
./deploy.sh <previous-tag>

# 启动服务
systemctl start app-example
```

#### 6. 验证回滚（< 10分钟）
```bash
# 1. 健康检查
curl http://localhost:8000/health
# 预期: 200 OK

# 2. 冒烟测试
pytest tests/example/test_smoke.py -v
# 预期: 全部通过

# 3. 监控指标
# 查看 Grafana，确认指标恢复正常

# 4. 用户验证
# 确认核心功能可用
```

### 回滚时间目标
- **决策时间**: < 15 分钟
- **执行时间**: < 30 分钟
- **验证时间**: < 15 分钟
- **总计**: < 1 小时

---

## 备份与恢复

### 数据备份策略

#### 自动备份
```bash
# 每日全量备份（cron）
0 2 * * * pg_dump app > /backup/app_$(date +\%Y\%m\%d).sql

# 实时增量备份（WAL archiving）
# 配置 postgresql.conf:
# wal_level = replica
# archive_mode = on
# archive_command = 'cp %p /backup/wal/%f'
```

#### 手动备份
```bash
# 完整备份
make backup

# 或手动执行
pg_dump -h localhost -U user -d app -F c -f backup_$(date +%Y%m%d).dump
```

### 恢复操作

#### 从全量备份恢复
```bash
# 1. 停止服务
systemctl stop app-example

# 2. 恢复数据库
psql -d app < backup_YYYYMMDD.sql

# 3. 验证数据
psql -d app -c "SELECT COUNT(*) FROM users"

# 4. 启动服务
systemctl start app-example

# 5. 验证功能
pytest tests/example/test_smoke.py
```

#### 点对时恢复（PITR）
```bash
# 恢复到特定时间点
pg_restore -d app -T <timestamp> backup.dump
```

---

## 扩容操作

### 水平扩容

#### 步骤
```bash
# 1. 增加实例数
docker-compose up --scale example=3

# 2. 配置负载均衡
# 编辑 nginx.conf 或更新 k8s deployment

# 3. 验证负载分布
curl http://lb/stats

# 4. 监控新实例
# 查看 Grafana 确认所有实例正常
```

**验证**:
- [ ] 所有实例健康检查通过
- [ ] 负载均衡分布均匀
- [ ] 无性能下降
- [ ] 错误率无异常

---

### 垂直扩容

#### 步骤
```bash
# 1. 调整资源配置
vim docker-compose.yml
# 修改 resources.limits.cpus 和 memory

# 2. 调整应用配置
vim config/prod.yaml
# 修改并发数、连接池大小

# 3. 重启服务
docker-compose up -d example

# 4. 验证资源使用
docker stats example
```

---

## 安全管理

### 密钥轮换

#### API 密钥轮换（每90天）
```bash
# 1. 生成新密钥
python -c "import secrets; print(secrets.token_urlsafe(32))"

# 2. 更新配置
# 在密钥管理服务中更新 API_KEY

# 3. 重启服务
systemctl reload app-example

# 4. 验证
curl -H "Authorization: Bearer <new-key>" http://localhost:8000/api/test
```

### 日志管理

#### 日志位置
- **开发环境**: stdout
- **生产环境**: `/var/log/app/example.log`

#### 日志轮换
```bash
# logrotate 配置
/var/log/app/example.log {
    daily
    rotate 180
    compress
    delaycompress
    notifempty
    create 0644 app app
    postrotate
        systemctl reload app-example
    endscript
}
```

### 审计日志
- **保留期**: 180 天
- **内容**: 用户操作、配置变更、权限变更
- **位置**: `/var/log/audit/example.log`

---

## 调试指南

### 日志调试

#### 临时提高日志级别
```bash
# 方法 1：环境变量
export LOG_LEVEL=DEBUG
systemctl restart app-example

# 方法 2：配置文件
vim config/prod.yaml
# 修改 logging.level: DEBUG
systemctl reload app-example
```

#### 查看实时日志
```bash
# 跟踪日志
tail -f /var/log/app/example.log

# 过滤错误
tail -f /var/log/app/example.log | grep ERROR

# 查看最近 100 行
tail -100 /var/log/app/example.log
```

### 性能调试

#### 性能分析
```bash
# Python 性能分析
py-spy record -o profile.svg --pid <pid>

# 查看慢查询
psql -d app -c "
  SELECT query, mean_time, calls 
  FROM pg_stat_statements 
  ORDER BY mean_time DESC 
  LIMIT 10
"

# 查看系统调用
strace -p <pid> -c
```

### 网络调试
```bash
# 检查端口监听
netstat -tulpn | grep example

# 测试连接
curl -v http://localhost:8000/health

# 抓包分析
tcpdump -i any port 8000 -w capture.pcap
```

---

## 验证清单

### 部署后验证
```markdown
- [ ] 服务启动正常（systemctl status）
- [ ] 健康检查通过（/health 返回 200）
- [ ] 数据库连接正常
- [ ] 配置加载正确
- [ ] 日志输出正常
- [ ] 监控指标正常
- [ ] 告警配置生效
- [ ] 冒烟测试通过
```

### 定期巡检（每周）
```markdown
- [ ] 检查日志无异常
- [ ] 监控指标在正常范围
- [ ] 磁盘空间充足（> 20%）
- [ ] 备份正常执行
- [ ] 无安全告警
- [ ] 依赖服务正常
```

---

## 相关文档
- **模块架构**: `README.md`
- **接口契约**: `CONTRACT.md`
- **测试计划**: `TEST_PLAN.md`
- **配置指南**: `docs/process/CONFIG_GUIDE.md`
- **监控规范**: `docs/project/SYSTEM_BOUNDARY.md`

