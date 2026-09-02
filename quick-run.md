# Quick Run

From-scratch setup and execution, assuming a fresh clone with **no** `.venv` yet.
Commands are for **Windows PowerShell**.

The app under test is [https://rahulshettyacademy.com/client/](https://rahulshettyacademy.com/client/).
The browser is launched **headed** (`headless=False` in `conftest.py`).

## 1) One-time setup (from scratch after clone)

```powershell
# 0) Check Python is available (use the Windows launcher)
py --version

# 1) Create the virtual environment
py -m venv .venv

# 2) Activate it (prompt should now show "(.venv)")
.\.venv\Scripts\Activate.ps1
# If activation is blocked by execution policy, run PowerShell once as:
#   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 3) Upgrade pip and install Python dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 4) Install Playwright browsers
python -m playwright install chromium
python -m playwright install firefox

# 5) Verify pytest is on the venv
python -m pytest --version
```

> Already set up? Activate the venv (`.\.venv\Scripts\Activate.ps1`) and jump to step 2.

## 2) Run tests

Course files are numbered by framework style. Run from the repo root.

```powershell
# All tests
python -m pytest

# One course file
python -m pytest test_e2e_framework_ui_not_oop_not_base_elements_1.py
python -m pytest test_e2e_framework_ui_and_api_not_oop_not_base_element_2.py
python -m pytest test_e2e_framework_ui_base_elements_not_oop_3.py
python -m pytest test_e2e_framework_ui_base_elements_oop_4.py
python -m pytest test_e2e_framework_ui_base_elements_oop_5.py

# One test (example: oop_5 filter-cards) — chrome, headed (default)
python -m pytest test_e2e_framework_ui_base_elements_oop_5.py::test_e2e_full_ui_filter_cards
pytest --browser_name chrome -m smoke -n auto --headless True --tracing on --video on --clean-alluredir
pytest --browser_name chrome -m smoke -n auto --headless False 

# Same test on Firefox
python -m pytest test_e2e_framework_ui_base_elements_oop_5.py::test_e2e_full_ui_filter_cards --browser_name firefox

# Same test headless (no browser window)
python -m pytest test_e2e_framework_ui_base_elements_oop_5.py::test_e2e_full_ui_filter_cards --headless True
python -m pytest test_e2e_framework_ui_base_elements_oop_5.py::test_e2e_full_ui_filter_cards --browser_name firefox --headless True
```

| File | What it covers |
|---|---|
| `test_e2e_framework_ui_not_oop_not_base_elements_1.py` | Raw Playwright: filter cards + search, then checkout |
| `test_e2e_framework_ui_and_api_not_oop_not_base_element_2.py` | Hybrid: create order via API, open it in UI history |
| `test_e2e_framework_ui_base_elements_not_oop_3.py` | Same flows with `TextBox` / `Button` / `Filter` / `ExpectValidation` |
| `test_e2e_framework_ui_base_elements_oop_4.py` | Same flows with page objects (`LoginPage`, `ProductPage`, …) |
| `test_e2e_framework_ui_base_elements_oop_5.py` | Page objects + data fixtures / parametrize from JSON |

## 3) Data and fixtures

Test users and catalog data live under `data/ui_data/`:

- `credentials.json` — `user_a`, `user_b`
- `products.json` — product name / id (used by `product_data`)
- `payments.json` — CVV / country (used by `payment_data`)

Shared fixtures are **not** in `conftest.py`. They are loaded automatically via:

```python
pytest_plugins = (
    "fixtures.data_fixtures",
)
```

That imports `fixtures/data_fixtures.py`, so tests can request `product_data`, `payment_data`, `credentials_user`, and `credentials_user_with_param` without importing the module.

Browser fixtures stay in `conftest.py`:

- `--browser_name` — `chrome` (default) or `firefox`
- `--headless` — `True` or `False` (default `False` = headed)
- `browser_setup` — one browser per session
- `context_setup` — a fresh context + page per test (this is the Playwright `page` the tests use)

## 4) Optional reports

`requirements.txt` includes pytest-html and allure-pytest. They are not required to run tests.

```powershell
# HTML report
python -m pytest test_e2e_framework_ui_base_elements_oop_5.py --html=reports/report.html --self-contained-html

# Allure results (needs the Allure CLI to view)
python -m pytest test_e2e_framework_ui_base_elements_oop_5.py --alluredir=reports/allure-results
allure serve reports/allure-results
```
