"""
@Author: kang.yang
@Date: 2023/10/26 09:48
"""
import time

from urllib import parse
from typing import Union
from kytest.utils.log import logger
from kytest.utils.config import config
from kytest.core.api.request import HttpReq
from kytest.core.ios.driver import IosDriver
from kytest.core.ios.element import IosElem
from kytest.core.web.driver import WebDriver
from kytest.core.web.element import WebElem
from kytest.core.android.driver import AdrDriver
from kytest.core.android.element import AdrElem


class TestCase(HttpReq):
    """
    测试用例基类，所有测试用例需要继承该类
    """

    driver: Union[AdrDriver, IosDriver, WebDriver] = None

    # ---------------------初始化-------------------------------
    def start_class(self):
        """
        Hook method for setup_class fixture
        :return:
        """
        pass

    def end_class(self):
        """
        Hook method for teardown_class fixture
        :return:
        """
        pass

    @classmethod
    def setup_class(cls):
        cls().start_class()

    @classmethod
    def teardown_class(cls):
        cls().end_class()

    def start(self):
        """
        Hook method for setup_method fixture
        :return:
        """
        pass

    def end(self):
        """
        Hook method for teardown_method fixture
        :return:
        """
        pass

    def setup_method(self):
        self.start_time = time.time()

        platform = config.get_common("platform")
        if platform == "android":
            device_id = config.get_app("device_id")
            pkg_name = config.get_app("pkg_name")
            self.driver = AdrDriver(device_id, pkg_name)
        elif platform == "ios":
            device_id = config.get_app("device_id")
            pkg_name = config.get_app("pkg_name")
            self.driver = IosDriver(device_id, pkg_name)
        elif platform == "web":
            browserName = config.get_web("browser_name")
            headless = config.get_web("headless")
            self.driver = WebDriver(browserName=browserName,
                                    headless=headless)

        if platform in ["android", "ios"]:
            if config.get_app("auto_start") is True:
                self.driver.start_app()

        self.start()

    def teardown_method(self):
        self.end()

        platform = config.get_common("platform")
        if platform in ["android", "ios"]:
            if config.get_app("auto_start") is True:
                self.driver.stop_app()

        take_time = time.time() - self.start_time
        logger.info("用例耗时: {:.2f} s".format(take_time))

    # 公共方法
    @staticmethod
    def sleep(n: float):
        """休眠"""
        logger.info(f"暂停: {n}s")
        time.sleep(n)

    def screenshot(self, name: str):
        """截图"""
        self.driver.screenshot(name)

    # UI方法
    def elem(self, *args, **kwargs):
        platform = config.get_common('platform')
        if platform == 'android':
            return AdrElem(self.driver, *args, **kwargs)
        elif platform == 'ios':
            return IosElem(self.driver, *args, **kwargs)
        elif platform == 'web':
            return WebElem(self.driver, *args, **kwargs)
        else:
            raise KeyError('支持android、ios、web三种平台')

    # 安卓方法
    def assert_act(self, activity_name: str, timeout=5):
        """断言当前页面的activity"""
        self.driver.assert_act(activity_name, timeout)

    # web方法
    def assert_title(self, title: str, timeout: int = 5):
        """断言页面标题"""
        self.driver.assert_title(title, timeout)

    @staticmethod
    def is_url_has_http(url):
        """针对为空和只有路径的情况，使用默认host进行补全"""
        host = config.get_common("base_url")
        if url is None:
            url = host
        if 'http' not in url:
            url = parse.urljoin(host, url)
        return url

    def assert_url(self, url: str = None, timeout: int = 5):
        """断言页面url"""
        url = self.is_url_has_http(url)
        self.driver.assert_url(url, timeout)

    def open(self, url):
        """打开页面"""
        url = self.is_url_has_http(url)
        self.driver.open(url)


