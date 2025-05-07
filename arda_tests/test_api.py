import requests
import allure
from conftest import log_request_and_response

@allure.epic("Главная страница")
@allure.feature("Доступность страницы")
@allure.story("GET-запрос на / возвращает 200 OK")
@allure.severity(allure.severity_level.CRITICAL)
def test_main_page_is_available(base_url):
    url = f"{base_url}/"

    with allure.step("Отправка GET-запроса на главный endpoint"):
        response = requests.get(url)
        log_request_and_response(response)

    assert response.status_code == 200


@allure.epic("Обработка ошибок")
@allure.feature("Некорректные маршруты")
@allure.story("GET-запрос на несуществующий URL возвращает 404")
@allure.severity(allure.severity_level.NORMAL)
def test_page_not_found(base_url):
    url = f"{base_url}/blabla"

    with allure.step("Отправка GET-запроса на несуществующий endpoint"):
        response = requests.get(url)
        log_request_and_response(response)

    assert response.status_code == 404