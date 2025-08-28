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
    # Иконка добавления обещго диска
    SIDE_MENU_ADD_SHARE_DRIVE = '//div[contains(@class,"body")]/div[not(contains(@class, "display-none"))]/div[contains(@class, "header") and contains(@class, "radio")]/div[contains(@class,"shared-drives")]/a[contains(@class,"new")]/i'
    # Активная текстареа нового названия общего диска
    SIDE_MENU_TEXTAREA_SHARE_DRIVE = '//div[contains(@class,"body")]/div[not(contains(@class, "display-none"))]/div[contains(@class, "header") and contains(@class, "radio")]/div[contains(@class,"shared-drives")]//div[contains(@class,"items")]//tr[contains(@class,"active")]//textarea'

    '''BODY'''

    # Заголовок раздела
    BODY_TITLE = '//div[contains(@class,"body")]/div[contains(@class,"tabs")]/div[contains(@class,"body")]/div[not(contains(@class,"inactive"))]//div[contains(@class,"commands")]/a[contains(@class,"folder")]'
    # Путь до иконки загрузки списка (песочные часы в заголовке раздела)
    BODY_STATUS = f'{BODY_TITLE}/i[contains(@class,"hourglass")and not(contains(@class,"empty"))]'
    # Путь до TR с заголовками столбоц TD
    BODY_COLUMNS = '//div[contains(@class,"body")]/div[contains(@class,"tabs")]/div[contains(@class,"body")]/div[not(contains(@class,"inactive"))]//div[@class="scroller headers"]/table/tbody/tr[@class="header"]'
    # Универсальный путь до строк списка файлов в любом активном боковом меню
    BODY_LIST = '//div[contains(@class,"body")]/div[contains(@class,"tabs")]/div[contains(@class,"body")]/div[not(contains(@class,"inactive"))]//div[contains(@class,"items")]/table/tbody/tr'
    # Универсальный путь до ячейки строки с названием файла
    BODY_NAMES = '//div[contains(@class,"body")]/div[contains(@class,"tabs")]/div[contains(@class,"body")]/div[not(contains(@class,"inactive"))]//div[contains(@class,"items")]/table/tbody/tr/td[contains(@class,"column")and contains(@class,"first")]/div'
    # Путь до TEXTAREA для ввода названия процесса/документа (например при переименовании) PS старый xpath нужен анализ
    BODY_TEXTAREA = '//div[contains(@class,"textarea")]/div/textarea'
    # Универсальный dropdown после ПКМ по файлу
    BODY_DROPDOWN = '//body/div[contains(@class,"dropdown")and not(contains(@class, "display-none"))]/div/table/tbody/tr'

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
    # Кнопка "Отменить"
    SHARE_CANCEL = '//div[contains(@class,"share-window")]/div[contains(@class,"footer")]/a[contains(@class,"default")]/span[contains(text(),"Отменить")]'

    '''PUBLISH WINDOW'''

    # Инпут ввода директории публикации
    PUBLISH_DIRECTORY_INPUT = '//div[contains(@class,"publish-window")]/div[contains(@class,"body")]//input[contains(@placeholder,"Шаблоны")]'
    # Путь до выпадающего списка со строками директорий
    PUBLISH_DIRECTORY_DROPDOWN = '//div[contains(@class,"publish-window")]/div[contains(@class,"body")]//div[contains(@class,"dropdown")and not(contains(@class,"none"))]/div[contains(@class,"items")]/table/tbody/tr/td[contains(@class,"first")]/div/span'
    # Путь до инпута имени пользователя или группы
    PUBLISH_INPUT = '//div[contains(@class,"publish-window")]/div[contains(@class,"body")]//input[contains(@placeholder,"Введите")]'
    # Элементы выпадашки с пользователями или группами
    PUBLISH_DROPDOWN = '//div[contains(@class,"publish-window")]/div[contains(@class,"body")]//div[contains(@class,"dropdown")and not(contains(@class,"none"))]/div[contains(@class,"items")]/table/tbody/tr/td[contains(@class,"last")]/div/span'
    # Список УЗ или групп на публикацию
    PUBLISH_LIST = '//div[contains(@class,"publish-window")]/div[contains(@class,"body")]/div[contains(@class,"flex-1")]//div[contains(@class,"items")]/table/tbody/tr'
    # Кнопка "Готово"
    PUBLISH_FINISH = '//div[contains(@class,"publish-window")]/div[contains(@class,"footer")]/a[contains(@class,"primary")]/span'
    # Кнопка "Отменить"
    PUBLISH_CANCEL = '//div[contains(@class,"publish-window")]/div[contains(@class,"footer")]/a[contains(@class,"default")]/span[contains(text(),"Отменить")]'

    '''COPY WINDOW'''

    # Инпут ввода нового названия
    COPY_WINDOW_INPUT = '//div[contains(@class,"window") and contains(@class,"selector")]/div[contains(@class,"body")]//div[contains(@class,"location")]//input'
	# Кнопка "Копировать"
    COPY_WINDOW_COPYBTN = '//div[contains(@class,"window") and contains(@class,"selector")]/div[contains(@class,"footer")]/a[contains(@class,"primary")]/span'
    # Список доступных папок для перемещения
    COPY_WINDOW_LIST = '//div[contains(@class,"window") and contains(@class,"selector")]/div[contains(@class,"body")]//div[contains(@class,"items")]//tr'

    '''POPUR WINDOWS'''
    # Любой информативный POPUP
    POPUP = '//div[contains(@class, "dzmessage")and (contains(@class,"info"))]'
    # Кнопка закрытия любого попапа
    POPUP_CLOSE = '//div[contains(@class, "dzmessage")]/button'
    # Кнопка подтверждения действия в всплывающем информативном окне
    POPUP_CONFIRM = '//div[contains(@class, "popup")]/div[contains(@class, "footer")]/a[contains(@class, "primary")]/span'
    # Кнопка отмены действия в всплывающем информативном окне
    POPUP_CANCEL = '//div[contains(@class, "popup")]/div[contains(@class, "footer")]/a[contains(@class, "default")]/span'

    '''ERRORS'''

    # Окно ошибки error dzmessage (красная всплывающая) без привязки к конкретному текусту ошибки
    ERROR_NOTIFICATION = '//div[contains(@class, "error")]'
    # Закрытие любого окна ошибки error dzmessage (красная всплывающая)
    ERROR_CLOSE = '//div[contains(@class, "error")]/button'