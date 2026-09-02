from playwright.sync_api import Locator
import logging


class BaseElements:

    def __init__(self,locator: Locator,element_description: str):
        """Initializes the base element with locator and description."""
        self.locator = locator
        self.default_timeout = 10000
        self.element_description = element_description
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
