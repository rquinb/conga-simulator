from behave import fixture, use_fixture
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

@fixture
def selenium_browser_firefox(context):
    context.browser = webdriver.Remote(command_executor="http://selenium-server:4444/wd/hub",
                                       desired_capabilities=DesiredCapabilities.FIREFOX)
    yield context.browser
    # -- CLEANUP-FIXTURE PART:
    context.browser.quit()

def before_all(context):
    use_fixture(selenium_browser_firefox, context)
