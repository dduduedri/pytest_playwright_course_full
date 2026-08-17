from playwright.sync_api import Locator
from ui.elements.base_element import BaseElements


class Filter(BaseElements):

    def has_text(self, text: str) -> Locator:
        """Filters elements that contain the specified text."""
        self.logger.info(f"[ filter by text: {text} ] -> {self.element_description}")
        return self.locator.filter(has_text=text)

    def has_locator(self, locator: Locator) -> Locator:
        """Filters elements that contain the specified child locator."""
        self.logger.info(f"[ filter by locator ] -> {self.element_description}")
        return self.locator.filter(has=locator)