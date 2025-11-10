-- Fixtures: standard (标准测试集)
-- 模块: example
-- 用途: 集成测试
-- 记录数: 20条

-- 插入runs表测试数据
INSERT INTO runs (id, task_description, language, status, result, created_at, updated_at) VALUES
-- Success cases (14条, 70%)
('run-std-001', 'Python任务：数据处理', 'python', 'success', '{"output": "Processed 100 records"}', NOW() - INTERVAL '7 days', NOW() - INTERVAL '7 days' + INTERVAL '5 seconds'),
('run-std-002', 'Python任务：API调用', 'python', 'success', '{"output": "API response received"}', NOW() - INTERVAL '6 days', NOW() - INTERVAL '6 days' + INTERVAL '3 seconds'),
('run-std-003', 'JavaScript任务：前端渲染', 'javascript', 'success', '{"output": "Rendered successfully"}', NOW() - INTERVAL '6 days', NOW() - INTERVAL '6 days' + INTERVAL '2 seconds'),
('run-std-004', 'Go任务：并发处理', 'go', 'success', '{"output": "10 goroutines completed"}', NOW() - INTERVAL '5 days', NOW() - INTERVAL '5 days' + INTERVAL '10 seconds'),
('run-std-005', 'Python任务：数据库查询', 'python', 'success', '{"output": "Query returned 50 rows"}', NOW() - INTERVAL '5 days', NOW() - INTERVAL '5 days' + INTERVAL '1 second'),
('run-std-006', 'JavaScript任务：JSON解析', 'javascript', 'success', '{"output": "JSON parsed"}', NOW() - INTERVAL '4 days', NOW() - INTERVAL '4 days' + INTERVAL '1 second'),
('run-std-007', 'Python任务：文件处理', 'python', 'success', '{"output": "File processed: 1.2MB"}', NOW() - INTERVAL '4 days', NOW() - INTERVAL '4 days' + INTERVAL '15 seconds'),
('run-std-008', 'Go任务：网络请求', 'go', 'success', '{"output": "HTTP 200 OK"}', NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days' + INTERVAL '2 seconds'),
('run-std-009', 'Python任务：机器学习', 'python', 'success', '{"output": "Model trained, accuracy 95%"}', NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days' + INTERVAL '60 seconds'),
('run-std-010', 'JavaScript任务：数据验证', 'javascript', 'success', '{"output": "All fields validated"}', NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days' + INTERVAL '1 second'),
('run-std-011', 'Python任务：报表生成', 'python', 'success', '{"output": "Report generated: report.pdf"}', NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days' + INTERVAL '8 seconds'),
('run-std-012', 'Go任务：缓存更新', 'go', 'success', '{"output": "Cache refreshed"}', NOW() - INTERVAL '1 days', NOW() - INTERVAL '1 days' + INTERVAL '1 second'),
('run-std-013', 'Python任务：邮件发送', 'python', 'success', '{"output": "Email sent to 10 recipients"}', NOW() - INTERVAL '1 days', NOW() - INTERVAL '1 days' + INTERVAL '3 seconds'),
('run-std-014', 'JavaScript任务：图表生成', 'javascript', 'success', '{"output": "Chart rendered"}', NOW() - INTERVAL '12 hours', NOW() - INTERVAL '12 hours' + INTERVAL '2 seconds'),

-- Error cases (4条, 20%)
('run-std-015', 'Python任务：语法错误', 'python', 'error', '{"error": "SyntaxError: invalid syntax"}', NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days' + INTERVAL '1 second'),
('run-std-016', 'JavaScript任务：类型错误', 'javascript', 'error', '{"error": "TypeError: undefined is not a function"}', NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days' + INTERVAL '1 second'),
('run-std-017', 'Go任务：空指针', 'go', 'error', '{"error": "runtime error: invalid memory address"}', NOW() - INTERVAL '1 days', NOW() - INTERVAL '1 days' + INTERVAL '1 second'),
('run-std-018', 'Python任务：超时', 'python', 'error', '{"error": "TimeoutError: operation timed out"}', NOW() - INTERVAL '6 hours', NOW() - INTERVAL '6 hours' + INTERVAL '1 second'),

-- Running cases (2条, 10%)
('run-std-019', 'Python任务：长时间运行', 'python', 'running', NULL, NOW() - INTERVAL '30 minutes', NOW() - INTERVAL '30 minutes'),
('run-std-020', 'JavaScript任务：批量处理', 'javascript', 'running', NULL, NOW() - INTERVAL '10 minutes', NOW() - INTERVAL '10 minutes');

