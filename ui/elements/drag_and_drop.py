from playwright.sync_api import Locator
from ui.elements.base_element import BaseElements


class DragAndDrop(BaseElements):

    def drag_to(self,target: Locator,timeout: int | None = None):
        """Drags the current element to the specified target element."""
        self.logger.info(f"[ drag_to ] -> {self.element_description}")
        self.locator.drag_to(target,timeout=timeout)