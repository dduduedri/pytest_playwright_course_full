from ui.elements.base_element import BaseElements


class Text(BaseElements):

    def get_text(self) -> str:
        """Returns the text content of the element."""
        extracted_text=self.locator.text_content() or ""
        self.logger.info(f"[ get_text ] -> {self.element_description} -> '{extracted_text}'")
        return extracted_text

    def get_inner_text(self) -> str:
        """Returns the rendered inner text of the element."""
        extracted_text = self.locator.inner_text() or ""
        self.logger.info(f"[ get element inner_text ] -> {self.element_description} -> '{extracted_text}'")
        return extracted_text