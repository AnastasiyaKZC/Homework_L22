import allure
from selene import have, be
import allure
from pages.auth_page import AuthPage
from pages.main_page import MainPage
from selene import be

@allure.epic("UI тесты")
@allure.feature("Лендинг")
@allure.story("Логотип должен отображаться в хедере")
@allure.severity(allure.severity_level.NORMAL)
def test_logo_is_visible(setup_browser):
    with allure.step("Открываем главную страницу"):
        setup_browser.open("https://it.arda.digital")
    with allure.step("Проверяем наличие изображения с логотипом в хедере"):
        setup_browser.element("header img").should(have.attribute("src"))


@allure.epic("UI тесты")
@allure.feature("Лендинг")
@allure.story("Форма регистрации должна открываться по клику на кнопку")
@allure.severity(allure.severity_level.CRITICAL)
def test_registration_form_opens(setup_browser):
    with allure.step("Открываем главную страницу"):
        setup_browser.open("https://it.arda.digital")
    with allure.step("Кликаем на кнопку регистрации"):
        setup_browser.element(
            "span.w-full.relative.inline-block.px-8.py-3.text-sm.font-bold.tracking-widest.text-black.uppercase.border-2.border-current.group-active\\:text-opacity-75"
        ).click()
    with allure.step("Проверяем, что форма регистрации отображается"):
        setup_browser.element("form").should(be.visible)


@allure.epic("UI тесты")
@allure.feature("Лендинг")
@allure.story("Переход по ссылке arda.digital")
@allure.severity(allure.severity_level.NORMAL)
def test_learn_more_link(setup_browser):
    with allure.step("Открываем главную страницу"):
        setup_browser.open("https://it.arda.digital")
    with allure.step("Скроллим в конец страницы"):
        setup_browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    with allure.step("Кликаем на кнопку 'Подробнее'"):
        setup_browser.element("#app > div > div > div > div:nth-child(10) > div.text-center > a").should(be.visible).click()
    with allure.step("Переключаемся на новую вкладку и проверяем URL"):
        setup_browser.switch_to_next_tab()
        setup_browser.should(have.url("https://arda.digital/"))

@allure.epic("UI тесты")
@allure.feature("Форма авторизации")
@allure.story("Проверка отправки пустой формы")
@allure.severity(allure.severity_level.CRITICAL)
def test_empty_auth_form(setup_browser):
    auth_page = AuthPage(setup_browser)  # ✅ Передаем browser в AuthPage
    (
        auth_page.open()
        .open_auth_form()
        .submit()
    )
    # Проверяем, что отображаются ошибки ввода
    setup_browser.element("span.text-red").should(be.visible)  # ✅ Используем setup_browser

@allure.epic("UI тесты")
@allure.feature("Форма авторизации")
@allure.story("Пользователь вводит неверный логин")
@allure.severity(allure.severity_level.NORMAL)
def test_invalid_login(setup_browser):
    auth_page = AuthPage(setup_browser)
    (
        auth_page.open()
        .open_auth_form()
        .enter_email("wrong@arda.digital")  # ❌ Неверный логин
        .enter_password("111111")  # ✅ Верный пароль
        .submit()
    )
    # Проверяем, что отображается ошибка авторизации
    setup_browser.element(".text-red").should(be.visible)

@allure.epic("UI тесты")
@allure.feature("Форма авторизации")
@allure.story("Пользователь вводит неверный пароль")
@allure.severity(allure.severity_level.NORMAL)
def test_invalid_password(setup_browser):
    auth_page = AuthPage(setup_browser)
    (
        auth_page.open()
        .open_auth_form()
        .enter_email("member@arda.digital")  # ✅ Верный логин
        .enter_password("wrongpassword")  # ❌ Неверный пароль
        .submit()
    )
    # Проверяем, что отображается ошибка авторизации
    setup_browser.element(".text-red").should(be.visible)

@allure.epic("UI тесты")
@allure.feature("Форма авторизации")
@allure.story("Пользователь успешно авторизуется")
@allure.severity(allure.severity_level.CRITICAL)
def test_successful_authorization_2(setup_browser, auth_credentials):
    auth_page = AuthPage(setup_browser)
    main_page = MainPage(setup_browser)
    (
        auth_page.open()
        .open_auth_form()
        .enter_email(auth_credentials["email"])
        .enter_password(auth_credentials["password"])
        .submit()
    )
    main_page.should_have_user_menu()