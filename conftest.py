import pytest
from playwright.sync_api import Browser, Page, Playwright


# fixtures live in dedicated modules and are registered as plugins
pytest_plugins = (
    "fixtures.data_fixtures",
)


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="my option: chrome or firefox"
    )
    parser.addoption(
        "--headless", action="store", default="False", help="my option: True or False"
    )


#A more efficient structure reuses the browser but creates a fresh context per test:
@pytest.fixture(scope="session")
def browser_setup(playwright: Playwright, request): # request gives access to global variables
    browser_name = request.config.getoption("--browser_name")  # pytest --browser_name firefox
    headless_option = str(request.config.getoption("--headless"))  # pytest --headless True
    if headless_option.lower() not in ("true", "false"):
        raise ValueError("headless must be True or False")
    headless = headless_option.lower() == "true"
    if browser_name == "chrome":
        browser = playwright.chromium.launch(headless=headless)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=headless)
    else:
        raise ValueError("browser_name must be chrome or firefox")
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
