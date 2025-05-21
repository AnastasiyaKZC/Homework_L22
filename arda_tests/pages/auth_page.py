import allure
from selene import be

class AuthPage:
    def __init__(self, browser):
        self.browser = browser  # ✅ Используем переданный browser

    def open(self):
        """Открываем страницу авторизации"""
        with allure.step("Открываем страницу https://it.arda.digital"):
            self.browser.open("https://arda.ws-dev.ru/")  # ✅ Используем self.browser
        return self

    def open_auth_form(self):
        """Нажимаем кнопку для открытия формы авторизации"""
        with allure.step("Открываем форму авторизации"):
            self.browser.element('button.px-4.py-2.mr-5.font-bold').click()
        return self

    def enter_email(self, email):
        """Вводим логин"""
        with allure.step(f"Вводим логин: {email}"):
            self.browser.element('#email').set_value(email)
        return self

    def enter_password(self, password):
        """Вводим пароль"""
        with allure.step("Вводим пароль"):
            self.browser.element('[placeholder="Введите пароль"]').set_value(password)
        return self

    def submit(self):
        """Отправляем форму авторизации"""
        with allure.step("Отправляем форму"):
            self.browser.element('[type="submit"]').click()
        return self