import requests
import allure
import pytest
from selene import Browser, have
from pages.main_page import MainPage
from allure_commons.types import Severity
from conftest import log_request_and_response


@allure.epic("API + UI тесты")
@allure.feature("Авторизация")
@allure.story("Успешная авторизация через API и проверка UI")
@allure.severity(Severity.CRITICAL)
@allure.tag("auth", "api", "ui", "positive")
@allure.label("owner", "Kuznetsova")
def test_api_auth_then_ui_check(setup_browser: Browser, credentials, base_url):
    with allure.step("Получаем токен через API /users/verify"):
        response = requests.post(
            f"{base_url}/api/users/verify",
            json={
                "identifier": credentials["identifier"],
                "password": credentials["password"]
            },
            headers={
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json",
                "Origin": base_url,
                "Referer": base_url + "/"
            }
        )
        response.raise_for_status()
        log_request_and_response(response)

        token = response.json().get("jwt")
        assert token, "❌ Не удалось получить токен из ответа"

    with allure.step("Авторизуемся через localStorage и открываем личный кабинет"):
        setup_browser.open(base_url)
        setup_browser.driver.execute_script(
            f"window.localStorage.setItem('accessToken', '{token}');"
        )
        setup_browser.open(f"{base_url}/account/main/")

    with allure.step("Кликаем на ссылку 'Профиль' и проверяем отображение 'Личный кабинет'"):
        profile_link = setup_browser.element('a[href="/account/profile/"]')
        profile_link.click()
        setup_browser.element("body").should(have.text("Личный кабинет"))