import requests
import allure
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

BASE_URL = "https://it.arda.digital"

@allure.epic("API")
@allure.feature("GET Main Page")
@allure.story("Check site availability")
def test_main_page_is_available():
    endpoint = "/"
    url = f"{BASE_URL}{endpoint}"

    with allure.step(f"GET {url}"):
        response = requests.get(url)

        allure.attach(
            name="Response body",
            body=response.text,
            attachment_type=allure.attachment_type.HTML
        )
        allure.attach(
            name="Status code",
            body=str(response.status_code),
            attachment_type=allure.attachment_type.TEXT
        )

    logging.info(f"{datetime.now()} — GET {url} — {response.status_code}")
    assert response.status_code == 200, "Ожидается статус 200 OK"