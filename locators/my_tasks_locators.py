class MyTasksLocators:
    # Заголовок активного раздела в "Мои задачи"
    MY_TASKS_TITLE = '//div[contains(@class, "tasks") and contains(@class, "tab") and not(contains(@class, "inactive"))]//a[contains(@class, "folder") and contains(@class, "btn")]'
    # Столбцы body
    MY_TASKS_COLUMNS = '//div[contains(@class,"tasks") and not(contains(@class,"inactive"))]//div[@class="scroller headers"]/table/tbody/tr[@class="header"]'