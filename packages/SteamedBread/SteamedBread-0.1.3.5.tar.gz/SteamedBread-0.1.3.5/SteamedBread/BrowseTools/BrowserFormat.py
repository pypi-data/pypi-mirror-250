"""
@Author: 馒头 (chocolate)
@Email: neihanshenshou@163.com
@File: browser_format.py
@Time: 2023/12/27 21:19
"""

import os
import time

from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver import Chrome
from selenium.webdriver import Remote
from selenium.webdriver.chrome import options

from SteamedBread.FileTools.FileOperateFormat import FileOperate
from SteamedBread.LoggerTools.Logger import logger


class ReuseChrome(Remote):

    def __init__(self, command_executor, session_id):
        self.r_session_id = session_id
        Remote.__init__(self, command_executor=command_executor, desired_capabilities={})

    def start_session(self, capabilities, browser_profile=None):
        """
        重写start_session方法
        """
        if not isinstance(capabilities, dict):
            raise InvalidArgumentException("Capabilities must be a dict like {}")
        if browser_profile:
            if "moz:firefoxOptions" in capabilities:
                capabilities["moz:firefoxOptions"]["profile"] = browser_profile.encoded
            else:
                capabilities.update({'firefox_profile': browser_profile.encoded})

        self.capabilities = options.Options().to_capabilities()
        self.session_id = self.r_session_id
        self.w3c = False


class StartBrowserChrome:
    def __init__(self, capabilities=None):
        self.capabilities = capabilities
        self._session_cache_path = os.path.join(os.path.dirname(__file__), "browser_session.yaml")

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
                session_id=_session.get("session_id")
            )
            _expect_driver.refresh()
            logger.info("[Congratulation] Current Browser Session Cache Is Enable!")
        except Exception as e:
            logger.warning(f"[Ignore] {e.args[0]}")
            _options = options.Options()
            _options.add_experimental_option("w3c", False)
            _expect_driver = Chrome(desired_capabilities=self.capabilities, chrome_options=_options)
            FileOperate.write_file(
                filename=self._session_cache_path,
                data={
                    "session_id": _expect_driver.session_id,
                    "executor_url": _expect_driver.service.service_url,
                    "timestamp": time.strftime("%F %T")
                }
            )
        time.sleep(0.7)
        return _expect_driver
