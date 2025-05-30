from pages.base_page import BasePage  # Импорт базового класса, содержащего общие методы для работы со страницами
from locators.login_locators import LoginLocators  # Импорт локаторов, относящихся к странице входа (например, поля ввода, кнопки)
from locators.base_locators import BaseLocators  # Общие локаторы, которые могут использоваться на разных страницах

class LoginPage(BasePage):
    """Класс, представляющий страницу авторизации."""

    def enter_username(self, username, log_enabled=False):
        """Метод для ввода логина."""
        try:
            element = self.xpath.find_visible(LoginLocators.USERNAME_INPUT)
            element.clear()
            if log_enabled:
                self.logger.info("Поле логина очищено успешно.")

            element.send_keys(username)
            if log_enabled:
                self.logger.info(f"Логин '{username}' успешно введён.")

        except Exception as e:
            if log_enabled:
                self.logger.error(f"Ошибка при работе с полем логина: {e}")

    def enter_password(self, password, log_enabled=False):
        """Метод для ввода пароля."""
        try:
            element = self.xpath.find_visible(LoginLocators.PASSWORD_INPUT)
            element.clear()
            if log_enabled:
                self.logger.info("Поле пароля очищено успешно.")

            element.send_keys(password)
            if log_enabled:
                self.logger.info(f"Пароль '{password}' успешно введён.")

        except Exception as e:
            if log_enabled:
                self.logger.error(f"Ошибка при работе с полем пароля: {e}")

    def click_login(self, log_enabled=False):
        """Метод для нажатия кнопки входа."""
        try:
            self.xpath.find_clickable(LoginLocators.LOGIN_BUTTON).click()
            if log_enabled:
                self.logger.info("Кнопка 'Войти' нажата успешно.")

        except Exception as e:
            if log_enabled:
                self.logger.error(f"Ошибка при нажатии на кнопку 'Войти': {e}")

    def check_account_button(self, log_enabled=False):
        """Проверяет наличие кнопки 'Личный кабинет'."""
        try:
            element = self.xpath.find_located(BaseLocators.HEADER_ACCOUNT_BUTTON, timeout=5)
            if log_enabled:
                self.logger.info("Кнопка 'Личный кабинет' найдена.")
            return True

        except Exception:
            if log_enabled:
                self.logger.info("Кнопка 'Личный кабинет' отсутствует.")
            return False