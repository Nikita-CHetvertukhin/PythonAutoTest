from locators.base_locators import BaseLocators

class MyFilesEditorLocators(BaseLocators):
    
    '''ВКЛАДКИ ТУЛБАРА'''
    
    # Кнопка файл
    FILE_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"header")]/div[contains(@class,"file")]'
    # Кнопки выпадающего списка меню "Файл"
    FILE_BUTTON_TRS = '//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"header")]/div[contains(@class,"file")]/div[contains(@class,"popup")and not(contains(@class,"display-none"))]/div[contains(@class,"menu")]/div[contains(@class,"item")]'
    # Опубликовать и снятьс  публикации в отедльном блоке в меню "Файл"
    FILE_PUBLICATION_BUTTONS='//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"header")]/div[contains(@class,"file")]/div[contains(@class,"popup")and not(contains(@class,"display-none"))]/div[contains(@class,"menu")]/div[contains(@class,"x-menu")]/div[contains(@class,"x-item")]/div[contains(@class,"headline")]'

    '''ТУЛБАР'''
    
    # Заголовки секци тулбара
    TOOLBAR_SECTION_TITLE = '//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"header")]/div[contains(@class,"tags")]/div'
    # Кнопки внутри активной секции тулбара
    TOOLBAR_SECTION_BUTTONS = '//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"body")]/div[contains(@class,"container")and not(contains(@class,"display-none"))][position() > 1]//div[contains(@class,"button")]'
    # Ещё кнопки внутри активной секции тулбара
    TOOLBAR_SECTION_DIVS = '//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"body")]/div[contains(@class,"container")and not(contains(@class,"display-none"))][position() > 1]//div[contains(@class,"x-control")]'
    # Кнопка "Сохранить" в тулбаре
    SAVE_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"body")]//div[contains(@title,"Сохранить")]'
    # Кнопка "Отмена" в тулбаре
    CANCEL_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"body")]//div[contains(@class,"button") and contains(@title,"Отменить")]'
    # Кнопка "Доступ" в тулбаре
    ACCESS_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"header")]/div[contains(@class,"commands")]//div[contains(@class,"label") and contains(text(), "Доступ")]/ancestor::div[1]'
    # Кнопка "Отправить на согласование"
    SEND_FOR_APPROVAL_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"header")]/div[contains(@class,"commands")]//div[contains(@class,"label") and contains(text(), "на согласование")]/ancestor::div[1]'
    # Кнопка "Действия" в тулбаре Документа
    WF_ACTIONS_BUTTON = '//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"header")]/div[contains(@class,"commands")]/div[contains(@class,"wf-status")]'
    # Tr выпадающего списка "Действия" в тулбаре WF (текст последнего label содержит название действия)
    WF_ACTIONS_LIST_ITEM = '//div[contains(@class,"body")]/div[contains(@class,"toolbar")]/div[contains(@class,"header")]/div[contains(@class,"commands")]/div[contains(@class,"wf-status")]//div[contains(@class,"x-menu") and not(contains(@class,"display-none"))]//div[contains(@class,"x-headline")]'

    '''БОКОВЫЕ ПАНЕЛИ (СЛЕВА)'''

    # Кнопка раздела боковой панели по названию атрибут title в конце равен названию кнопки
    DOC_SIDE_PANEL = '//div[contains(@class,"editor")]/div[contains(@class,"menubar")and contains(@class,"left")]/div[contains(@class,"header")]//div[contains(@class,"button")]'
    #xpath до кнопки активной боковой панели
    DOC_SIDE_PANEL_ACTIVE = '//div[contains(@class,"editor")]/div[contains(@class,"menubar")and contains(@class,"left")]/div[contains(@class,"header")]//div[contains(@class,"button") and(contains(@class,"active"))]'
    # Технический xpath до активной панели
    ACTIVE_SIDE_PANEL = '//div[contains(@class,"editor")]/div[contains(@class,"menubar")and contains(@class,"left")]/div[contains(@class,"body")]/div[not(contains(@class,"display-none"))and not(contains(@class,"resizer"))]'
    # Активный textarea в панели
    ACTIVE_TEXTAREA_PANEL = f'{ACTIVE_SIDE_PANEL}//div[contains(@class,"textarea")and not(contains(@class,"display-none"))]//textarea'

    '''БОКОВЫЕ ПАНЕЛИ ФОРМАТИРОВАНИЯ (СПРАВА)'''

     # Кнопка раздела боковой панели по названию атрибут title в конце равен названию кнопки
    DOC_SIDE_PANEL_FORMAT = '//div[contains(@class,"editor")]/div[contains(@class,"menubar")and contains(@class,"right")]/div[contains(@class,"header")]//div[contains(@class,"x-button")]'
    # Путь до всех доступных действий в панели форматирования (класс x-box) предварительная ориентация только по порядковому номеру (не за что цепляться)
    DOC_SIDE_FORMAT_XBOX = '//div[contains(@class,"editor")]/div[contains(@class,"menubar")and contains(@class,"right")]/div[contains(@class,"body")]/div[contains(@class,"body") and not(contains(@class,"display-none"))]/div[contains(@class,"x-box") and not(contains(@class,"display-none"))]'
    
    '''СХЕМА'''

    # Кнопка создать переменную в пустой схеме
    SCHEM_CREATE_FIRST_VARIABLE = f'{ACTIVE_SIDE_PANEL}//div[contains(@class,"label") and(text()="Создать переменную")]/ancestor::div[1]'
    # Переменная по названию атрибут title последнего span равен названию переменной
    SCHEM_VARIABLE_LIST = f'{ACTIVE_SIDE_PANEL}//table/tbody//span'

    '''АНКЕТА'''

    # Комбобокс переменной анкеты (Текст последнего div равен названию переменной)
    QUESTIONNAIRE_ITEM_NAME = '//table/tbody/tr[contains(@class,"questionnaire")]//div[contains(@class,"header")]/div'
    # Кнопка "Далее" после заполнения анкеты
    QUESTIONNAIRE_FINISH_BUTTON = f'{ACTIVE_SIDE_PANEL}/div[contains(@class,"footer")]/div[contains(@class,"actions")]/div[contains(@class,"button")]'
    # Список действий из кнопки "Далее" текст крайнего label равен названию действия
    QUESTIONNAIRE_FINISH_LIST = f'{QUESTIONNAIRE_FINISH_BUTTON}//div[contains(@class,"headline")]'

    '''РЕДАКТОР'''
    # Технический xpath до листа редактора
    EDITOR_LIST = '//div[contains(@class,"container")]//div[contains(@class,"container")]/div[contains(@class,"editor")]/div[contains(@class,"editor")]/div[contains(@class,"container")]/div[contains(@class,"container")]'
    # Технический xpath до строки (в конце можно добавлять номер строки [x])
    EDITOR_LINE = f'{EDITOR_LIST}//div[contains(@class,"main")]/div[contains(@class,"x-line")]'
    # Универсальный инпут, принимает текст туда где активен курсор в докмуенте
    DOC_INPUT = f'{EDITOR_LIST}/input'
    # Кнопка привязки к схеме, появляющая после выделения текста
    EDITOR_TIE = f'{EDITOR_LIST}/div[contains(@class,"minibar")]/div[1]'
    # Выпадающий список по нажатию ПКМ в тексте документа текст последнего label равен названию действия по ПКМ
    EDITOR_DROPDOWN = f'{EDITOR_LIST}/div[contains(@class,"hover")]/div/div[contains(@class,"item")]/label'

    '''ФУТЕР'''
    # Статус документа
    DOC_STATUS = '//div[contains(@class,"container")]/div[contains(@class,"body")]/div[contains(@class,"statusbar")]/div[contains(@class,"status")]' #[contains(text(),"Последнее")]