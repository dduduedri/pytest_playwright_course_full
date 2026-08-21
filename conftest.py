import pytest
from playwright.sync_api import Browser, Page, Playwright


# fixtures live in dedicated modules and are registered as plugins
pytest_plugins = (
    "fixtures.data_fixtures",
)

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


