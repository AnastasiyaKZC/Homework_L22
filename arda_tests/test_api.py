import os

import requests
import allure
from conftest import log_request_and_response


@allure.epic("API тесты")
@allure.feature("Доступность страницы")
@allure.story("GET-запрос на / возвращает 200 OK")
@allure.severity(allure.severity_level.CRITICAL)
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
def test_page_not_found(base_url):
    url = f"{base_url}/blabla"

    with allure.step("Отправка GET-запроса на несуществующий endpoint"):
        response = requests.get(url)
        log_request_and_response(response)

    assert response.status_code == 404


@allure.epic("API тесты")
@allure.feature("Аутентификация")
@allure.story("POST-запрос с неверным паролем возвращает 400 Bad Request")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_with_invalid_password(base_url, credentials):
    url = f"{base_url}/api/users/verify"
    payload = {
        "identifier": credentials["identifier"],
        "password": "wrong_password"  # специально неверный пароль
    }

    with allure.step("Отправка POST-запроса с неверным паролем"):
        response = requests.post(url, json=payload)
        log_request_and_response(response)

    assert response.status_code == 400


@allure.epic("API тесты")
@allure.feature("Аутентификация")
@allure.story("POST-запрос с верными кредами возвращает 200 ОК")
@allure.severity(allure.severity_level.CRITICAL)
def test_successful_login(base_url, credentials):
    url = f"{base_url}/api/users/verify"
    payload = {
        "identifier": credentials["identifier"],
        "password": credentials["password"]
    }

    with allure.step("Отправка POST-запроса для авторизации с валидными данными"):
        response = requests.post(url, json=payload)
        log_request_and_response(response)

    assert response.status_code == 200
