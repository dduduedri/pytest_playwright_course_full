# Migration mapping

Translation tables from other frameworks into this one, plus a worked example.

Anything in a source test that has no row here needs a new wrapper method before the migration
continues. See the element-wrapper template in `SKILL.md`.

## Selenium, Python

| Selenium | This framework |
|---|---|
| `driver.get(url)` | page-object method with `self.page.goto(url, wait_until="domcontentloaded")` |
| `driver.find_element(By.XPATH, x)` | `self.page.locator(x)` |
| `driver.find_element(By.CSS_SELECTOR, c)` | `self.page.locator(c)` |
| `driver.find_element(By.ID, i)` | `self.page.locator(f"#{i}")` |
| `driver.find_elements(...)` | the same locator, matching many; narrow with `Filter` or `.nth(i)` |
| `.send_keys(value)` | `TextBox(loc, "desc").fill(value)` |
| `.send_keys(Keys.ENTER)` | `TextBox(loc, "desc").press_key("Enter")` |
| `.clear()` | `TextBox(loc, "desc").clear()` |
| `.click()` | `Button(loc, "desc").click()` |
| `.text` | `Text(loc, "desc").get_text()` |
| `.get_attribute(name)` | `ExpectValidation(loc, "desc").to_have_attribute(name, value)` when asserting |
| `.is_displayed()` | `ElementState(loc, "desc").is_visible()` |
| `.is_enabled()` | `ElementState(loc, "desc").is_enabled()` |
| `ActionChains(driver).move_to_element(el)` | `Button(loc, "desc").hover()` |
| `ActionChains(driver).drag_and_drop(a, b)` | `DragAndDrop(loc_a, "desc").drag_to(loc_b)` |
| `Select(el).select_by_visible_text(t)` | no wrapper yet, add a `Dropdown` class |
| `WebDriverWait(...).until(EC.visibility_of_element_located(...))` | `ElementState(loc, "desc").wait_visible()` |
| `WebDriverWait(...).until(EC.invisibility_of_element_located(...))` | `ElementState(loc, "desc").wait_hidden()` |
| `WebDriverWait(...).until(EC.presence_of_element_located(...))` | `ElementState(loc, "desc").wait_attached()` |
| `WebDriverWait(...).until(EC.element_to_be_clickable(...))` | `ExpectValidation(loc, "desc").to_be_enabled()` |
| `WebDriverWait(...).until(EC.url_contains(u))` | `PageState(page, "desc").wait_url(f"**{u}**")` |
| `assertEqual(el.text, expected)` | `ExpectValidation(loc, "desc").to_have_text(expected)` |
| `assertIn(expected, el.text)` | `ExpectValidation(loc, "desc").to_contain_text(expected)` |
| `assertTrue(el.is_displayed())` | `ExpectValidation(loc, "desc").to_be_visible()` |
| `time.sleep(n)` | a wait method, or delete it |
| `setUp` / `tearDown`, `driver.quit()` | the `context_setup` fixture, delete the source code |
| `unittest.TestCase` subclass | plain `test_*` function taking `context_setup` |
| implicit wait, `driver.implicitly_wait` | delete it, Playwright locators auto-wait |
| `requests.post(...)` for setup | a method on `APIUtils` in `utils/api_base.py` |

Selenium's explicit waits usually disappear entirely: Playwright locators auto-wait before every
action, so only keep a wait when the next step depends on something the locator cannot see.

## Cypress

| Cypress | This framework |
|---|---|
| `cy.visit(url)` | page-object method with `self.page.goto(url, wait_until="domcontentloaded")` |
| `cy.get(sel)` | `self.page.locator(sel)` |
| `cy.get(sel).type(v)` | `TextBox(loc, "desc").fill(v)`, or `.type(v)` to keep per-key typing |
| `cy.get(sel).clear()` | `TextBox(loc, "desc").clear()` |
| `cy.get(sel).type("{enter}")` | `TextBox(loc, "desc").press_key("Enter")` |
| `cy.get(sel).click()` | `Button(loc, "desc").click()` |
| `cy.get(sel).dblclick()` | `Button(loc, "desc").double_click()` |
| `cy.get(sel).rightclick()` | `Button(loc, "desc").right_click()` |
| `cy.get(sel).trigger("mouseover")` | `Button(loc, "desc").hover()` |
| `cy.contains(text)` | `self.page.get_by_text(text)` |
| `cy.get(sel).contains(text)` | `Filter(loc, "desc").has_text(text)` |
| `cy.get(sel).eq(i)` | `loc.nth(i)` |
| `cy.get(sel).invoke("text")` | `Text(loc, "desc").get_text()` |
| `.should("have.text", t)` | `ExpectValidation(loc, "desc").to_have_text(t)` |
| `.should("contain.text", t)` | `ExpectValidation(loc, "desc").to_contain_text(t)` |
| `.should("be.visible")` | `ExpectValidation(loc, "desc").to_be_visible()` |
| `.should("not.be.visible")` | `ExpectValidation(loc, "desc").not_to_be_visible()` |
| `.should("have.value", v)` | `ExpectValidation(loc, "desc").to_have_value(v)` |
| `.should("have.length", n)` | `ExpectValidation(loc, "desc").to_have_count(n)` |
| `.should("have.class", c)` | `ExpectValidation(loc, "desc").to_have_class(c)` |
| `.should("be.checked")` | `ExpectValidation(loc, "desc").to_be_checked()` |
| `.should("be.disabled")` | `ExpectValidation(loc, "desc").to_be_disabled()` |
| `cy.url().should("include", u)` | `PageState(page, "desc").wait_url(f"**{u}**")` |
| `cy.intercept` plus `cy.wait("@alias")` | `PageState(page, "desc").expect_response(url_part)` |
| `cy.request(...)` | a method on `APIUtils` in `utils/api_base.py` |
| `cy.fixture("products")` | `get_data("products")`, or the `product_data` fixture |
| `beforeEach` | the `context_setup` fixture, already automatic |
| `cy.wait(ms)` | a wait method, or delete it |
| custom command in `commands.js` | a page-object method, or an element wrapper if single-element |

Cypress chains collapse into one wrapper call: the subject becomes the locator argument and the
final command becomes the method.

## Raw Playwright, including pytest-playwright

The mechanics already match, so this is purely about routing calls through the wrappers.

| Raw Playwright | This framework |
|---|---|
| the built-in `page` fixture | `context_setup` |
| `page.goto(url)` | page-object method with `wait_until="domcontentloaded"` |
| `loc.fill(v)` | `TextBox(loc, "desc").fill(v)` |
| `loc.type(v)` | `TextBox(loc, "desc").type(v)` |
| `loc.press_sequentially(v)` | `TextBox(loc, "desc").press_sequentially(v)` |
| `loc.click()` | `Button(loc, "desc").click()` |
| `page.keyboard.press("Enter")` | `TextBox(loc, "desc").press_key("Enter")` on the focused input |
| `loc.text_content()` | `Text(loc, "desc").get_text()` |
| `loc.inner_text()` | `Text(loc, "desc").get_inner_text()` |
| `loc.filter(has_text=t)` | `Filter(loc, "desc").has_text(t)` |
| `loc.filter(has=other)` | `Filter(loc, "desc").has_locator(other)` |
| `loc.drag_to(target)` | `DragAndDrop(loc, "desc").drag_to(target)` |
| `expect(loc).to_have_text(t)` | `ExpectValidation(loc, "desc").to_have_text(t)` |
| any other `expect(loc)....` | the matching `ExpectValidation` method, or add it |
| `loc.wait_for(state="visible")` | `ElementState(loc, "desc").wait_visible()` |
| `loc.is_visible()` | `ElementState(loc, "desc").is_visible()` |
| `page.wait_for_load_state("networkidle")` | `PageState(page, "desc").wait_network_idle()` |
| `page.wait_for_url(u)` | `PageState(page, "desc").wait_url(u)` |
| `page.expect_response(...)` | `PageState(page, "desc").expect_response(url_part)` |
| `browser.new_context()` in the test | already handled by `context_setup` |

## Worked example

Source, a Selenium test doing everything in one function:

```python
def test_login_and_add_to_cart(self):
    driver.get("https://rahulshettyacademy.com/client/")
    driver.find_element(By.ID, "userEmail").send_keys("dudued@gmail.com")
    driver.find_element(By.ID, "userPassword").send_keys("Aa123456")
    driver.find_element(By.ID, "login").click()

    cards = driver.find_elements(By.CSS_SELECTOR, "div.card")
    for card in cards:
        if card.find_element(By.TAG_NAME, "h5").text == "ZARA COAT 3":
            card.find_element(By.XPATH, ".//button[text()='Add To Cart']").click()
            break

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "button.btn-custom label")))
    self.assertEqual(driver.find_element(By.CSS_SELECTOR, "button.btn-custom label").text, "1")
```

**Step 1, inventory.** Navigate and log in on the login page; find a card by name and add it to
cart, then confirm the badge, on the product page. Data: one user, one product name.

**Step 2 and 3.** Every action maps to an existing wrapper: `TextBox.fill`, `Button.click`,
`Filter.has_text` for the manual card loop, `ElementState.wait_visible`, and
`ExpectValidation.to_have_text`. No new wrapper methods needed.

**Step 4.** Both flows already exist as `LoginPage.login_goto`, `LoginPage.login`,
`ProductPage.add_product_to_cart`, and `ProductPage.check_cart_count`. Nothing to write.

**Step 5.** The user is already in `credentials.json` as `user_a`; the product is already in
`products.json` as `zara_coat`.

**Step 6, the migrated test:**

```python
# Login, add ZARA COAT 3 to the cart, and confirm the cart badge shows one item.
# user_a comes from data/ui_data/credentials.json; product_data loads data/ui_data/products.json.
@pytest.mark.smoke
@pytest.mark.parametrize("product_data", ["products"], indirect=True)
def test_login_and_add_to_cart(context_setup, product_data):
    user_list = get_credentials("user_a")
    product_name = product_data["zara_coat"]["productName"]

    my_page = context_setup
    LoginPage(my_page).login_goto()
    LoginPage(my_page).login(user_list["userEmail"], user_list["UserPassword"])
    ProductPage(my_page).add_product_to_cart(product_name)
    ProductPage(my_page).check_cart_count(1)
```

**Step 7.** The manual card loop, the explicit wait, and the `assertEqual` are gone: `Filter` plus
`ElementState.wait_visible` inside `add_product_to_cart` and `ExpectValidation.to_have_text` inside
`check_cart_count` already cover them. The migrated test is only ordering, which is the goal.
