# import pytest
#
# @pytest.fixture(scope="session")
# def base_url():
#     return "https://it.arda.digital"


import pytest
import logging
import allure
from allure_commons.types import AttachmentType

# Настройка логирования
logger = logging.getLogger()
logger.setLevel(logging.INFO)
if not logger.handlers:
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

@pytest.fixture(scope="session")
def base_url():
    return "https://it.arda.digital"

def log_request_and_response(response):
    logger.info(f"Response Status Code: {response.status_code}")
    logger.info(f"Response Headers: {response.headers}")
    logger.info(f"Response Body (partial): {response.text[:200]}...")

    # Allure attachments
    allure.attach("Request URL", response.request.url, AttachmentType.TEXT)
    allure.attach("Request Method", response.request.method, AttachmentType.TEXT)
    allure.attach("Request Headers", str(response.request.headers), AttachmentType.TEXT)
    allure.attach("Response Status Code", str(response.status_code), AttachmentType.TEXT)
    allure.attach("Response Headers", str(response.headers), AttachmentType.TEXT)
    allure.attach("Response Body", response.text, AttachmentType.JSON)