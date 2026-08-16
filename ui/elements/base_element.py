from playwright.sync_api import Locator
import logging


class BaseElements:

    def __init__(self,locator: Locator,element_description: str):
        """Initializes the base element with locator and description."""
        self.locator = locator
        self.default_timeout = 10000
        self.element_description = element_description
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")

    def wait_visible(self, timeout: int | None = None):
        """Waits until the element becomes visible."""
        timeout = timeout or self.default_timeout
        self.logger.info(f"[ wait_visible timeout: {timeout} ] -> {self.element_description}")
        self.locator.wait_for(state="visible",timeout=timeout)

    def is_visible(self) -> bool:
        """Returns True when the element is visible."""
        self.logger.info(f"[ is_visible ] -> {self.element_description}")
        return self.locator.is_visible()