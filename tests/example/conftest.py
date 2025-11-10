"""
Pytest configuration for example module tests
 fixtures
"""
import pytest


@pytest.fixture
def sample_data():
    """ [Fixture]"""
    return {
        "task": "",
        "language": "python",
        "dry_run": False
    }


@pytest.fixture
def expected_response():
    """ [Fixture]"""
    return {
        "result": "",
        "status": "success",
        "metadata": {
            "duration_ms": 100,
            "version": "1.0.0"
        }
    }


@pytest.fixture
def mock_database(monkeypatch):
    """Mock  [Fixture]"""
    #  monkeypatch 
    # class MockDB:
    #     def query(self, *args):
    #         return []
    # 
    # monkeypatch.setattr('example.db', MockDB())
    pass


@pytest.fixture(scope="session")
def test_config():
    """ [Fixture - Session ]"""
    return {
        "env": "test",
        "database_url": "sqlite:///:memory:",
        "cache_enabled": False
    }


@pytest.fixture
def sample_user():
    """ [Fixture]"""
    return {
        "id": "test-user-001",
        "email": "test@example.com",
        "name": ""
    }


# Pytest 
def pytest_configure(config):
    """Pytest """
    # 
    config.addinivalue_line(
        "markers", "slow: "
    )
    config.addinivalue_line(
        "markers", "integration: "
    )


# 
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """"""
    outcome = yield
    rep = outcome.get_result()
    
    # 
    if rep.when == "call" and rep.failed:
        print(f"\n❌ : {item.nodeid}")

