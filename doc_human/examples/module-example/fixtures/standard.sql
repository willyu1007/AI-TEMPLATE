-- Fixtures: standard
-- Module: example
-- Purpose: integration tests
-- Records: 20

INSERT INTO runs (id, task_description, language, status, result, created_at, updated_at) VALUES
-- Success cases (14 / 70%)
('run-std-001', 'Python task: data processing', 'python', 'success', '{"output": "Processed 100 records"}', NOW() - INTERVAL '7 days', NOW() - INTERVAL '7 days' + INTERVAL '5 seconds'),
('run-std-002', 'Python task: API call', 'python', 'success', '{"output": "API response received"}', NOW() - INTERVAL '6 days', NOW() - INTERVAL '6 days' + INTERVAL '3 seconds'),
('run-std-003', 'JavaScript task: frontend render', 'javascript', 'success', '{"output": "Rendered successfully"}', NOW() - INTERVAL '6 days', NOW() - INTERVAL '6 days' + INTERVAL '2 seconds'),
('run-std-004', 'Go task: concurrent processing', 'go', 'success', '{"output": "10 goroutines completed"}', NOW() - INTERVAL '5 days', NOW() - INTERVAL '5 days' + INTERVAL '10 seconds'),
('run-std-005', 'Python task: database query', 'python', 'success', '{"output": "Query returned 50 rows"}', NOW() - INTERVAL '5 days', NOW() - INTERVAL '5 days' + INTERVAL '1 second'),
('run-std-006', 'JavaScript task: JSON parsing', 'javascript', 'success', '{"output": "JSON parsed"}', NOW() - INTERVAL '4 days', NOW() - INTERVAL '4 days' + INTERVAL '1 second'),
('run-std-007', 'Python task: file processing', 'python', 'success', '{"output": "File processed: 1.2MB"}', NOW() - INTERVAL '4 days', NOW() - INTERVAL '4 days' + INTERVAL '15 seconds'),
('run-std-008', 'Go task: network request', 'go', 'success', '{"output": "HTTP 200 OK"}', NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days' + INTERVAL '2 seconds'),
('run-std-009', 'Python task: machine learning', 'python', 'success', '{"output": "Model trained, accuracy 95%"}', NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days' + INTERVAL '60 seconds'),
('run-std-010', 'JavaScript task: data validation', 'javascript', 'success', '{"output": "All fields validated"}', NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days' + INTERVAL '1 second'),
('run-std-011', 'Python task: report generation', 'python', 'success', '{"output": "Report generated: report.pdf"}', NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days' + INTERVAL '8 seconds'),
('run-std-012', 'Go task: cache refresh', 'go', 'success', '{"output": "Cache refreshed"}', NOW() - INTERVAL '1 days', NOW() - INTERVAL '1 days' + INTERVAL '1 second'),
('run-std-013', 'Python task: email sending', 'python', 'success', '{"output": "Email sent to 10 recipients"}', NOW() - INTERVAL '1 days', NOW() - INTERVAL '1 days' + INTERVAL '3 seconds'),
('run-std-014', 'JavaScript task: chart rendering', 'javascript', 'success', '{"output": "Chart rendered"}', NOW() - INTERVAL '12 hours', NOW() - INTERVAL '12 hours' + INTERVAL '2 seconds'),

-- Error cases (4 / 20%)
('run-std-015', 'Python task: syntax error', 'python', 'error', '{"error": "SyntaxError: invalid syntax"}', NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days' + INTERVAL '1 second'),
('run-std-016', 'JavaScript task: type error', 'javascript', 'error', '{"error": "TypeError: undefined is not a function"}', NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days' + INTERVAL '1 second'),
('run-std-017', 'Go task: nil pointer', 'go', 'error', '{"error": "runtime error: invalid memory address"}', NOW() - INTERVAL '1 days', NOW() - INTERVAL '1 days' + INTERVAL '1 second'),
('run-std-018', 'Python task: timeout', 'python', 'error', '{"error": "TimeoutError: operation timed out"}', NOW() - INTERVAL '6 hours', NOW() - INTERVAL '6 hours' + INTERVAL '1 second'),

-- Running cases (2 / 10%)
('run-std-019', 'Python task: long running', 'python', 'running', NULL, NOW() - INTERVAL '30 minutes', NOW() - INTERVAL '30 minutes'),
('run-std-020', 'JavaScript task: batch processing', 'javascript', 'running', NULL, NOW() - INTERVAL '10 minutes', NOW() - INTERVAL '10 minutes');
