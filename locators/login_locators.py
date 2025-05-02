class LoginLocators:
    USERNAME_INPUT = '//input[contains(@autocomplete,"username")]'
    PASSWORD_INPUT = '//input[contains(@autocomplete,"password")]'
    LOGIN_BUTTON = '//a[contains(@class, "btn primary push")][span[text()]]'

    AUTH_ERROR = '//div[contains(@class, "error")]//span[text()="Неверный логин или пароль"]'