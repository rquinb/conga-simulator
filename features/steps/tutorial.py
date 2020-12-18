from behave import *

@given('we browse to "CONGA SIMULATOR" main page')
def step_impl(context):
    context.browser.get('http://frontend:8080')

@when('we look at the page')
def step_impl(context):
    pass

@then('we see "{app_title_text}" displayed as title')
def step_impl(context, app_title_text):
    app_title = context.browser.find_element_by_css_selector('.app-title')
    assert app_title.text == app_title_text