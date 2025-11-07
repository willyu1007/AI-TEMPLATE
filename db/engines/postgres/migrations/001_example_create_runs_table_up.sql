-- 迁移：创建 runs 表
-- 版本：001
-- 说明：用于记录 AI 代理的执行运行记录

CREATE TABLE IF NOT EXISTS runs (
    run_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent TEXT NOT NULL,
    prompt_hash TEXT,
    tool_version TEXT,
    latency_ms INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_runs_agent ON runs(agent);
CREATE INDEX IF NOT EXISTS idx_runs_created_at ON runs(created_at DESC);

-- 添加注释
COMMENT ON TABLE runs IS 'AI 代理执行运行记录';
COMMENT ON COLUMN runs.run_id IS '运行唯一标识';
COMMENT ON COLUMN runs.agent IS '代理名称';
COMMENT ON COLUMN runs.prompt_hash IS '提示词哈希';
COMMENT ON COLUMN runs.tool_version IS '工具版本';
COMMENT ON COLUMN runs.latency_ms IS '执行延迟（毫秒）';

