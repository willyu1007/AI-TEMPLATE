-- Rollback: drop runs table (version 001)
DROP INDEX IF EXISTS idx_runs_created_at;
DROP INDEX IF EXISTS idx_runs_agent;
DROP TABLE IF EXISTS runs;
