# 模块初始化 - Phase 2: 创建目录

> **所属**: MODULE_INIT_GUIDE.md Phase 2  
> **用途**: Phase 2的详细执行指南  
> **目标**: 创建模块的基础目录结构

---

## 目标

创建模块的基础目录结构

---

## 2.1 创建基础目录

```bash
MODULE=<entity>

# 必需目录
mkdir -p modules/$MODULE/{core,doc}

# 可选：如has_api=true
mkdir -p modules/$MODULE/api

# 可选：如has_frontend=true
mkdir -p modules/$MODULE/frontend/components

# 可选：如有专属模型
mkdir -p modules/$MODULE/models
```

---

## 2.2 创建__init__.py（Python项目）

```bash
# 使core/和api/成为Python包
touch modules/$MODULE/core/__init__.py
touch modules/$MODULE/api/__init__.py
touch modules/$MODULE/models/__init__.py
```

---

## 2.3 验证目录结构

检查创建的目录：

```bash
tree modules/$MODULE
```

期望输出（示例）：

```
modules/user_auth/
├── core/
│   └── __init__.py
├── api/
│   └── __init__.py
└── doc/
```

---

## 常见问题

### Q: 如果是Go项目怎么办？
**A**: Go不需要__init__.py文件，但目录结构相同。

### Q: frontend/目录需要什么文件？
**A**: 取决于前端框架。React项目通常需要：
```
frontend/
├── components/
│   └── index.tsx
└── README.md
```

### Q: 目录创建失败怎么办？
**A**: 检查：
1. 是否在项目根目录执行？
2. 是否有写入权限？
3. modules/父目录是否存在？

---

## AI执行规范

**必须做**:
- ✅ 根据Phase 1确定的信息，只创建必要的目录
- ✅ 如has_api=false，不要创建api/目录
- ✅ 如has_frontend=false，不要创建frontend/目录

**不要做**:
- ❌ 不要创建不必要的目录
- ❌ 不要在core/和api/中放置代码（Phase 9才放代码）

---

## 下一步

完成目录创建后，进入 → [Phase 3: 生成文档](init-documents.md)

