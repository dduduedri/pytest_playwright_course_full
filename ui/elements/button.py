from ui.elements.base_element import BaseElements


class Button(BaseElements):

    def click(self, timeout: int | None = None):
        """Clicks the button."""
        self.logger.info(f"[ click ] -> {self.element_description}")
        self.locator.click(timeout=timeout)

    def double_click(self, timeout: int | None = None):
        """Double-clicks the button."""
        self.logger.info(f"[ double_click ] -> {self.element_description}")
        self.locator.dblclick(timeout=timeout)

    def right_click(self, timeout: int | None = None):
        """Right-clicks the button."""
        self.logger.info(f"[ right_click ] -> {self.element_description}")
        self.locator.click(button="right",timeout=timeout
        )

    def hover(self, timeout: int | None = None):
        """Moves the mouse over the button."""
        self.logger.info(f"[ hover ] -> {self.element_description}")
        self.locator.hover(timeout=timeout)

    def press_key(self, key: str, timeout: int | None = None):
        """Presses a keyboard key on the button."""
        self.logger.info(f"[ press_key: {key} ] -> {self.element_description}")
        self.locator.press(key,timeout=timeout)