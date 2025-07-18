class MyTasksLocators:
    # Заголовок активного раздела в "Мои задачи"
    MY_TASKS_TITLE = '//div[contains(@class, "tasks") and contains(@class, "tab") and not(contains(@class, "inactive"))]//a[contains(@class, "folder") and contains(@class, "btn")]'
    # Столбцы body
    MY_TASKS_COLUMNS = '//div[contains(@class,"tasks") and not(contains(@class,"inactive"))]//div[@class="scroller headers"]/table/tbody/tr[@class="header"]'
    # Поиск всех строк в столбце "Название" в body "Мои задачи"
    MY_TASKS_LIST = '//div[contains(@class,"finder") and not(contains(@class,"none"))]//div[contains(@class, "tab")and contains(@class,"task") and not(contains(@class,"inactive"))]//div[@class="scroller items"]/table/tbody/tr/td[contains(@class,"column")and contains(@class,"first")]/div'
    # Путь до tr dropdown выпадающего списка действий с файлом
    MY_TASKS_DROPDOWN = '//body/div[contains(@class,"dropdown")]/div/table/tbody/tr'
    # Кнопка "Создать задачу"
    MY_TASKS_CREATE_TASK_BUTTON = '//div[contains(@class,"tasks") and not(contains(@class,"inactive"))]//div[contains(@class,"location")]//a[contains(@class,"create")]/span'

    '''Окно создания задачи'''

    # Инпут наименования задачи
    MY_TASKS_TASK_NAME_INPUT = '//div[contains(@class,"task-selector")]//div[contains(@class,"body")]//div[contains(@class,"row")]//span[contains(@title,"Наименование задачи")]/parent::div/div/input'
    # Инпут описания (создания задачи из меню Мои задачи)
    MY_TASKS_TASK_DESCRIPTION_INPUT = '//div[contains(@class,"task-selector")]//div[contains(@class,"body")]//div[contains(@class,"row")]//span[contains(@title,"Описание")]/following-sibling::div//div[contains(@contenteditable,"true")]'
    # Инпут описания (создания задачи из файла)
    MY_TASKS_FROM_FILE_TASK_DESCRIPTION_INPUT = '//div[contains(@class,"task-selector")]//div[contains(@class,"body")]//div[contains(@class,"row")]//span[contains(@title,"Комментарий")]/following-sibling::div//div[contains(@contenteditable,"true")]'
    # Инпут типа задачи (создания задачи из меню Мои задачи)
    MY_TASKS_TASK_TYPE_INPUT = '//div[contains(@class,"task-selector")]//div[contains(@class,"body")]//div[contains(@class,"row")]//span[contains(@title,"Тип задачи")]/parent::div/div/input'
    # Инпут типа задачи (создания задачи из файла)
    MY_TASKS_FROM_FILE_TASK_TYPE_INPUT = '//div[contains(@class,"task-selector")]//div[contains(@class,"body")]//div[contains(@class,"row")]//span[contains(@title,"Маршрут согласования")]/parent::div/div/input'
    # Найденный span должен содержать атрибут title с названием процесса (создание задачи из меню Мои задачи)
    MY_TASKS_TASK_TYPE_TRS = '//div[contains(@class,"task-selector")]//div[contains(@class,"body")]//div[contains(@class,"row")]//span[contains(@title,"Тип задачи")]/parent::div/div[contains(@class,"dropdown")and not(contains(@class,"display-none"))]//div[contains(@class,"items")]//tbody/tr/td[1]//span'
    # Найденный span должен содержать атрибут title с названием процесса (создание задачи из файла)
    MY_TASKS_FROM_FILE_TASK_TYPE_TRS = '//div[contains(@class,"task-selector")]//div[contains(@class,"body")]//div[contains(@class,"row")]//span[contains(@title,"Маршрут согласования")]/parent::div/div[contains(@class,"dropdown")and not(contains(@class,"display-none"))]//div[contains(@class,"items")]//tbody/tr/td[1]//span'

    # Инпут дедлайна
    MY_TASKS_TASK_DEADLINE_INPUT = '//div[contains(@class,"task-selector")]//div[contains(@class,"body")]//div[contains(@class,"row")]//span[contains(@title,"Дедлайн")]/parent::div/div/input'
    # Инпут исполнителя
    MY_TASKS_TASK_PERFORMER_INPUT = '//div[contains(@class,"task-selector")]//div[contains(@class,"body")]//div[contains(@class,"row")]//span[contains(@title,"Исполнитель")]/parent::div/div/input'
    # Найденный span должен содержать атрибут title с именем пользователя
    MY_TASKS_TASK_PERFORMER_TRS = '//div[contains(@class,"task-selector")]//div[contains(@class,"body")]//div[contains(@class,"row")]//span[contains(@title,"Исполнитель")]/parent::div/div[contains(@class,"dropdown")and not(contains(@class,"display-none"))]//div[contains(@class,"items")]//tbody/tr/td[2]//span'

    # Кнопка "Отменить"
    MY_TASKS_CANCEL_BUTTON = '//div[contains(@class,"task-selector")]//div[contains(@class,"footer")]/a/span[text()="Отменить"]'
    # Кнопка "Создать задачу"
    MY_TASKS_CREATE_BUTTON = '//div[contains(@class,"task-selector")]//div[contains(@class,"footer")]/a/span[text()="Создать задачу"]'
    # Кнопка "Отправить на согласование"
    MY_TASKS_SEND_FOR_APPROVAL_BUTTON = '//div[contains(@class,"task-selector")]//div[contains(@class,"footer")]/a/span[text()="Отправить на согласование"]'

    # Кнопка переключения на вкладку "Документы"
    MY_TASKS_DOCUMENTS_TAB = '//div[contains(@class,"task-selector")]//div[contains(@class,"body")]//div[contains(@class,"header")]/a[contains(@class,"files")and not(contains(@class,"display-none"))]'
    # Кнопка добавления документа на вкладке "Документы"
    MY_TASKS_DOCUMENTS_ADD_BUTTON = '//div[contains(@class,"task-selector")]//div[contains(@class,"body")]//div[contains(@class,"body")]//span[contains(@class,"toolbar")]//a[contains(@title,"Прикрепить")]'
    # Путь до td с названием документа в меню прикреплении документа (атрибут title последнего span содержит название документа) 
    MY_TASKS_DOCUMENTS_ADD_FILE_TD = '//div[contains(@class,"window")]/div[contains(@class,"body")]//div[contains(@class,"workspace")]/div[contains(@class,"items")]/table/tbody/tr/td[contains(@class,"string")]//span'
    # Кнопка "Выбрать" в меню прикреплении документа
    MY_TASKS_DOCUMENTS_ADD_FILE_SELECT_BUTTON = '//div[contains(@class,"window")]/div[contains(@class,"footer")]/a[contains(@class,"primary")]/span[text()="Выбрать"]'

    '''Окно taskform при открытии задачи'''
    # Сам taskform
    MY_TASKS_TASKFORM = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[@class="taskform"]'
    # Кнопка "Действия"
    MY_TASKS_TASKFORM_ACTIONS_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[@class="taskform"]/div[contains(@class,"toolbox")]//a[contains(@class,"primary")]/span[contains(@title,"Действия")]/ancestor::a'
    # Дропдаун действий с задачей
    MY_TASKS_TASKFORM_ACTIONS_DROPDOWN = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[@class="taskform"]/div[contains(@class,"toolbox")]//div[contains(@class,"dropdown")and not(contains(@class,"display-none"))]//table/tbody/tr'
    # Кнопка создать подзадачу в taskform
    MY_TASKS_TASKFORM_CREATE_SUBTASK_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[@class="taskform"]/div[contains(@class,"toolbox")]/a[contains(@class,"subtask")]/i'
    # Кнопка "Удалить" в taskform
    MY_TASKS_TASKFORM_DELETE_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[@class="taskform"]/div[contains(@class,"toolbox")]/a[contains(@class,"remove")]/i'
    # Кнопка "Закрыть" в taskform
    MY_TASKS_TASKFORM_CLOSE_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[@class="taskform"]/div[contains(@class,"toolbox")]/a[contains(@class,"close")]/i'
    # Кнопка "На весь экран"
    MY_TASKS_TASKFORM_EXPAND_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[@class="taskform"]/div[contains(@class,"toolbox")]/a[contains(@class,"fullscreen")]/i[contains(@class,"expand")]'
    # Кнопка "Свернуть"
    MY_TASKS_TASKFORM_COLLAPSE_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[contains(@class,"taskform")and contains(@class,"taskform-fullscreen")]/div[contains(@class,"toolbox")]/a[contains(@class,"fullscreen")]/i[contains(@class,"collapse")]'
    # Инпут заколовка (названия) задачи (атрибут title равен названию задачи)
    MY_TASKS_TASKFORM_TITLE_INPUT = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[@class="taskform"]//div[@class="row"]//div[contains(@class,"title")]//input'
    # Инпут исполнителя задачи
    MY_TASKS_TASKFORM_EXECUTOR_INPUT = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[@class="taskform"]//div[@class="row"]//span[contains(@title,"Исполнитель")]/parent::div/div/input'
    # Найденный span должен содержать атрибут title с именем пользователя
    MY_TASKS_TASKFORM_EXECUTOR_TRS = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[@class="taskform"]//div[@class="row"]//span[contains(@title,"Исполнитель")]/parent::div/div[contains(@class,"dropdown")and not(contains(@class,"display-none"))]//div[contains(@class,"items")]//tbody/tr/td[2]//span'
    # Инпут дедлайна задачи
    MY_TASKS_TASKFORM_DEADLINE_INPUT = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[@class="taskform"]//div[@class="row"]//span[contains(@title,"Дедлайн")]/parent::div/div/input'
    # Окно календаря с активной введенной в инпут датой
    MY_TASKS_TASKFORM_CALENDAR_ACTIVE_DATE = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[@class="taskform"]//div[@class="row"]//span[contains(@title,"Дедлайн")]/parent::div/div[contains(@class,"calendar") and not(contains(@class,"display-none"))]/div[contains(@class,"day")and not(contains(@class,"week"))]/div[contains(@class,"selected")]'
    # Инпут описания задачи
    MY_TASKS_TASKFORM_DESCRIPTION_INPUT = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[@class="taskform"]//div[@class="row"]//span[contains(@title,"Описание")]/following-sibling::div//div[contains(@contenteditable,"true")]'
    
    # Кнопка "Показать системные события" задачи
    MY_TASKS_TASKFORM_SHOW_SYSTEM_EVENTS_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[@class="taskform"]//div[@class="row"]//span[contains(@title,"Активность")]/div[contains(@class,"checkbox")]/div/div'
    # Отркыть выпадающий список скачивания истории задачи
    MY_TASKS_TASKFORM_DOWNLOAD_HISTORY_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[@class="taskform"]//div[@class="row"]//span[contains(@title,"Активность")]/div[contains(@class,"btn-group")]//a[contains(@class,"trigger")]'
    # Список форматов загрузки истории задачи (атрибут title последнего td можно фильтровать по наличию форматов)
    MY_TASKS_TASKFORM_DOWNLOAD_HISTORY_FORMATS_LIST = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[@class="taskform"]//div[@class="row"]//span[contains(@title,"Активность")]/div[contains(@class,"btn-group")]//div[contains(@class,"dropdown")and not(contains(@class,"display-none"))]//td'
    
    # Путь до кнокпи "Скачать" в  списках документов задачи
    MY_TASKS_TASKFORM_DOWNLOAD_FILE_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[@class="taskform"]//div[@class="row"]//span[contains(@title,"Документы")]/following-sibling::div//div[contains(@class,"items")]//tr//a[contains(@class,"download")]'
    # Путь до кнопки "Удалить" в списках документов задачи
    MY_TASKS_TASKFORM_DELETE_FILE_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[@class="taskform"]//div[@class="row"]//span[contains(@title,"Документы")]/following-sibling::div//div[contains(@class,"items")]//tr//a[contains(@class,"remove")]'
    # Путь до td содержащий title с названием докмуента в списке документов задачи
    MY_TASKS_TASKFORM_DOCUMENTS_FILE_TD = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[@class="taskform"]//div[@class="row"]//span[contains(@title,"Документы")]/following-sibling::div//div[contains(@class,"items")]//tr/td//span'

    # Добавить комментарий к задаче (кликнуть чтобы появился инпут и кнопки сохранить/отменить)
    MY_TASKS_TASKFORM_ADD_COMMENT_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[@class="taskform"]//div[@class="row"]//span[contains(@title,"Активность")]/following-sibling::div[contains(@class,"dummy")]'
    # Текстареа комментария к задаче
    MY_TASKS_TASKFORM_COMMENT_TEXTAREA = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[@class="taskform"]//div[@class="row"]//span[contains(@title,"Активность")]/following-sibling::div[contains(@class,"dummy")]/following-sibling::div[contains(@class, "comment")and contains(@class,"editor")]//textarea'
    # Кнопка "Сохранить" комментарий к задаче
    MY_TASKS_TASKFORM_COMMENT_SAVE_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[@class="taskform"]//div[@class="row"]//span[contains(@title,"Активность")]/following-sibling::div[contains(@class,"dummy")]/following-sibling::div[contains(@class, "comment")and contains(@class,"editor")]/a/span[text()="Сохранить"]'
    # Список всех комментариев с содержимым текстом (text() последнего span равен тексту коммента)
    MY_TASKS_TASKFORM_COMMENT_LIST = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[@class="taskform"]//div[@class="row"]//span[contains(@title,"Активность")]/following-sibling::div[contains(@class,"dummy")]/following-sibling::div[contains(@class, "box")]//div[contains(@class,"items")]//tr//span[contains(@class,"event")]/span'
    # Кнопка "Изменить" комментарий к задаче (не учитывает наличие нескольких комментариев, если нужно можно усложнить)
    MY_TASKS_TASKFORM_COMMENT_EDIT_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[@class="taskform"]//div[@class="row"]//span[contains(@title,"Активность")]/following-sibling::div[contains(@class,"dummy")]/following-sibling::div[contains(@class, "box")]//div[contains(@class,"items")]//tr//div[contains(@class,"toolbox")]/a/span[text()="Изменить"]'
    # Кнопка "Удалить" комментарий к задаче
    MY_TASKS_TASKFORM_COMMENT_DELETE_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"tasks")]//div[@class="taskform"]//div[@class="row"]//span[contains(@title,"Активность")]/following-sibling::div[contains(@class,"dummy")]/following-sibling::div[contains(@class, "box")]//div[contains(@class,"items")]//tr//div[contains(@class,"toolbox")]/a/span[text()="Удалить"]'