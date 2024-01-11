import kytest
from kytest import *
from pages.adr_page import DemoPage


@story('测试demo')
class TestAdrDemo(TestCase):
    def start(self):
        self.page = DemoPage(self.driver)
        self.set_act = '.me.MeSettingActivity'

    @title('进入设置页')
    def test_go_setting(self):
        self.page.adBtn.click_exists()
        self.page.myTab.click()
        self.page.setBtn.click()
        self.assert_act(self.set_act)
        self.screenshot("设置页")


if __name__ == '__main__':
    kytest.main(platform='android', pkg_name='企知道-测试版')
