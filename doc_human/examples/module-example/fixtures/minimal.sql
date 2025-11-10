-- Fixtures: minimal
-- Module: example
-- Purpose: unit tests
-- Records: 3

INSERT INTO runs (id, task_description, language, status, result, created_at, updated_at) VALUES
('run-test-001', 'Sample task 1: simple success', 'python', 'success', '{"output": "Hello World"}', '2024-01-01 10:00:00', '2024-01-01 10:00:05'),
('run-test-002', 'Sample task 2: error handling', 'javascript', 'error', '{"error": "Syntax Error"}', '2024-01-02 11:00:00', '2024-01-02 11:00:03'),
('run-test-003', 'Sample task 3: long-running', 'go', 'running', NULL, '2024-01-03 12:00:00', '2024-01-03 12:00:00');
