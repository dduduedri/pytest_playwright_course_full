---
name: playwright-framework-authoring
description: Write new tests, page objects, and element wrappers for this pytest + Playwright framework, and port tests into it from Selenium, Cypress, or raw Playwright. Use when adding or changing anything under ui/elements/, ui/pages/, fixtures/, utils/, or test_*.py files, or when the user mentions migrating, porting, or converting existing tests into this framework.
---

# Authoring in this pytest + Playwright framework

## Architecture

Four layers, each with one job. Code belongs in the lowest layer that can own it.

| Layer | Path | Owns |
|-------|------|------|
| Element wrappers | `ui/elements/` | One interaction with one locator, plus logging |
| Page objects | `ui/pages/` | Locators and business flows for one page |
| Data and API | `utils/`, `data/ui_data/`, `fixtures/` | JSON test data, API steps, pytest fixtures |
| Tests | `test_*.py` at repo root | Ordering page-object calls, nothing else |

Element wrappers all subclass `BaseElements(locator, element_description)`. `PageState` is the
exception: it takes a `Page`, not a `Locator`, because its waits are not tied to one element.

There are no `__init__.py` files; imports work as namespace packages from the repo root.

## Golden rules

1. **No raw Playwright actions outside `ui/elements/`.** Tests and page objects never call
   `.click()`, `.fill()`, `.wait_for()`, or `expect()` directly. If no wrapper method fits, add one
   to the right element class instead of reaching around it.
2. **No selectors in tests.** Locators are built inside page objects with `self.page.locator(...)`.
3. **Every wrapper call gets a description.** It is the log line, so write it as action plus target:
   `"Fill User Name"`, `"click Buy Now"`, `"Cart Count"`.
4. **Keep the raw Playwright line as a comment above the wrapped call.** This repo teaches the
   mapping, so the original stays visible:

```python
# my_page.get_by_role("button",name="Login").click()
Button(self.page.get_by_role("button", name="Login"), "click Login").click()
```

5. **Assertions go through `ExpectValidation`**, never a bare `assert` on UI state. It retries;
   `assert` does not. Text assertions take strings, so cast: `to_have_text(str(count))`.
6. **Wait in this order of preference:** `ExpectValidation` (assert and wait at once) →
   `ElementState` (element appears, disappears, attaches) → `PageState` (URL, load state, response).
   Never add `sleep()` to a page object or wrapper. The `sleep(5)` at the end of existing tests is
   only there to keep the browser visible.
7. **Test data comes from `data/ui_data/*.json`** through `utils/data_reader.py` or a fixture in
   `fixtures/data_fixtures.py`. No credentials or product IDs invented inline in new tests.
8. **Register every marker in `pytest.ini`** before using it.
9. **Navigate through `BasePage.navigate(url)`**, never a bare `page.goto`. It retries once when
   the demo app aborts or stalls the first request under parallel load. The default
   `wait_until="domcontentloaded"` returns as soon as the HTML shell is parsed, which is before
   Angular has rendered anything, so pass `wait_until="load"` with a longer `timeout` when the next
   step needs rendered UI, as `LoginPage.login_goto` does.

## Where does this code go?

| The step you are adding | Put it in |
|---|---|
| Click, hover, key press | `ui/elements/button.py` (`Button`) |
| Fill, type, clear an input | `ui/elements/text_box.py` (`TextBox`) |
| Read text off the page | `ui/elements/text.py` (`Text`) |
| Narrow a list of matches | `ui/elements/filter.py` (`Filter`, returns a `Locator`) |
| Assert anything about an element | `ui/elements/expect_validation.py` (`ExpectValidation`) |
| Wait for or query element state | `ui/elements/element_state.py` (`ElementState`) |
| Wait for URL, load state, response | `ui/elements/page_state.py` (`PageState`) |
| Drag an element onto another | `ui/elements/drag_and_drop.py` (`DragAndDrop`) |
| Open a URL | `self.navigate(url)`, inherited from `ui/pages/base_page.py` |
| A multi-step flow on one page | a page object in `ui/pages/` |
| An HTTP-only step | `utils/api_base.py` (`APIUtils`) |

No wrapper for dropdowns, checkboxes, file inputs, tables, or dialogs exists yet. Adding one is
expected work, not a workaround; use the element-wrapper template below.

## Workflow: new development

1. Read the closest existing sibling first and copy its shape (`ui/pages/login_page.py` for a small
   page, `ui/pages/create_product_order_page.py` for a page with waits and assertions).
2. Add any missing element-wrapper methods, one interaction per method.
3. Add or extend the page object with business-level methods that read like the test steps.
4. Move data into `data/ui_data/*.json` and expose it with a fixture if the test needs parametrizing.
5. Write the test: get the page from `context_setup`, then call page objects only.
6. Run it and read the live log. Every UI step should produce a line; a silent step means something
   bypassed the wrappers.

### Templates

New element wrapper, `ui/elements/<family>.py`:

```python
from ui.elements.base_element import BaseElements


class Dropdown(BaseElements):

    def select_by_label(self, label: str, timeout: int | None = None):
        """Selects the option with the given visible label."""
        self.logger.info(f"[ select_by_label: {label} ] -> {self.element_description}")
        self.locator.select_option(label=label, timeout=timeout)
```

Every method: docstring, one `self.logger.info(f"[ action ] -> {self.element_description}")`, then
delegate to the locator, with `timeout: int | None = None` as the last parameter.

New page object, `ui/pages/<page>_page.py`:

```python
from ui.elements.button import Button
from ui.elements.expect_validation import ExpectValidation
from ui.elements.text_box import TextBox
from ui.pages.base_page import BasePage


class CheckoutPage(BasePage):

    def apply_coupon(self, coupon_code):
        # my_page.locator("//input[@class='promoCode']").fill(coupon_code)
        TextBox(self.page.locator("//input[@class='promoCode']"), "Fill Coupon Code").fill(coupon_code)

        # my_page.locator("//button[@class='promoBtn']").click()
        Button(self.page.locator("//button[@class='promoBtn']"), "click Apply Coupon").click()

        # expect(my_page.locator("//span[@class='promoInfo']")).to_have_text("Code applied ..!")
        ExpectValidation(self.page.locator("//span[@class='promoInfo']"), "Coupon Message").to_have_text("Code applied ..!")
```

New test, at repo root:

```python
# One-line intent, then which data source and fixture feed it.
@pytest.mark.smoke
@pytest.mark.parametrize("product_data", ["products"], indirect=True)
def test_e2e_full_ui_apply_coupon(context_setup, product_data):
    user_list = get_credentials("user_a")
    product_name = product_data["zara_coat"]["productName"]

    my_page = context_setup
    LoginPage(my_page).login_goto()
    LoginPage(my_page).login(user_list["userEmail"], user_list["UserPassword"])
    ProductPage(my_page).add_product_to_cart(product_name)
    CheckoutPage(my_page).apply_coupon("rahulshettyacademy")
```

Every test carries a comment above it stating what it covers and where its data comes from, matching
`test_e2e_framework_ui_base_elements_oop_5.py`.

## Workflow: migration from another framework

Migrate one test at a time, bottom-up. Do not translate line by line into the test file.

```
Migration progress:
- [ ] Step 1: Inventory the source test
- [ ] Step 2: Convert selectors
- [ ] Step 3: Fill wrapper gaps
- [ ] Step 4: Build page objects
- [ ] Step 5: Externalize data
- [ ] Step 6: Write the test
- [ ] Step 7: Run and check the log
```

**Step 1: Inventory.** List the source test's actions, assertions, waits, and hardcoded data. Name
the pages it touches. This list becomes the page-object method list.

**Step 2: Convert selectors.** Prefer `get_by_role`, `get_by_placeholder`, or `get_by_text`; fall
back to XPath, which is what most of this repo uses. CSS-only frameworks translate directly:
`page.locator("div.card")`.

**Step 3: Fill wrapper gaps.** Map each source action to a wrapper method using
[migration.md](migration.md). Anything unmapped becomes a new method or a new element class first,
before any page object uses it.

**Step 4: Build page objects.** Group the inventory by page. Each source flow becomes one method,
named for the business outcome (`place_order`, `search_order_history`), not for the widgets.

**Step 5: Externalize data.** Hardcoded logins, product IDs, and payment details move to
`data/ui_data/*.json` and are read through `utils/data_reader.py`. Add a fixture only if the test
parametrizes over the data.

**Step 6: Write the test.** Setup and teardown come from `context_setup`; delete the source
framework's driver setup, base classes, and cleanup entirely.

**Step 7: Run and check the log.** Compare the emitted log lines against the Step 1 inventory. A
missing line means a step bypassed the wrappers; a raw Playwright call is the usual cause.

## Verify before finishing

- [ ] No `.click()`, `.fill()`, `.wait_for()`, `expect()`, or `sleep()` outside `ui/elements/`
- [ ] No selector strings in any `test_*.py`
- [ ] Every wrapper call has a description that reads as action plus target
- [ ] Each new wrapper method logs once and accepts `timeout`
- [ ] Raw Playwright equivalent left as a comment above each wrapped call
- [ ] UI assertions use `ExpectValidation`, with text values passed as strings
- [ ] New data lives in `data/ui_data/`, new markers in `pytest.ini`
- [ ] Test runs and every step appears in the live log

## Additional resources

- Full method catalog for every wrapper, page object, fixture, and CLI option: [reference.md](reference.md)
- Selenium, Cypress, and raw-Playwright mapping tables plus a worked conversion: [migration.md](migration.md)
- Run commands: `quick-run.md` at the repo root
