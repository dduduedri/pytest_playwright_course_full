from playwright.sync_api import expect
from ui.elements.base_element import BaseElements


class Validation(BaseElements):

    def to_have_text(self, expected_text: str, timeout: int | None = None):
        """Validates that the element's complete text matches the expected text."""
        self.logger.info(f"[ expect to_have_text: {expected_text} ] -> {self.element_description}")
        expect(self.locator).to_have_text(expected_text, timeout=timeout)

    def to_contain_text(self, expected_text: str, timeout: int | None = None):
        """Validates that the element contains the expected text."""
        self.logger.info(f"[ expect to_contain_text: {expected_text} ] -> {self.element_description}")
        expect(self.locator).to_contain_text(expected_text, timeout=timeout)

    def to_be_visible(self, timeout: int | None = None):
        """Validates that the element is visible to the user."""
        self.logger.info(f"[ expect to_be_visible ] -> {self.element_description}")
        expect(self.locator).to_be_visible(timeout=timeout)

    def to_be_hidden(self, timeout: int | None = None):
        """Validates that the element is hidden or not visible."""
        self.logger.info(f"[ expect to_be_hidden ] -> {self.element_description}")
        expect(self.locator).to_be_hidden(timeout=timeout)

    def to_be_enabled(self, timeout: int | None = None):
        """Validates that the element is enabled and can be interacted with."""
        self.logger.info(f"[ expect to_be_enabled ] -> {self.element_description}")
        expect(self.locator).to_be_enabled(timeout=timeout)

    def to_be_disabled(self, timeout: int | None = None):
        """Validates that the element is disabled and cannot be interacted with."""
        self.logger.info(f"[ expect to_be_disabled ] -> {self.element_description}")
        expect(self.locator).to_be_disabled(timeout=timeout)

    def to_have_value(self, expected_value: str, timeout: int | None = None):
        """Validates that an input element has the expected value."""
        self.logger.info(f"[ expect to_have_value: {expected_value} ] -> {self.element_description}")
        expect(self.locator).to_have_value(expected_value, timeout=timeout)

    def to_have_count(self, expected_count: int, timeout: int | None = None):
        """Validates the number of elements matched by the locator."""
        self.logger.info(f"[ expect to_have_count: {expected_count} ] -> {self.element_description}")
        expect(self.locator).to_have_count(expected_count, timeout=timeout)

    def to_have_attribute(self,name: str,value: str,timeout: int | None = None):
        """Validates that the element has the expected HTML attribute and value."""
        self.logger.info(f"[ expect to_have_attribute: {name}={value} ] -> {self.element_description}")
        expect(self.locator).to_have_attribute(name, value, timeout=timeout)

    def to_have_class(self, expected_class: str, timeout: int | None = None):
        """Validates that the element has the expected class attribute value."""
        self.logger.info(f"[ expect to_have_class: {expected_class} ] -> {self.element_description}")
        expect(self.locator).to_have_class(expected_class, timeout=timeout)

    def to_be_checked(self, timeout: int | None = None):
        """Validates that a checkbox or radio button is checked."""
        self.logger.info(f"[ expect to_be_checked ] -> {self.element_description}")
        expect(self.locator).to_be_checked(timeout=timeout)

    def not_to_be_visible(self, timeout: int | None = None):
        """Validates that the element is not visible."""
        self.logger.info(f"[ expect not_to_be_visible ] -> {self.element_description}")
        expect(self.locator).not_to_be_visible(timeout=timeout)

    def not_to_have_text(self, text: str, timeout: int | None = None):
        """Validates that the element's complete text does not match the specified text."""
        self.logger.info(f"[ expect not_to_have_text: {text} ] -> {self.element_description}")
        expect(self.locator).not_to_have_text(text, timeout=timeout)