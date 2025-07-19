class MyFilesEditorLocators:
    # Комбобокс переменной анкеты (Текст последнего div равен названию переменной)
    QUESTIONNAIRE_ITEM_NAME = '//table/tbody/tr[contains(@class,"questionnaire")]//div[contains(@class,"header")]/div'
    # Кнопка "Сохранить" в тулбаре
    SAVE_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"body")]//button[contains(@title,"Сохранить")]'
    # Кнопка "Отправить на согласование"
    SEND_FOR_APPROVAL_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"header")]/div[contains(@class,"commands")]/button/label[contains(text(), "согласование")]/ancestor::button'