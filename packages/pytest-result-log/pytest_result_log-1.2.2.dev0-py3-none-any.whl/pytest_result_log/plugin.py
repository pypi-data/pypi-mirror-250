import logging
from string import Template

import pytest
from _pytest.reports import BaseReport

from . import const

logger = logging.getLogger("pytest_result_log")

template = ""
level_map = {}
enable_plugin = True
enable_separator = True


def pytest_cmdline_parse():
    global __test_set

    __test_set = set()


def pytest_addoption(parser):
    parser.addini(
        const.RESULT_LOG_ENABLE,
        type="bool",
        default=True,
        help="是否在日志中【记录】用例结果",
    )
    parser.addini(
        const.RESULT_LOG_SEPARATOR,
        type="bool",
        default=True,
        help="是否在日志中【划线分隔】用例结果",
    )
    parser.addini(
        const.RESULT_LOG_SEPARATOR_LENGTH,
        default="80",
        help="日志中【划线分隔】的长度",
    )
    parser.addini(
        const.RESULT_LOG_LEVEL_SEPARATOR,
        default="info",
        help="日志中【划线分隔】的等级",
    )
    parser.addini(
        const.RESULT_LOG_FORMAT,
        default="test status is ${result_word} (${case_id}): ${reason}",
        help="用例执行结果的日志格式",
    )
    parser.addini(
        const.RESULT_LOG_LEVEL_PASSED,
        default="info",
        help="用例执行通过的的日志等级",
    )
    parser.addini(
        const.RESULT_LOG_LEVEL_FAILED,
        default="error",
        help="用例执行失败的的日志等级",
    )
    parser.addini(
        const.RESULT_LOG_LEVEL_ERROR,
        default="error",
        help="用例执行出错的的日志等级",
    )
    parser.addini(
        const.RESULT_LOG_LEVEL_SKIPPED,
        default="warning",
        help="用例执行跳过的的日志等级",
    )
    parser.addini(
        const.RESULT_LOG_LEVEL_XPASS,
        default="warning",
        help="用例意外通过的的日志等级",
    )
    parser.addini(
        const.RESULT_LOG_LEVEL_XFAIL,
        default="warning",
        help="用例预期失败的的日志等级",
    )
    parser.addini(
        const.RESULT_LOG_LEVEL_VERBOSE,
        default="debug",
        help="失败详情的日志等级",
    )


def pytest_addhooks(pluginmanager):
    from . import hooks

    pluginmanager.add_hookspecs(hooks)


def pytest_configure(config):
    global template, level_map, enable_plugin, enable_separator, result_log_separator_len, result_log_level_separator
    enable_plugin = config.getini(const.RESULT_LOG_ENABLE)
    enable_separator = config.getini(const.RESULT_LOG_SEPARATOR)
    result_log_level_separator = config.getini(const.RESULT_LOG_LEVEL_SEPARATOR)

    try:
        result_log_separator_len = int(config.getini(const.RESULT_LOG_SEPARATOR_LENGTH))
    except ValueError:
        result_log_separator_len = 80

    template = config.getini(const.RESULT_LOG_FORMAT)
    level_map = {
        "PASSED": config.getini(const.RESULT_LOG_LEVEL_PASSED),
        "FAILED": config.getini(const.RESULT_LOG_LEVEL_FAILED),
        "ERROR": config.getini(const.RESULT_LOG_LEVEL_ERROR),
        "SKIPPED": config.getini(const.RESULT_LOG_LEVEL_SKIPPED),
        "XPASS": config.getini(const.RESULT_LOG_LEVEL_XPASS),
        "XFAIL": config.getini(const.RESULT_LOG_LEVEL_XFAIL),
        "VERBOSE": config.getini(const.RESULT_LOG_LEVEL_VERBOSE),
    }

    config.pluginmanager.register(Logger())


def pytest_runtest_setup(item):
    if enable_plugin and enable_separator:
        f = getattr(logger, result_log_level_separator)
        f(f"Start: {item.nodeid}".center(result_log_separator_len, "-"))


def pytest_runtest_teardown(item):
    if enable_plugin and enable_separator:
        f = getattr(logger, result_log_level_separator)
        f(f"End: {item.nodeid}".center(result_log_separator_len, "-"))


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_report_teststatus(report: BaseReport, config: pytest.Config):
    outcome = yield

    if not enable_plugin:
        return

    result = outcome.get_result()

    if report.when == "setup" and result[1] in ["s", "E"]:
        config.hook.pytest_result_log(report=report, config=config, result=result)

    if report.when == "call" and result[1] in [".", "F", "x", "X"]:
        config.hook.pytest_result_log(report=report, config=config, result=result)


def get_reason(report: BaseReport, result="F"):
    reason = "Please review verbose content"

    match result:
        case "F" | "x":
            try:
                reason = report.longrepr.reprtraceback.reprentries[
                    -1
                ].reprfileloc.message
            except Exception:
                ...
        case "E":
            try:
                reason = report.longrepr.errorstring.split("\n")[0]
            except Exception:
                ...
        case "s":
            try:
                reason = report.longrepr[2]
            except Exception:
                ...
        case _:
            reason = ""

    return reason, report.longreprtext


class Logger:
    def __init__(self):
        self.test_set = set()

    def pytest_result_log(
        self, report: BaseReport, config: pytest.Config, result: tuple
    ):
        if report.nodeid in self.test_set:
            return
        case_id = report.nodeid
        result_char = result[1]
        result_word = result[2]
        reason, detail = get_reason(report, result_char)

        level = level_map.get(result_word, "warning").lower()
        f = getattr(logger, level)
        f(Template(template).safe_substitute(**locals()))

        if detail:
            verbose_level = level_map.get("VERBOSE", "debug").lower()
            f = getattr(logger, verbose_level)(f"{case_id} -> {detail}")

        self.test_set.add(case_id)
        return case_id, result_word
