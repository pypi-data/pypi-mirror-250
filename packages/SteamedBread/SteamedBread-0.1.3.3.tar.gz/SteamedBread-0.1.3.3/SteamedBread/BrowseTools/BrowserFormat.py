"""
@Author: 馒头 (chocolate)
@Email: neihanshenshou@163.com
@File: browser_format.py
@Time: 2023/12/27 21:19
"""

import os
import time

from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver import Remote, Chrome
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.options import Options

from SteamedBread.FileTools.FileOperateFormat import FileOperate
from SteamedBread.LoggerTools.Logger import logger


class ReuseChrome(Remote):

    def __init__(self, command_executor, session_id, caps=None):
        self.r_session_id = session_id
        self.caps = caps.to_capabilities() if isinstance(caps, Options) else caps
        Remote.__init__(self, command_executor=command_executor, desired_capabilities=self.caps)

    def start_session(self, capabilities, browser_profile=None):
        """
        重写start_session方法
        """
        if not isinstance(capabilities, dict):
            raise InvalidArgumentException("Capabilities must be a dictionary")
        if browser_profile:
            if "moz:firefoxOptions" in capabilities:
                capabilities["moz:firefoxOptions"]["profile"] = browser_profile.encoded
            else:
                capabilities.update({'firefox_profile': browser_profile.encoded})

        self.caps = options.Options().to_capabilities()
        self.session_id = self.r_session_id


class StartBrowserChrome:
    def __init__(self, capabilities=None):
        self._session_cache_path = os.path.join(os.path.dirname(__file__), "browser_session.yaml")
        self._caps = capabilities or {}

    def _session_cache_get(self):
        _session_cache = {}
        if os.path.exists(self._session_cache_path):
            _session_cache = FileOperate.read_file(filename=self._session_cache_path, jsonify=True, yamlify=True)

        return _session_cache

    def start_chrome(self):
        _session = self._session_cache_get()
        try:
            _expect_driver = ReuseChrome(
                command_executor=_session.get("executor_url"),
                session_id=_session.get("session_id"),
                caps=self._caps
            )
            _expect_driver.get(url="https://www.baidu.com")
            logger.info("[Congratulation] Current Browser Session Cache Is Enable!")
        except Exception as e:
            logger.warning(f"[Ignore] {e.args[0]}")
            _expect_driver = Chrome(options=self._caps)
            FileOperate.write_file(
                filename=self._session_cache_path,
                data={
                    "session_id": _expect_driver.session_id,
                    "executor_url": _expect_driver.service.service_url,
                    "timestamp": time.strftime("%F %T")
                }
            )

        return _expect_driver
