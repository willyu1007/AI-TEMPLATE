-- Fixtures: minimal (最小测试集)
-- 模块: example
-- 用途: 单元测试
-- 记录数: 3条

-- 插入runs表测试数据
INSERT INTO runs (id, task_description, language, status, result, created_at, updated_at) VALUES
('run-test-001', '示例任务1：简单测试', 'python', 'success', '{"output": "Hello World"}', '2024-01-01 10:00:00', '2024-01-01 10:00:05'),
('run-test-002', '示例任务2：错误处理测试', 'javascript', 'error', '{"error": "Syntax Error"}', '2024-01-02 11:00:00', '2024-01-02 11:00:03'),
('run-test-003', '示例任务3：长任务测试', 'go', 'running', NULL, '2024-01-03 12:00:00', '2024-01-03 12:00:00');

