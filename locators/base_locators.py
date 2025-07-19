class BaseLocators:

    '''Licence.Properties'''

    # Путь до json с лицензиями
    LICENCE_PROPERTIES = '//script[@type="text/javascript" and contains(text(), "Licence.Properties")]'

    '''HEADER'''

    # Кнопка Лого DZ
    HEADER_LOGO_BUTTON = '//div[contains(@class,"header")]/div[contains(@class,"logo")]/button[1]'
    # Кнопка выпадашки Doczilla Pro
    HEADER_DOCZILLA_BUTTON = '//div[contains(@class,"header")]/div[contains(@class,"logo")]/button[2]'
    # Кнопки меню в Header
    HEADER_MENU_BUTTONS = '//div[contains(@class, "entry-buttons")]/button'
    # Выпадающий список при нажатии на кнопку из меню в Header или выпадашку Doczilla Pro
    HEADER_DROPDOWN_LIST = '//div[not(contains(@class,"display-none"))and contains(@class,"x-popup")]/div[contains(@class,"menu")]'
    # Название отвкрытого процесса или документа вместо строки поиска
    HEADER_FILENAME = '//div[contains(@class,"content")]/div[contains(@class,"edit")]/input'
    # Инпут "Найти"
    HEADER_SEARCH_INPUT = '//div[@class = "header"]/div[contains(@class, "content")]/a[contains(@class, "search")]'
    # Кнопка "Помощь"
    HEADER_HELP_BUTTON = '//div[@class = "header"]/div[contains(@class, "content")]/a[contains(@class, "help")]'
    # Кнопка личного кабинета
    HEADER_ACCOUNT_BUTTON = '//div[contains(@class,"header")]/div[contains(@class,"commands")]/button[contains(@class,"account")]/label[not(contains(@class,"display-none"))]'


    '''ACCOUNT'''

    # Кнопка "Выйти"
    ACCOUNT_SIGNOUT = '//div[contains(@class, "account-panel")]//div[contains(@class, "sign-out")]'

    '''SIDE MENU'''

    # Кнопки бокового меню
    SIDE_MENU_BUTTONS = '//div[contains(@class,"body")]/div[not(contains(@class, "display-none"))]/div[contains(@class, "header") and contains(@class, "radio")]/a[not(contains(@class, "display-none"))]'

    '''BODY'''

    # Путь до TEXTAREA для ввода названия процесса/документа (например при переименовании)
    BODY_TEXTAREA = '//div[contains(@class,"textarea")]/div/textarea'

    '''DIALOG WINDOW'''
    # Кнопка подтвердить действие в диалоговом окне
    DIALOG_WINDOW_CONFIRM = '//div[contains(@class,"dialog")]/div[contains(@class,"footer")]/a[contains(@class,"primary")]/span'
    # Кнопка отменить действие в диалоговом окне
    DIALOG_WINDOW_CANCEL = '//div[contains(@class,"dialog")]/div[contains(@class,"footer")]/a[contains(@class,"default")]/span'

    '''SHARE WINDOW'''

    # Инпут ввода имени пользователя или группы
    SHARE_INPUT = '//div[contains(@class,"share-window")]/div[contains(@class,"body")]//input[contains(@placeholder,"Введите")]'
    # Элементы выпадашки с пользователями или группами
    SHARE_DROPDOWN = '//div[contains(@class,"share-window")]/div[contains(@class,"body")]//div[contains(@class,"dropdown")and not(contains(@class,"none"))]/div[contains(@class,"items")]/table/tbody/tr/td[contains(@class,"last")]/div/span'
    # Список строк пользователей или групп с доступом
    SHARE_LIST = '//div[contains(@class,"share-window")]/div[contains(@class,"body")]/div[contains(@class,"flex-1")]//div[contains(@class,"items")]/table/tbody/tr'
    # Развернуть список уровней доступа (искать от строки выше + перед действием нужен клик по td с доступами...)
    SHARE_TRIGGER = '//div[contains(@class,"acces")]/div[contains(@class,"box")]/a[contains(@class,"btn-trigger")]'
    # Список уровней доступа
    SHARE_LEVEL = '//td[contains(@class,"column int")]/div[contains(@class,"focus") and contains(@class,"open")]/div[contains(@class,"dropdown")and not(contains(@class,"none"))]/div[contains(@class,"items")]/table/tbody/tr/td'
    # Кнопка "Сохранить"
    SHARE_SAVE = '//div[contains(@class,"share-window")]/div[contains(@class,"footer")]/a[contains(@class,"primary")]/span'

    '''COPY WINDOW'''

    # Инпут ввода нового названия
    COPY_WINDOW_INPUT = '//div[contains(@class,"window") and contains(@class,"selector")]/div[contains(@class,"body")]//div[contains(@class,"location")]//input'
	# Кнопка "Копировать"
    COPY_WINDOW_COPYBTN= '//div[contains(@class,"window") and contains(@class,"selector")]/div[contains(@class,"footer")]/a[contains(@class,"primary")]/span'

    '''ERRORS'''

    # Окно ошибки error dzmessage (красная всплывающая) без привязки к конкретному текусту ошибки
    ERROR_NOTIFICATION = '//div[contains(@class, "error")]'
    # Закрытие любого окна ошибки error dzmessage (красная всплывающая)
    ERROR_CLOSE = '//div[contains(@class, "error")]/button'