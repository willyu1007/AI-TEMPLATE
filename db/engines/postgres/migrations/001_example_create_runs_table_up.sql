-- Migration: create runs table
-- Version: 001
-- Description: store AI agent run records

CREATE TABLE IF NOT EXISTS runs (
    run_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent TEXT NOT NULL,
    prompt_hash TEXT,
    tool_version TEXT,
    latency_ms INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_runs_agent ON runs(agent);
CREATE INDEX IF NOT EXISTS idx_runs_created_at ON runs(created_at DESC);

COMMENT ON TABLE runs IS 'AI agent run records';
COMMENT ON COLUMN runs.run_id IS 'Unique identifier';
COMMENT ON COLUMN runs.agent IS 'Agent name';
COMMENT ON COLUMN runs.prompt_hash IS 'Prompt hash';
COMMENT ON COLUMN runs.tool_version IS 'Tool version';
COMMENT ON COLUMN runs.latency_ms IS 'Latency in milliseconds';
