# 运维手册（Runbook）

## 目标
提供 common 模块的完整运维指南，包括部署、监控、故障排查和回滚操作。

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
# common 模块作为基础库，随主应用启动
export APP_ENV=dev
export LOG_LEVEL=DEBUG
python -m app.main
```

#### 生产环境
```bash
# 1. 切换到生产配置
export APP_ENV=prod

# 2. 启动服务
systemctl start app-main

# 3. 验证启动
systemctl status app-main
curl http://localhost:8000/health
```

**验证步骤**:
- [ ] 进程正常运行
- [ ] 健康检查接口返回 200
- [ ] 日志无错误信息
- [ ] Common 模块正确加载

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
| `SECRET_KEY` | 生产必填 | - | 加密密钥 |

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
- **日志记录速度**：每秒日志条数
- **中间件响应时间**：P50, P95, P99
- **加密/解密性能**：操作耗时
- **认证成功率**：认证成功占比

#### 系统指标
- CPU 使用率
- 内存使用率
- 磁盘 I/O
- 网络带宽

### 告警规则

| 告警名称 | 触发条件 | 严重级别 | 响应时间 | 处理步骤 |
|---------|---------|---------|---------|---------|
| HighLatency | 中间件P95 > 100ms | Warning | 30分钟 | 1. 检查中间件性能<br>2. 查看系统资源 |
| AuthFailure | 认证失败率 > 10% | Critical | 15分钟 | 1. 检查密钥配置<br>2. 查看错误日志 |
| EncryptionError | 加密失败 > 5次/分钟 | Critical | 5分钟 | 1. 检查SECRET_KEY<br>2. 联系安全团队 |

---

## 故障排查

### 1. 中间件初始化失败

#### 症状
- 应用启动失败
- 日志显示中间件错误

#### 排查步骤
```bash
# 1. 检查配置
cat config/prod.yaml
env | grep APP_

# 2. 检查日志
tail -f /var/log/app/main.log | grep middleware

# 3. 检查依赖服务
redis-cli ping
```

#### 解决方案
1. 修复配置错误
2. 启动依赖服务
3. 检查权限和资源

---

### 2. 加密解密失败

#### 症状
- 用户数据无法解密
- 日志显示加密错误

#### 排查步骤
```bash
# 1. 检查密钥配置
echo $SECRET_KEY

# 2. 测试加密功能
python -c "from common.utils.encryption import encrypt, decrypt; print(decrypt(encrypt('test')))"

# 3. 查看错误日志
grep "encryption" /var/log/app/main.log
```

#### 解决方案
1. 修复密钥配置
2. 检查加密算法版本
3. 恢复备份数据

---

### 3. 性能下降

#### 症状
- 响应时间显著增加
- 中间件耗时过长

#### 排查步骤
```bash
# 1. 检查系统资源
top
free -h

# 2. 检查日志量
wc -l /var/log/app/*.log

# 3. 查看中间件性能
py-spy record -o profile.svg -- python -m app.main
```

#### 解决方案
1. 优化日志级别（降低到 INFO）
2. 增加缓存
3. 扩容系统资源

---

## 回滚操作

### 回滚触发条件
- 认证失败率 > 10%
- 加密解密错误频发
- 中间件导致应用崩溃
- 发现严重安全漏洞

### 回滚步骤

#### 1. 决策评估（< 15分钟）
```bash
# 评估影响范围
git diff <current-tag> <previous-tag> -- modules/common/

# 检查回滚风险
make rollback_check PREV_REF=<previous-tag>
```

#### 2. 代码回滚（< 15分钟）
```bash
# 回退到上一标签
git checkout <previous-tag> -- modules/common/
git commit -m "Rollback common module to <previous-tag>"
git push
```

#### 3. 重新部署（< 20分钟）
```bash
# 停止当前版本
systemctl stop app-main

# 部署上一版本
./deploy.sh <previous-tag>

# 启动服务
systemctl start app-main
```

#### 4. 验证回滚（< 10分钟）
```bash
# 1. 健康检查
curl http://localhost:8000/health
# 预期: 200 OK

# 2. 冒烟测试
pytest tests/common/ -v -k smoke

# 3. 验证核心功能
python -c "from common.utils.encryption import encrypt, decrypt; print('OK' if decrypt(encrypt('test')) == 'test' else 'FAIL')"
```

---

## 备份与恢复

### 密钥备份
```bash
# 定期备份密钥配置
mkdir -p /backup/secrets/
echo $SECRET_KEY > /backup/secrets/secret_key_$(date +%Y%m%d).txt
chmod 600 /backup/secrets/*.txt
```

### 配置备份
```bash
# 备份配置文件
cp config/prod.yaml /backup/config/prod_$(date +%Y%m%d).yaml
```

---

## 安全管理

### 密钥轮换

#### SECRET_KEY 轮换（每90天）
```bash
# 1. 生成新密钥
python -c "import secrets; print(secrets.token_urlsafe(32))"

# 2. 更新配置
# 在密钥管理服务中更新 SECRET_KEY

# 3. 重启服务
systemctl restart app-main

# 4. 验证
curl http://localhost:8000/health
```

### 日志管理

#### 日志位置
- **开发环境**: stdout
- **生产环境**: `/var/log/app/main.log`

#### 日志轮换
```bash
# logrotate 配置
/var/log/app/*.log {
    daily
    rotate 180
    compress
    delaycompress
    notifempty
    create 0644 app app
}
```

---

## 验证清单

### 部署后验证
```
- [ ] 服务启动正常
- [ ] Common 模块正确加载
- [ ] 中间件初始化成功
- [ ] 加密解密功能正常
- [ ] 认证功能正常
- [ ] 日志输出正常
- [ ] 监控指标正常
```

### 定期巡检（每周）
```
- [ ] 检查日志无异常
- [ ] 监控指标在正常范围
- [ ] 密钥有效期检查
- [ ] 无安全告警
```

---

## 相关文档
- **模块架构**: `README.md`
- **接口契约**: `CONTRACT.md`
- **测试计划**: `TEST_PLAN.md`
- **配置指南**: `../../doc/process/CONFIG_GUIDE.md`

