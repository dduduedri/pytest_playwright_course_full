from playwright.sync_api import Page
import logging


class PageState:
    """Page level waits, for cases that are not tied to a single element."""

    def __init__(self, page: Page, page_description: str):
        """Initializes the page state with a page and description."""
        self.page = page
        self.default_timeout = 10000
        self.page_description = page_description
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")

    def wait_dom_loaded(self, timeout: int | None = None):
        """Waits until the HTML is parsed."""
        timeout = timeout or self.default_timeout
        self.logger.info(f"[ wait_dom_loaded timeout: {timeout} ] -> {self.page_description}")
        self.page.wait_for_load_state("domcontentloaded", timeout=timeout)

    def wait_page_loaded(self, timeout: int | None = None):
        """Waits until the page load event fires."""
        timeout = timeout or self.default_timeout
        self.logger.info(f"[ wait_page_loaded timeout: {timeout} ] -> {self.page_description}")
        self.page.wait_for_load_state("load", timeout=timeout)

    def wait_network_idle(self, timeout: int | None = None):
        """Waits until there are no network connections for at least 500ms."""
        timeout = timeout or self.default_timeout
        self.logger.info(f"[ wait_network_idle timeout: {timeout} ] -> {self.page_description}")
        self.page.wait_for_load_state("networkidle", timeout=timeout)

    def wait_url(self, url: str, timeout: int | None = None):
        """Waits until the page reaches the expected URL, glob or regex."""
        timeout = timeout or self.default_timeout
        self.logger.info(f"[ wait_url: {url} timeout: {timeout} ] -> {self.page_description}")
        self.page.wait_for_url(url, timeout=timeout)

    def expect_response(self, url_part: str, timeout: int | None = None):
        """Returns a context manager that waits for a response whose URL contains url_part.

        Wrap the action that triggers the request:
            with PageState(page, "Add To Cart").expect_response("add-to-order") as response:
                button.click()
            print(response.value.status)
        """
        timeout = timeout or self.default_timeout
        self.logger.info(f"[ expect_response contains: {url_part} timeout: {timeout} ] -> {self.page_description}")
        return self.page.expect_response(lambda response: url_part in response.url, timeout=timeout)
