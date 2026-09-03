import logging

from playwright.sync_api import Error, Page, TimeoutError as PlaywrightTimeoutError


# parent class for every page object: stores the shared Playwright `page`
# so child pages don't repeat it, and holds behavior common to all pages
class BasePage:
    """Common base for all page objects."""

    # receive the Playwright page (one browser tab) and keep a reference to it
    def __init__(self, page: Page):
        self.page = page
        self.navigate_attempts = 2
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")

    def navigate(self, url: str, wait_until: str = "domcontentloaded", timeout: int | None = None):
        """Navigates to url, retrying when the demo app cancels or stalls the main frame request."""
        for attempt in range(1, self.navigate_attempts + 1):
            self.logger.info(f"[ navigate attempt {attempt}: {url} ] -> {self.__class__.__name__}")
            try:
                self.page.goto(url, wait_until=wait_until, timeout=timeout)
                return
            except PlaywrightTimeoutError:
                # the request stalled instead of failing, so nothing committed to the tab
                if attempt == self.navigate_attempts:
                    raise
            except Error as error:
                # an aborted request leaves the tab at about:blank, so a fresh goto is safe
                if "ERR_ABORTED" not in str(error) or attempt == self.navigate_attempts:
                    raise
