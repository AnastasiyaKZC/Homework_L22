import pytest

@pytest.fixture(scope="session")
def base_url():
    return "https://it.arda.digital"