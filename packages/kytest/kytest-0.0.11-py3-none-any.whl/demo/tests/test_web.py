"""
@Author: kang.yang
@Date: 2023/11/16 17:50
"""
import kytest
from kytest import *
from pages.web_page import IndexPage, LoginPage


class TestWebDemo(kytest.TestCase):

    def start(self):
        self.username = "13652435335"
        self.password = "wz123456@QZD"
        self.index_name = "首页"
        self.index_page = IndexPage(self.driver)
        self.login_page = LoginPage(self.driver)

    @title("登录")
    def test_login(self):
        self.index_page.open()
        self.index_page.loginBtn.click()
        self.sleep(5)
        self.login_page.pwdTab.click()
        self.login_page.userInput.\
            input(self.username)
        self.login_page.pwdInput.\
            input(self.password)
        self.login_page.accept.click()
        self.login_page.loginBtn.click()
        self.login_page.firstItem.click()
        self.assert_url()
        self.screenshot(self.index_name)


if __name__ == '__main__':
    kytest.main(
        platform='web',
        host="https://www-test.qizhidao.com/"
    )
