import allure
from selene import be

class MainPage:
    def __init__(self, browser):
        self.browser = browser  # ✅ Используем переданный browser

    def should_have_user_menu(self):
        """Проверяем, что меню пользователя появилось после авторизации"""
        with allure.step("Проверяем наличие меню авторизованного пользователя"):
            self.browser.element('button.w-auto.flex.justify-center.align-middle').should(be.visible)