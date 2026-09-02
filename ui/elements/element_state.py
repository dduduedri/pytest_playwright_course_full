from ui.elements.base_element import BaseElements


class ElementState(BaseElements):

    def wait_visible(self, timeout: int | None = None):
        """Waits until the element becomes visible."""
        timeout = timeout or self.default_timeout
        self.logger.info(f"[ wait_visible timeout: {timeout} ] -> {self.element_description}")
        self.locator.wait_for(state="visible", timeout=timeout)

    def wait_hidden(self, timeout: int | None = None):
        """Waits until the element is hidden or removed, for spinners and toasts."""
        timeout = timeout or self.default_timeout
        self.logger.info(f"[ wait_hidden timeout: {timeout} ] -> {self.element_description}")
        self.locator.wait_for(state="hidden", timeout=timeout)

    def wait_attached(self, timeout: int | None = None):
        """Waits until the element is present in the DOM, even if not yet visible."""
        timeout = timeout or self.default_timeout
        self.logger.info(f"[ wait_attached timeout: {timeout} ] -> {self.element_description}")
        self.locator.wait_for(state="attached", timeout=timeout)

    def wait_detached(self, timeout: int | None = None):
        """Waits until the element is removed from the DOM."""
        timeout = timeout or self.default_timeout
        self.logger.info(f"[ wait_detached timeout: {timeout} ] -> {self.element_description}")
        self.locator.wait_for(state="detached", timeout=timeout)

    def is_visible(self) -> bool:
        """Returns True when the element is visible right now, without waiting."""
        element_visible = self.locator.is_visible()
        self.logger.info(f"[ is_visible ] -> {self.element_description} -> {element_visible}")
        return element_visible

    def is_hidden(self) -> bool:
        """Returns True when the element is hidden right now, without waiting."""
        element_hidden = self.locator.is_hidden()
        self.logger.info(f"[ is_hidden ] -> {self.element_description} -> {element_hidden}")
        return element_hidden

    def is_enabled(self) -> bool:
        """Returns True when the element is enabled right now, without waiting."""
        element_enabled = self.locator.is_enabled()
        self.logger.info(f"[ is_enabled ] -> {self.element_description} -> {element_enabled}")
        return element_enabled
