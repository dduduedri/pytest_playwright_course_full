import pytest

from utils.data_reader import get_all_users, get_all_credentials , get_credentials, get_data


@pytest.fixture(scope="function")
def credentials_all() -> list[dict]:
    return get_all_users()

@pytest.fixture(scope="function")
def get_all_credentials_file() -> dict:
    return get_all_credentials()

@pytest.fixture(scope="function")
def credentials_user(user_name):
    return get_credentials(user_name)

@pytest.fixture(scope="function")
def product_data(request):
    return get_data(request.param)

@pytest.fixture(scope="function")
def payment_data(request):
    return get_data(request.param)

@pytest.fixture(scope="function")
def credentials_user_with_param(request):
    return get_credentials(request.param)