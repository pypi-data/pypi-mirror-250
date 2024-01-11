import pytest


@pytest.hookspec(firstresult=True)
def pytest_result_log(report: pytest.TestReport, config: pytest.Config, result: tuple):
    pass
