from locators.base_locators import BaseLocators

class MyFilesEditorLocators(BaseLocators):
    
    '''ВКЛАДКИ ТУЛБАРА'''
    
    # Кнопка файл
    FILE_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"header")]/button[contains(@class,"file")]'
    # Кнопки выпадающего списка меню "Файл"
    FILE_BUTTON_TRS = '//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"header")]/button[contains(@class,"file")]/div[contains(@class,"popup")and not(contains(@class,"display-none"))]/div[contains(@class,"menu")]/div[contains(@class,"item")]'
    
    '''ТУЛБАР'''
    
    # Кнопка "Сохранить" в тулбаре
    SAVE_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"body")]//button[contains(@title,"Сохранить")]'
    # Кнопка "Доступ" в тулбаре
    ACCESS_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"header")]/div[contains(@class,"commands")]/button/label[contains(text(), "Доступ")]/ancestor::button'
    # Кнопка "Отправить на согласование"
    SEND_FOR_APPROVAL_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"header")]/div[contains(@class,"commands")]/button/label[contains(text(), "согласование")]/ancestor::button'
    # Кнопка "Действия" в тулбаре WF
    WF_ACTIONS_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"header")]/div[contains(@class,"commands")]/button/label/following-sibling::div[contains(@class,"trigger")]'
    # Tr выпадающего списка "Действия" в тулбаре WF (текст последнего label содержит название действия)
    WF_ACTIONS_LIST_ITEM = '//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"header")]/div[contains(@class,"commands")]/button/label/following-sibling::div[contains(@class,"container")and not(contains(@class,"display-none"))]//label'

    '''БОКОВЫЕ ПАНЕЛИ'''

    # Кнопка раздела боковой панели по названию атрибут title в конце равен названию кнопки
    DOC_SIDE_PANEL = '//div[contains(@class,"editor")]/div[contains(@class,"menubar")and contains(@class,"left")]/div[contains(@class,"header")]//button'
    # Технический xpath до активной панели
    ACTIVE_SIDE_PANEL = '//div[contains(@class,"editor")]/div[contains(@class,"menubar")and contains(@class,"left")]/div[contains(@class,"body")]/div[not(contains(@class,"display-none"))and not(contains(@class,"resizer"))]'
    # Активный textarea в панели
    ACTIVE_TEXTAREA_PANEL = f'{ACTIVE_SIDE_PANEL}//div[contains(@class,"textarea")and not(contains(@class,"display-none"))]//textarea'

    '''СХЕМА'''

    # Кнопка создать переменную в пустой схеме
    SCHEM_CREATE_FIRST_VARIABLE = f'{ACTIVE_SIDE_PANEL}//button[contains(@class,"accent")and not(contains(@class,"display-none"))]'
    # Переменная по названию атрибут title последнего span равен названию переменной
    SCHEM_VARIABLE_LIST = f'{ACTIVE_SIDE_PANEL}//table/tbody//span'

    '''АНКЕТА'''

    # Комбобокс переменной анкеты (Текст последнего div равен названию переменной)
    QUESTIONNAIRE_ITEM_NAME = '//table/tbody/tr[contains(@class,"questionnaire")]//div[contains(@class,"header")]/div'
    # Кнопка "Далее" после заполнения анкеты
    QUESTIONNAIRE_FINISH_BUTTON = f'{ACTIVE_SIDE_PANEL}/div[contains(@class,"footer")]//button'
    # Список действий из кнопки "Далее" текст крайнего label равен названию действия
    QUESTIONNAIRE_FINISH_LIST = f'{QUESTIONNAIRE_FINISH_BUTTON}/div[contains(@class,"popup")]//label'

    '''РЕДАКТОР'''
    # Технический xpath до листа редактора
    EDITOR_LIST = '//div[contains(@class,"container")]//div[contains(@class,"container")]/div[contains(@class,"editor")]/div[contains(@class,"editor")]/div[contains(@class,"container")]/div[contains(@class,"container")]'
    # Универсальный инпут, принимает текст туда где активен курсор в докмуенте
    DOC_INPUT = f'{EDITOR_LIST}/input'
    # Кнопка привязки к схеме, появляющая после выделения текста
    EDITOR_TIE = f'{EDITOR_LIST}/div[contains(@class,"minibar")]/button[1]'
    # Выпадающий список по нажатию ПКМ в тексте документа текст последнего label равен названию действия по ПКМ
    EDITOR_DROPDOWN = f'{EDITOR_LIST}/div[contains(@class,"hover")]/div/div[contains(@class,"item")]/label'

    '''ФУТЕР'''
    # Статус документа
    DOC_STATUS = '//div[contains(@class,"container")]/div[contains(@class,"editor")]/div[contains(@class,"body")]/div[contains(@class,"statusbar")]/div[contains(@class,"status")]' #[contains(text(),"Последнее")]