class MyTasksLocators:
    # Заголовок активного раздела в "Мои задачи"
    MY_TASKS_TITLE = '//div[contains(@class, "tasks") and contains(@class, "tab") and not(contains(@class, "inactive"))]//a[contains(@class, "folder") and contains(@class, "btn")]'
    # Столбцы body
    MY_TASKS_COLUMNS = '//div[contains(@class,"tasks") and not(contains(@class,"inactive"))]//div[@class="scroller headers"]/table/tbody/tr[@class="header"]'
    # Кнопка "Создать задачу"
    MY_TASKS_CREATE_TASK_BUTTON = '//div[contains(@class,"tasks") and not(contains(@class,"inactive"))]//div[contains(@class,"location")]//a[contains(@class,"create")]/span'

    '''Окно создания задачи'''

    # Инпут типа задачи
    MY_TASKS_TASK_TYPE_INPUT = '//div[contains(@class,"task-selector")]//div[contains(@class,"body")]//div[contains(@class,"row")]//span[contains(@title,"Тип задачи")]/parent::div/div/input'
    # Найденный span должен содержать атрибут title с названием процесса
    MY_TASKS_TASK_TYPE_TRS = '//div[contains(@class,"task-selector")]//div[contains(@class,"body")]//div[contains(@class,"row")]//span[contains(@title,"Тип задачи")]/parent::div/div[contains(@class,"dropdown")and not(contains(@class,"display-none"))]//div[contains(@class,"items")]//tbody/tr/td[1]//span'
    # Кнопка "Отменить"
    MY_TASKS_CANCEL_BUTTON = '//div[contains(@class,"task-selector")]//div[contains(@class,"footer")]/a/span[text()="Отменить"]'