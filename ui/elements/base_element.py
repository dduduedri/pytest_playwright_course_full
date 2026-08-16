from playwright.sync_api import Page, Locator
import logging


class BaseElements:
    def __init__(self,page:Page):
        self.page = page
        self.default_timeout=1000
        self.logger = logging.getLogger(__name__)

    def _wait_visible(self, locator: Locator, timeout=None):
        timeout = timeout or self.default_timeout
        try:
            locator.wait_for(
                state="visible",
                timeout=timeout
            )
        except Exception:
            self.page.screenshot()
            self.logger.error("Element was not visible")
            raise

    def _is_visible(self, locator: Locator) -> bool:
        return locator.is_visible()

    def _click_opr(self, locator: Locator):
        self._wait_visible(locator, timeout=1000)
        if self._is_visible(locator):
            locator.click()

    def _fill_opr(self, locator: Locator, value):
        self._wait_visible(locator, timeout=1000)
        if self._is_visible(locator):
            locator.fill(value)

    def by_locator(self,locator_path):
        return self.page.locator(locator_path)

    def by_role(self,role ,name):
        return self.page.get_by_role(role,name=name)

#------------
    def click_by_locator(self,locator_path,element_description):
        self.logger.info(f"{element_description} -> click_by_locator")
        element = self.by_locator(locator_path)
        self._click_opr(element)

    def click_by_role(self,role ,name ,element_description):
        self.logger.info(f"{element_description} -> click_by_role")
        element = self.by_role(role ,name)
        self._click_opr(element)

    def fill_by_locator(self,locator_path,value,element_description):
        self.logger.info(f"{element_description} -> fill_by_locator ,value : {value} ")
        element = self.by_locator(locator_path)
        self._fill_opr(element,value)

