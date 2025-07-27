class MyFilesEditorLocators:
    # Комбобокс переменной анкеты (Текст последнего div равен названию переменной)
    QUESTIONNAIRE_ITEM_NAME = '//table/tbody/tr[contains(@class,"questionnaire")]//div[contains(@class,"header")]/div'
    # Кнопка "Сохранить" в тулбаре
    SAVE_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"body")]//button[contains(@title,"Сохранить")]'
    
    # Кнопка "Отправить на согласование"
    SEND_FOR_APPROVAL_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"header")]/div[contains(@class,"commands")]/button/label[contains(text(), "согласование")]/ancestor::button'
    # Кнопка "Действия" в тулбаре WF
    WF_ACTIONS_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"header")]/div[contains(@class,"commands")]/button/label/following-sibling::div[contains(@class,"trigger")]'
    # Tr выпадающего списка "Действия" в тулбаре WF (текст последнего label содержит название действия)
    WF_ACTIONS_LIST_ITEM = '//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"header")]/div[contains(@class,"commands")]/button/label/following-sibling::div[contains(@class,"container")and not(contains(@class,"display-none"))]//label'
    # Кнопка "Доступ" в тулбаре
    ACCESS_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"header")]/div[contains(@class,"commands")]/button/label[contains(text(), "Доступ")]/ancestor::button'