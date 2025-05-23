import json

import requests
import allure
from conftest import log_request_and_response
from jsonschema import validate


@allure.epic("API тесты")
@allure.feature("Доступность страницы")
@allure.story("GET-запрос на / возвращает 200 OK")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "availability")
@allure.label("owner", "Kuznetsova")
def test_main_page_is_available(base_url):
    url = f"{base_url}/"

    with allure.step("Отправка GET-запроса на главный endpoint"):
        response = requests.get(url)
        log_request_and_response(response)

    assert response.status_code == 200


@allure.epic("API тесты")
@allure.feature("Некорректные маршруты")
@allure.story("GET-запрос на несуществующий URL возвращает 404")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "routing")
@allure.label("owner", "Kuznetsova")
def test_page_not_found(base_url):
    url = f"{base_url}/blabla"

    with allure.step("Отправка GET-запроса на несуществующий endpoint"):
        response = requests.get(url)
        log_request_and_response(response)

    assert response.status_code == 404


from schemas import ERROR_LOGIN_SCHEMA
@allure.epic("API тесты")
@allure.feature("Аутентификация")
@allure.story("POST-запрос с неверным паролем возвращает 400 Bad Request")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "auth")
@allure.label("owner", "Kuznetsova")
def test_login_with_invalid_password(base_url, credentials):
    url = f"{base_url}/api/users/verify"
    payload = {
        "identifier": credentials["identifier"],
        "password": "wrong_password"  # специально неверный пароль
    }

    with allure.step("Отправка POST-запроса с неверным паролем"):
        response = requests.post(url, json=payload)
        log_request_and_response(response)
        body = response.json()

    assert response.status_code == 400
    validate(body, ERROR_LOGIN_SCHEMA)  # Проверяем схему
    assert "Введен неверный пароль" in body["error"]["message"]

    allure.attach(
        json.dumps(ERROR_LOGIN_SCHEMA, indent=2),
        name="Expected Error Schema",
        attachment_type=allure.attachment_type.JSON
    )


from schemas import SUCCESS_LOGIN_SCHEMA
@allure.epic("API тесты")
@allure.feature("Аутентификация")
@allure.story("POST-запрос с верными кредами возвращает 200 ОК")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "auth")
@allure.label("owner", "Kuznetsova")
def test_successful_login(base_url, credentials):
    url = f"{base_url}/api/users/verify"
    payload = {
        "identifier": credentials["identifier"],
        "password": credentials["password"]
    }

    with allure.step("Отправка POST-запроса для авторизации с валидными данными"):
        response = requests.post(url, json=payload)
        log_request_and_response(response)
        response_data = response.json()

    assert response.status_code == 200
    validate(response_data, SUCCESS_LOGIN_SCHEMA)

    allure.attach(
        json.dumps(SUCCESS_LOGIN_SCHEMA, indent=2),
        name="Expected Schema",
        attachment_type=allure.attachment_type.JSON
    )


@allure.epic("API тесты")
@allure.feature("Редиректы")
@allure.story("GET-запрос на http:// редиректит на https://")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "redirect")
@allure.label("owner", "Kuznetsova")
def test_http_redirect_to_https():
    url = "http://it.arda.digital"

    with allure.step("Отправка GET-запроса по HTTP без следования редиректу"):
        response = requests.get(url, allow_redirects=False)
        log_request_and_response(response)

    assert response.status_code in [301, 302], "Ожидается редирект"
    assert response.headers.get("Location", "").startswith("https://"), "Ожидается редирект на HTTPS"