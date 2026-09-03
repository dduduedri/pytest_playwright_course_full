# Framework reference

Catalog of what already exists. Check here before writing a new method.

## Element wrappers

All live in `ui/elements/` and subclass `BaseElements`, constructed as
`Wrapper(locator, element_description)`.

`BaseElements` sets `self.locator`, `self.element_description`, `self.default_timeout = 10000`, and
`self.logger`, named `<module>.<ClassName>` so log lines identify the wrapper.

### Timeout behaviour

Two different defaults, worth knowing when a step flakes:

- `ElementState` and `PageState` fall back to `self.default_timeout` (10s) when `timeout` is `None`.
- `Button`, `TextBox`, `Text`, `Filter`, `DragAndDrop`, and `ExpectValidation` pass `None` straight
  to Playwright, so they use Playwright's own defaults (30s for actions, 5s for `expect`). Pass an
  explicit timeout when a step needs longer, as `check_cart_count` does with `timeout=10000`.

### Button

`click`, `double_click`, `right_click`, `hover`, `press_key(key)`

### TextBox

`fill(value)`, `type(value)`, `clear`, `press_key(key)`, `press_sequentially(value, delay=None)`

### Text

`get_text()` returns `text_content()` or `""`. `get_inner_text()` returns `inner_text()` or `""`.
Both log the extracted value.

### Filter

Returns a `Locator` rather than acting, so the result is fed into another wrapper.

- `has_text(text)` → `locator.filter(has_text=text)`
- `has_locator(locator)` → `locator.filter(has=locator)`

```python
product_element = Filter(self.page.locator("//div[@class='card']"), "Product Cards").has_text(product_name)
Button(product_element.get_by_role("button", name="Add To Cart"), f"Add {product_name} To Cart").click()
```

### ExpectValidation

Wraps Playwright's auto-retrying `expect`. Text arguments must be strings.

`to_have_text`, `to_contain_text`, `to_be_visible`, `to_be_hidden`, `to_be_enabled`,
`to_be_disabled`, `to_have_value`, `to_have_count`, `to_have_attribute(name, value)`,
`to_have_class`, `to_be_checked`, `not_to_be_visible`, `not_to_have_text`

### ElementState

Waits and instant state queries for one element.

- Waits: `wait_visible`, `wait_hidden`, `wait_attached`, `wait_detached`
- Instant, no retry: `is_visible()`, `is_hidden()`, `is_enabled()`

Use `ExpectValidation` when the state is the thing being verified; use `ElementState` when the wait
is only there to stabilize the next step.

### PageState

Constructed as `PageState(page, page_description)`, not from a locator.

- `wait_dom_loaded`, `wait_page_loaded`, `wait_network_idle`, `wait_url(url)`
- `expect_response(url_part)` returns a context manager; wrap the triggering action:

```python
with PageState(self.page, "Add To Cart").expect_response("add-to-order") as response:
    Button(add_to_cart_locator, "click Add To Cart").click()
print(response.value.status)
```

### DragAndDrop

`drag_to(target: Locator)`

## Page objects

All in `ui/pages/`, subclassing `BasePage`, which stores `self.page`. Instantiated per call in
tests: `LoginPage(my_page).login(...)`.

`BasePage` also provides `navigate(url, wait_until="domcontentloaded", timeout=None)`, the only
place any page object should call `goto`. It logs each attempt and retries once on the two ways the
demo app fails a first navigation under parallel load: `net::ERR_ABORTED` when it cancels the main
frame request, and a `goto` timeout when the request stalls instead. Both leave the tab at
`about:blank`, so a fresh `goto` is safe. Every other Playwright error propagates on the first
attempt. Raise `self.navigate_attempts` if one retry proves insufficient, keeping in mind that a
genuinely unreachable site then costs `attempts * timeout` before the test reports.

| Class | File | Methods |
|---|---|---|
| `LoginPage` | `login_page.py` | `login_goto()`, `login(user_name, user_password)` |
| `ProductPage` | `create_product_order_page.py` | `filter_product_element(product_name)`, `search_product(product_name)`, `add_product_to_cart(product_name)`, `check_cart_count(count)` |
| `CartPage` | `cart_page.py` | `check_and_buy_ordered_product_in_cart(product_name, product_id)` |
| `OrderPaymentPage` | `order_payement_page.py` | `place_order(cvv, country)` returns the order id |
| `OrderHistory` | `order_history.py` | `search_order_history(order_id)` |

`login_goto()` is just `self.navigate(...)`; copy that shape for any new navigation method. It
overrides the default with `wait_until="load", timeout=60000`, because the login form only exists
once the Angular bundles have arrived and parallel runs starve that download.
`ui/componenets/` is empty and reserved for composite components.

## Fixtures

`conftest.py` registers `fixtures/data_fixtures.py` through `pytest_plugins`, so its fixtures are
available everywhere without importing:

```python
pytest_plugins = (
    "fixtures.data_fixtures",
)
```

### Browser fixtures, `conftest.py`

- `browser_setup`, session scope. Launches chromium or firefox based on `--browser_name`, headless
  based on `--headless`, and closes the browser at the end of the session.
- `context_setup`, function scope. Creates a fresh context and page per test, yields the `Page`, and
  closes the context. **This is the fixture every UI test takes.**

A fresh context per test means no cookies or storage leak between tests, and no manual cleanup.

### Data fixtures, `fixtures/data_fixtures.py`

| Fixture | Returns | Usage |
|---|---|---|
| `credentials_all` | list of user dicts | direct |
| `get_all_credentials_file` | whole credentials dict, keyed `user_a` / `user_b` | direct |
| `credentials_user` | one user, requires a `user_name` fixture in scope | direct |
| `credentials_user_with_param` | one user by key | `parametrize(..., indirect=True)` |
| `product_data` | a JSON file from `data/ui_data/` | `parametrize(..., indirect=True)` |
| `payment_data` | a JSON file from `data/ui_data/` | `parametrize(..., indirect=True)` |

`product_data` and `payment_data` both call `get_data(request.param)`, so the param is a file name
without the extension: `["products"]` loads `data/ui_data/products.json`.

## Data

`utils/data_reader.py`, all reading from `data/ui_data/`:

- `get_credentials(user)` → one user dict from `credentials.json`
- `get_all_users()` → list of every user dict, used to parametrize logins
- `get_all_credentials()` → the whole `credentials.json` dict
- `get_data(file_name)` → `data/ui_data/<file_name>.json`

Paths are relative to the repo root, so pytest must run from there.

Current files and shapes:

```json
// credentials.json
{ "user_a": { "userEmail": "...", "UserPassword": "..." } }

// products.json
{ "zara_coat": { "productName": "ZARA COAT 3", "productID": "6960eac0c941646b7a8b3e68" } }

// payments.json
{ "credit": { "cvv": "123", "country": "India" } }
```

Note the inconsistent casing in `credentials.json`: `userEmail` but `UserPassword`. Match the file,
and keep new keys camelCase.

## API steps

`utils/api_base.py` holds `APIUtils`, built on `playwright.request.new_context(base_url=BASE_URL, ignore_https_errors=True)`:

- `get_token(playwright, user_cred)` → auth token
- `create_order(playwright, user_cred, product_id, country)` → order id

Both assert `response.ok` with the status and body in the message. Tests that need API setup take
the `playwright` fixture alongside `context_setup`, as `test_e2e_full_hybrid_order_created_by_api`
does. New API methods follow the same shape: build payload, post, assert `response.ok`, return the
piece the test needs.

## Configuration and running

`pytest.ini`:

```ini
[pytest]
log_cli = true
log_cli_level = INFO
log_cli_format = %(asctime)s - %(levelname)s - %(name)s - %(message)s
markers =
    smoke: quick smoke suite
```

`log_cli` is why wrapper logging is the framework's main debugging tool. Add new markers under
`markers` to avoid `PytestUnknownMarkWarning`.

Custom CLI options, both from `pytest_addoption` in `conftest.py`:

- `--browser_name`, `chrome` or `firefox`, default `chrome`
- `--headless`, the string `True` or `False`, default `False`. It takes a value, so
  `--headless True`, not a bare `--headless`.

```bash
python -m pytest test_e2e_framework_ui_base_elements_oop_5.py --browser_name firefox --headless True
python -m pytest -m smoke
```

Tracing and video capture are not implemented. `pytest-playwright` accepts `--tracing` and
`--video`, but they only apply to its own `page` and `context` fixtures, and this framework builds
its own context in `context_setup`, so the flags are silently ignored. Wiring them up means adding
`record_video_dir` or `context.tracing.start(...)` to `context_setup`.

Reporting works only at the plugin level: `--html=reports/report.html --self-contained-html` and
`--alluredir=reports/allure-results` produce results, but there are no Allure steps or attachments
in the wrappers, so the reports show pytest outcomes rather than the step log.

Parallel runs with `pytest-xdist` (`-n auto`) stress the public demo app and cause
`net::ERR_ABORTED` and timeouts on `goto`, plus cart badges that never update. Lower the worker
count before treating such failures as product bugs. See `quick-run.md` for the full run matrix.
