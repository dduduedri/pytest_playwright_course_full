from ui.elements.base_element import BaseElements


class TextBox(BaseElements):

    def fill(self, value: str, timeout: int | None = None):
        """Fills the text box with the specified value."""
        self.logger.info(f"[ fill: {value} ] -> {self.element_description}")
        self.locator.fill(value,timeout=timeout)

    def clear(self, timeout: int | None = None):
        """Clears all text from the text box."""
        self.logger.info(f"[ clear ] -> {self.element_description}")
        self.locator.clear(timeout=timeout)

    def press_key(self, key: str, timeout: int | None = None):
        """Presses a keyboard key or key combination in the text box."""
        self.logger.info(f"[ press_key: {key} ] -> {self.element_description}")
        self.locator.press(key,timeout=timeout)

    def press_sequentially(self,value: str,delay: int | None = None,timeout: int | None = None):
        """Types text character by character to simulate keyboard input."""
        self.logger.info(f"[ press_sequentially: {value} ] -> {self.element_description}")
        self.locator.press_sequentially(value,delay=delay,timeout=timeout)