"""
Pytest configuration for example module tests
测试配置和共享 fixtures
"""
import pytest


@pytest.fixture
def sample_data():
    """示例测试数据 [Fixture]"""
    return {
        "task": "示例任务",
        "language": "python",
        "dry_run": False
    }


@pytest.fixture
def expected_response():
    """期望的响应格式 [Fixture]"""
    return {
        "result": "处理完成",
        "status": "success",
        "metadata": {
            "duration_ms": 100,
            "version": "1.0.0"
        }
    }


@pytest.fixture
def mock_database(monkeypatch):
    """Mock 数据库连接 [Fixture]"""
    # 示例：使用 monkeypatch 替换数据库连接
    # class MockDB:
    #     def query(self, *args):
    #         return []
    # 
    # monkeypatch.setattr('example.db', MockDB())
    pass


@pytest.fixture(scope="session")
def test_config():
    """测试配置 [Fixture - Session 级别]"""
    return {
        "env": "test",
        "database_url": "sqlite:///:memory:",
        "cache_enabled": False
    }


@pytest.fixture
def sample_user():
    """示例用户数据 [Fixture]"""
    return {
        "id": "test-user-001",
        "email": "test@example.com",
        "name": "测试用户"
    }


# Pytest 钩子：自定义测试行为
def pytest_configure(config):
    """Pytest 配置钩子"""
    # 添加自定义标记
    config.addinivalue_line(
        "markers", "slow: 标记慢速测试"
    )
    config.addinivalue_line(
        "markers", "integration: 标记集成测试"
    )


# 测试失败时的自定义处理（可选）
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试报告生成钩子"""
    outcome = yield
    rep = outcome.get_result()
    
    # 可以在这里添加自定义日志或报告
    if rep.when == "call" and rep.failed:
        print(f"\n❌ 测试失败: {item.nodeid}")

