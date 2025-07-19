class MyFilesLocators:
    # Заголовок активного раздела в "Мои файлы"
    MY_FILES_TITLE = '//div[contains(@class, "workspace") and contains(@class, "tab") and not(contains(@class, "inactive"))]//a[contains(@class, "folder") and contains(@class, "btn")]'
    # Столбцы body
    MY_FILES_COLUMNS = '//div[contains(@class,"workspace") and not(contains(@class,"inactive"))]//div[@class="scroller headers"]/table/tbody/tr[@class="header"]'
    # Поиск всех строк в столбце "Название" в body "Мои файлы" (тут также svg типа файла)
    MY_FILES_LIST = '//div[contains(@class,"finder") and not(contains(@class,"none"))]//div[contains(@class, "tab")and contains(@class,"workspace") and not(contains(@class,"inactive"))]//div[@class="scroller items"]/table/tbody/tr/td[contains(@class,"column")and contains(@class,"first")]/div'
    # Путь до tr dropdown выпадающего списка действий с файлом
    MY_FILES_DROPDOWN = '//body/div[contains(@class,"dropdown")]/div/table/tbody/tr'
    # Кнопка "Создать"
    MY_FILES_CREATE_FILE_BUTTON = '//div[contains(@class,"workspace") and not(contains(@class,"inactive"))]//div[contains(@class,"location")]//a[contains(@class,"create")]/span'
    # Строки выпадающего списка кнопки "Создать" (аргумент title послежнего td содержит название действия)
    MY_FILES_CREATE_FILE_DROPDOWN = '//div[contains(@class,"workspace") and not(contains(@class,"inactive"))]//div[contains(@class,"location")]//a[contains(@class,"create")]/div[contains(@class,"dropdown")and not(contains(@class, "display-none"))]//tr/td'
    # Инпут загрузки документа
    MY_FILES_UPLOAD_INPUT = '//input[@type="file"]'

    # Кнопка "Создать процесс"
    MY_FILES_CREATE = '//div[contains(@class,"body")]//div[contains(@class,"finder") and not(contains(@class,"none"))]/div[@class="body"]/div[contains(@class,"workspace")and not(contains(@class,"inactive"))]/div/div/a[contains(@class,"create")]/span'
    # Выпадашка кнопки "Создать" (@title последнего td содержит название действия)
    MY_FILES_CREATE_DROPDOWN = '//div[contains(@class,"body")]//div[contains(@class,"finder") and not(contains(@class,"none"))]/div[@class="body"]/div[contains(@class,"workspace")and not(contains(@class,"inactive"))]/div/div/a[contains(@class,"create")]/div[contains(@class,"dropdown")and not(contains(@class, "display-none"))]//tr/td'
    # Активное textarea для ввода названия файла
    MY_FILES_TEXTAREA = '//div[contains(@class,"finder") and not(contains(@class,"none"))]//div[contains(@class, "workspace ") and not(contains(@class,"inactive")) and (contains(@class,"tab"))]/div[contains(@class,"items")]/table/tbody/tr[contains(@class,"active")]/td//textarea'