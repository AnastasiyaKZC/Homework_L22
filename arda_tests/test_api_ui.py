import requests
import allure
from selene import Browser, have
from allure_commons.types import Severity
import time


@allure.epic("API + UI тесты")
@allure.feature("Авторизация по API проверка по UI")
@allure.story("Переход в ЛК")
@allure.severity(Severity.CRITICAL)
@allure.tag("auth", "api", "positive")
@allure.label("owner", "Kuznetsova")
def test_api_auth_then_ui_check(setup_browser: Browser, credentials, base_url):

    with allure.step("Запрос токена авторизации через API"):
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
        token = response.json().get("jwt")
        assert token is not None, "Токен не получен"

    with allure.step("Формирование mock-объекта пользователя"):
        user_json = '{"id":200,"username":"QA Анастасия","email":"' + credentials["identifier"] + '","provider":"local","name":"Анастасия","company":"тестQA","post":"QA","lastName":"Кузнецова","userRole":"Член ARDA", ...}'

    with allure.step("Установка токена и данных пользователя в localStorage"):
        setup_browser.open(base_url)
        setup_browser.driver.execute_script(
            f"window.localStorage.setItem('token', '{token}');"
            f"window.localStorage.setItem('user', '{user_json}');"
        )

    with allure.step("Переход в Личный кабинет"):
        setup_browser.open(f"{base_url}/account/main/")
        profile_link = setup_browser.element('a[href="/account/profile/"]')
        time.sleep(2)
        profile_link.click()

    with allure.step("Проверка отображения страницы 'Личный кабинет'"):
        time.sleep(2)
        setup_browser.element("body").should(have.text("Личный кабинет"))