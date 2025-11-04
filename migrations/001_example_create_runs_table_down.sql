-- 回滚：删除 runs 表
-- 版本：001
-- 警告：此操作将删除表和所有数据

-- 删除索引
DROP INDEX IF EXISTS idx_runs_created_at;
DROP INDEX IF EXISTS idx_runs_agent;

-- 删除表
DROP TABLE IF EXISTS runs;

