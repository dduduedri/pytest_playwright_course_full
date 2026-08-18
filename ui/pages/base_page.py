from playwright.sync_api import Page


# parent class for every page object: stores the shared Playwright `page`
# so child pages don't repeat it, and holds behavior common to all pages
class BasePage:
    """Common base for all page objects."""

    # receive the Playwright page (one browser tab) and keep a reference to it
    def __init__(self, page: Page):
        self.page = page
