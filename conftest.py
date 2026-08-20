import pytest
from playwright.sync_api import Browser, Page, Playwright
from utils.data_reader import get_credentials, get_all_users,get_data
from ui.pages.base_page import BasePage


#A more efficient structure reuses the browser but creates a fresh context per test:
@pytest.fixture(scope="session")
def browser_setup(playwright: Playwright): # request gives access to global variables
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()

#new context for each test
@pytest.fixture(scope="function")
def context_setup(browser_setup: Browser) :
    browser = browser_setup
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture(scope="function")
def credentials_all() -> list[dict]:
    return get_all_users()

@pytest.fixture(scope="function")
def credentials_user(user_name):
    return get_credentials(user_name)

@pytest.fixture(scope="function")
def product_data(request):
    return get_data(request.param)

@pytest.fixture(scope="function")
def payment_data(request):
    return get_data(request.param)

@pytest.fixture(scope="function")
def credentials_user_with_param(request):
    return get_credentials(request.param)
