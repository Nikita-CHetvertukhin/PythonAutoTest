class BaseLocators:

    '''Licence.Properties'''

    # Путь до json с лицензиями
    LICENCE_PROPERTIES = '//script[@type="text/javascript" and contains(text(), "Licence.Properties")]'

    '''HEADER'''

    # Кнопка Лого DZ
    HEADER_LOGO_BUTTON = '//div[@class = "header"]/a[contains(@class, "logo")]'
    # Кнопки меню в Header
    HEADER_MENU_BUTTONS = '//div[contains(@class, "header-menu")]//a[contains(@class, "btn")]'
    # Выпадающий список при нажатии на кнопку из меню в Header
    HEADER_DROPDOWN_LIST = '//div[contains(@class, "dropdown") and not(contains(@class, "display-none"))]'
    # Инпут "Найти"
    HEADER_SEARCH_INPUT = '//div[@class = "header"]/div[contains(@class, "content")]/a[contains(@class, "search")]'
    # Кнопка "Помощь"
    HEADER_HELP_BUTTON = '//div[@class = "header"]/div[contains(@class, "content")]/a[contains(@class, "help")]'
    # Кнопка личного кабинета
    HEADER_ACCOUNT_BUTTON = '//div[@class="header"]//div[@class="content"]/a[contains(@class, "user")]'

    '''ACCOUNT'''

    # Кнопка "Выйти"
    ACCOUNT_SIGNOUT = '//div[contains(@class, "account-panel")]//a[contains(@class, "sign-out")]'

    '''SIDE MENU'''
    # Кнопки бокового меню
    SIDE_MENU_BUTTONS = '//div[@class="body"]/div[not(contains(@class, "display-none"))]/div[contains(@class, "header") and contains(@class, "radio")]/a[not(contains(@class, "display-none"))]'

    '''ERRORS'''

    # Окно ошибки error dzmessage (красная всплывающая) без привязки к конкретному текусту ошибки
    ERROR_NOTIFICATION = '//div[contains(@class, "error")]'
    # Закрытие любого окна ошибки error dzmessage (красная всплывающая)
    ERROR_CLOSE = '//div[contains(@class, "error")]//a[contains(@class, "close")]'