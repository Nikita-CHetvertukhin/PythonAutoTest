from locators.base_locators import BaseLocators

class WorkflowEditorLocators(BaseLocators):

   '''Тулбар'''

    # Кнопка "Файл"
   WFEDITOR_FILE_BUTTON = '//body//div[contains(@class,"wfeditor")]/div[contains(@class,"toolbar")]/button[contains(@class,"file")]'
   # Выпадающий список с кнопками из "Файл"
   WFEDITOR_FILE_DROPDOWN = '//div[not(contains(@class,"display-none"))and contains(@class,"x-popup")]/div[contains(@class,"menu")]'
   # Путь до элементов фигур в тулбаре wfeditor сами - элементы /a внутри
   WFEDITOR_SHAPE_BUTTONS = '//body//div[contains(@class,"wfeditor")]/div[contains(@class,"toolbar")]/div[contains(@class,"shape")]'
   # Путь до кнопок Отменить/Повторить (идут следующими /a)
   WFEDITOR_UNDOREDO = '//body//div[contains(@class,"wfeditor")]/div[contains(@class,"toolbar")]/div[contains(@class,"undo")]'
   # Путь до "Отдалить"/"Приблизить"/Автомасштаб (идут следующими /a)
   WFEDITOR_ZOOM = '//body//div[contains(@class,"wfeditor")]/div[contains(@class,"toolbar")]/div[contains(@class,"tools")]/div[contains(@class,"zoom")]'
   # Путь до инпута со значением текущего масштаба
   WFEDITOR_ZOOM_INPUT = '//body//div[contains(@class,"wfeditor")]/div[contains(@class,"toolbar")]/div[contains(@class,"tools")]/div[contains(@class,"zoom")]/div//input[@type="text"]'
   
   '''Лист редактора'''

   # Путь до видимой области редактора
   WFEDITOR_VIEWS = '//div[contains(@class,"body")]/div[contains(@class,"wfeditor")]/div[contains(@class,"body")]//div[contains(@class,"views")]//*[name()="svg"]'
   # Область доски процессов ограниченная крайними точками созданных фигур, внутри содержит объекты фигур
   WFEDITOR_LAYERS = '//div[contains(@class,"views")]//*[name()="svg"]/*[name()="g"]'
   # Путь до g внутри которого массив g фигур созданных на доске (можно использовать при проверке автомасштаба)
   WFEDITOR_SHAPES = '//div[contains(@class,"body")]/div[contains(@class,"wfeditor")]/div[contains(@class,"body")]//div[contains(@class,"views")]//*[name()="svg"]/*[name()="g"]/*[name()="g"][contains(@class, "cells")]'
   # Путь до элементов массива g с характеристиками фигур
   WFEDITOR_SHAPES_TOOLS = '//div[contains(@class,"body")]/div[contains(@class,"wfeditor")]/div[contains(@class,"body")]//div[contains(@class,"views")]//*[name()="svg"]/*[name()="g"]/*[name()="g"][contains(@class, "tools")]/*[name()="g"][contains(@class, "tools")]'

   '''Свойства процесса и фигур'''

   # Инпут наименования процесса или фигуры
   WFEDITOR_PROPERTIES_NAME = '//div[contains(@class,"properties")]/div[contains(@class,"properties")and not(contains(@class,"display-none"))]//span[contains(@title,"Наименование")]/following-sibling::div[contains(@class,"box")]/input'
   # Инпут описания процесса или фигуры
   WFEDITOR_PROPERTIES_DESCRIPTIONS = '//div[contains(@class,"properties")]/div[contains(@class,"properties")and not(contains(@class,"display-none"))]//div[contains(@class,"rte")]/span[contains(@title,"Описание")]/following-sibling::div[contains(@class,"box")]//div[contains(@contenteditable,"true")]'
   # Инпут срока процесса или фигуры
   WFEDITOR_PROPERTIES_TERM = '//div[contains(@class,"properties")]//span[contains(@title,"Срок")]/following-sibling::div[contains(@class,"box")]/input'
   # Инпут уведомления о приближении срока процесса или фигуры
   WFEDITOR_PROPERTIES_NOTIFY_TERM_INPUT = '//div[contains(@class,"properties")]//span[contains(@title,"Уведомить")]/following-sibling::div[contains(@class,"box")]/input'
   # Стрелка октрывающая выпадающий список срока процесса или фигуры
   WFEDITOR_PROPERTIES_NOTIFY_TERM_BUTTON = '//div[contains(@class,"properties")]//span[contains(@title,"Уведомить")]/following-sibling::div[contains(@class,"box")]/a'
   # Элементы выпадающего списка срока процесса или фигуры в последнем div содержится атрибут text, по которому можно искать
   WFEDITOR_PROPERTIES_NOTIFY_TERM_LIST = '//div[contains(@class,"properties")]//span[contains(@title,"Уведомить")]/parent::div/div[contains(@class,"dropdown")and not(contains(@class,"display-none"))]/div[contains(@class,"items")]/table/tbody/tr/td/div/div'
   # Инпут добавления наблюдателя
   WFEDITOR_PROPERTIES_OBSERVER_INPUT = '//div[contains(@class,"properties")]//span[contains(@title,"Добавить наблюдателя")]/following-sibling::div[contains(@class,"box")]/input'
   # Элементы выпадающего списка наблюдателей. В последнем span содержится атрибут title
   WFEDITOR_PROPERTIES_OBSERVER_LIST = '//div[contains(@class,"properties")]//span[contains(@title,"Добавить наблюдателя")]/parent::div/div[contains(@class,"dropdown")and not(contains(@class,"display-none"))]/div[contains(@class,"items")]/table/tbody/tr/td/div/span'
   # Элементы таблицы наблюдателей. В последнем span содержится атрибут title
   WFEDITOR_PROPERTIES_OBSERVER_TABLE = '//div[contains(@class,"properties")]//span[contains(@title,"Наблюдатели")]/parent::div//div[contains(@class,"items")]/table/tbody/tr/td/div/span'

   # Чекбокс "Автоматизация при старте" процесса или фигуры
   WFEDITOR_PROPERTIES_START_AUTO = '//div[contains(@class,"properties")]/div[contains(@class,"properties")and not(contains(@class,"display-none"))]//div[contains(@class,"checkbox")]/span[contains(@title,"старте")]/parent::div/div[contains(@class,"box")]/div[contains(@class,"checkbox")]'
   # Первый экземпляр автоматизации при старте, инпут. Можно проверять по атрибуту title
   WFEDITOR_PROPERTIES_START_AUTO_FIRST_INPUT = '//div[contains(@class,"properties")]/div[contains(@class,"properties")and not(contains(@class,"display-none"))]//div[contains(@class,"checkbox")]/span[contains(@title,"старте")]/parent::div/following-sibling::div[1][not(contains(@class,"display-none"))]/div[contains(@class,"form")][1]//div[contains(@class,"combobox")]/div/input'
   # Первый экземпляр автоматизации при старте, кнопка раскрытия выпадающего списка вида автомтаизаций
   WFEDITOR_PROPERTIES_START_AUTO_FIRST_BUTTON = '//div[contains(@class,"properties")]/div[contains(@class,"properties")and not(contains(@class,"display-none"))]//div[contains(@class,"checkbox")]/span[contains(@title,"старте")]/parent::div/following-sibling::div[1][not(contains(@class,"display-none"))]/div[contains(@class,"form")][1]//div[contains(@class,"combobox")]/div/a'
   # Элементы span выпадающего списка видов автоматизаций только для первого комбобокса. По атрибуту title можно выбирать
   WFEDITOR_PROPERTIES_START_AUTO_FIRST_lIST = '//div[contains(@class,"properties")]/div[contains(@class,"properties")and not(contains(@class,"display-none"))]//div[contains(@class,"checkbox")]/span[contains(@title,"старте")]/parent::div/following-sibling::div[1][not(contains(@class,"display-none"))]/div[contains(@class,"form")][1]//div[contains(@class,"combobox")]/div[contains(@class,"dropdown")and not(contains(@class,"display-none"))]/div[contains(@class,"items")]/table/tbody/tr/td/div/span'
    # Путь до иконки выбора каталога в автоматизациях при старте
   WFEDITOR_PROPERTIES_START_AUTO_FOLDER_ICON = '//div[contains(@class,"properties")]/div[contains(@class,"properties")and not(contains(@class,"display-none"))]//div[contains(@class,"checkbox")]/span[contains(@title,"старте")]/parent::div/following-sibling::div[1][not(contains(@class,"display-none"))]/div[contains(@class,"form")]/div[contains(@class,"parameters")]//span[contains(@title,"Каталог")]/ancestor::div[1]//a[contains(@title,"каталог")]'
   # Путь до span с названием параметра автоматизации при старте (атрибут title последнего span содержит название параметра автоматизации)
   WFEDITOR_PROPERTIES_START_AUTO_BOXNAME = '//div[contains(@class,"properties")]/div[contains(@class,"properties")and not(contains(@class,"display-none"))]//div[contains(@class,"checkbox")]/span[contains(@title,"старте")]/parent::div/following-sibling::div[1][not(contains(@class,"display-none"))]/div[contains(@class,"form")]/div[ contains(@class,"parameters")]//div[contains(@class,"combobox")]/span'

   # Чекбокс "Автоматизация при завершении" процесса или фигуры
   WFEDITOR_PROPERTIES_FINISH_AUTO = '//div[contains(@class,"properties")]/div[contains(@class,"properties")and not(contains(@class,"display-none"))]//div[contains(@class,"checkbox")]/span[contains(@title,"завершении")]/parent::div/div[contains(@class,"box")]/div[contains(@class,"checkbox")]'
   # Первый экземпляр автоматизации при завершении, инпут. Можно проверять по атрибуту title
   WFEDITOR_PROPERTIES_FINISH_AUTO_FIRST_INPUT = '//div[contains(@class,"properties")]/div[contains(@class,"properties")and not(contains(@class,"display-none"))]//div[contains(@class,"checkbox")]/span[contains(@title,"завершении")]/parent::div/following-sibling::div[1][not(contains(@class,"display-none"))]/div[contains(@class,"form")][1]//div[contains(@class,"combobox")]/div/input'
   # Первый экземпляр автоматизации при завершении, кнопка раскрытия выпадающего списка вида автомтаизаций
   WFEDITOR_PROPERTIES_FINISH_AUTO_FIRST_BUTTON = '//div[contains(@class,"properties")]/div[contains(@class,"properties")and not(contains(@class,"display-none"))]//div[contains(@class,"checkbox")]/span[contains(@title,"завершении")]/parent::div/following-sibling::div[1][not(contains(@class,"display-none"))]/div[contains(@class,"form")][1]//div[contains(@class,"combobox")]/div/a'
   # Элементы span выпадающего списка видов автоматизаций только для первого комбобокса. По атрибуту title можно выбирать
   WFEDITOR_PROPERTIES_FINISH_AUTO_FIRST_lIST = '//div[contains(@class,"properties")]/div[contains(@class,"properties")and not(contains(@class,"display-none"))]//div[contains(@class,"checkbox")]/span[contains(@title,"завершении")]/parent::div/following-sibling::div[1][not(contains(@class,"display-none"))]/div[contains(@class,"form")][1]//div[contains(@class,"combobox")]/div[contains(@class,"dropdown")and not(contains(@class,"display-none"))]/div[contains(@class,"items")]/table/tbody/tr/td/div/span'
   # Путь до всех иконок выбора каталога в автоматизациях при завершении
   WFEDITOR_PROPERTIES_FINISH_AUTO_FOLDER_ICON = '//div[contains(@class,"properties")]/div[contains(@class,"properties")and not(contains(@class,"display-none"))]//div[contains(@class,"checkbox")]/span[contains(@title,"завершении")]/parent::div/following-sibling::div[1][not(contains(@class,"display-none"))]/div[contains(@class,"form")]/div[contains(@class,"parameters")]//span[contains(@title,"Каталог")]/ancestor::div[1]//a[contains(@title,"каталог")]'
   # Путь до span с названием параметра автоматизации при завершении (атрибут title последнего span содержит название параметра автоматизации)
   WFEDITOR_PROPERTIES_FINISH_AUTO_BOXNAME = '//div[contains(@class,"properties")]/div[contains(@class,"properties")and not(contains(@class,"display-none"))]//div[contains(@class,"checkbox")]/span[contains(@title,"завершении")]/parent::div/following-sibling::div[1][not(contains(@class,"display-none"))]/div[contains(@class,"form")]/div[ contains(@class,"parameters")]//div[contains(@class,"combobox")]/span'

   '''Свойства только фигур'''

   # Кнопка раскрытия выпадающего списка исполнителей
   WFEDITOR_PROPERTIES_EXECUTOR_BUTTON = '//div[contains(@class,"properties")]//span[contains(@title,"Исполнитель")]/following-sibling::div[contains(@class,"box")]/a'
   # Элементы выпадающего списка Исполнителей. В последнем span содержится атрибут title
   WFEDITOR_PROPERTIES_EXECUTOR_LIST = '//div[contains(@class,"properties")]//span[contains(@title,"Исполнитель")]/parent::div/div[contains(@class,"dropdown")and not(contains(@class,"display-none"))]/div[contains(@class,"items")]/table/tbody/tr/td/div/span'
   # Инпут добавления исполнителя
   WFEDITOR_PROPERTIES_EXECUTOR_INPUT = '//div[contains(@class,"properties")]//span[contains(@title,"Исполнитель")]/following-sibling::div[contains(@class,"box")]/input'

   # Кнопка раскрытия выпадающего списка стадий
   WFEDITOR_PROPERTIES_STAGE_BUTTON = '//div[contains(@class,"properties")]//span[contains(@title,"Стадия процесса")]/following-sibling::div[contains(@class,"box")]/a[2]'
   # Элементы выпадающего списка стадий. В последнем span содержится атрибут title
   WFEDITOR_PROPERTIES_STAGE_LIST = '//div[contains(@class,"properties")]//span[contains(@title,"Стадия процесса")]/parent::div/div[contains(@class,"dropdown")and not(contains(@class,"display-none"))]/div[contains(@class,"items")]/table/tbody/tr/td/div/span'
   # Инпут добавления стадий
   WFEDITOR_PROPERTIES_STAGE_INPUT = '//div[contains(@class,"properties")]//span[contains(@title,"Стадия процесса")]/following-sibling::div[contains(@class,"box")]/input'

   # Строки таблицы связи фигуры (содержат td с /div/span с конетнтом ячеек)
   WFEDITOR_PROPERTIES_CONNECT_TRS = '//div[contains(@class,"properties")]/div[contains(@class,"properties")and not(contains(@class,"display-none"))]//div[contains(@class,"sortable")and not(contains(@class,"empty"))]/div[contains(@class,"headers")]/table/tbody/tr/td[contains(@title,"Целевой")]/ancestor::div[contains(@class,"sortable")]/div[contains(@class,"items")]//tr'

   # Свойство "Резльтат" фигуры "Выход" (class может быть svg-circle-24, svg-check-circle-24, svg-cancel-circle-24)
   WFEDITOR_PROPERTIES_EXIT_RESULT = '//div[contains(@class,"properties")]/div[contains(@class,"properties")and not(contains(@class,"display-none"))]/div[contains(@class,"checkbox")]/span[contains(@title,"Результат")]/parent::div/div/div'

   '''Свойства только процесса'''

   # Кнопка создания Роли процесса
   WFEDITOR_PROPERTIES_INSERT_ROLE = '//span[contains(@class,"toolbar")]/div[text()="Роли"]/following-sibling::div[contains(@class,"group")]/a[contains(@title,"Insert")]'
   # Кнопка удаления Роли процесса
   WFEDITOR_PROPERTIES_DELETE_ROLE = '//span[contains(@class,"toolbar")]/div[text()="Роли"]/following-sibling::div[contains(@class,"group")]/a[contains(@title,"Delete")]'
   # Строки таблицы ролей
   WFEDITOR_PROPERTIES_ROLE_TRS = '//span[contains(@class,"toolbar") and contains(@title,"Роли")]/following-sibling::div[contains(@class,"box")]/div/div[contains(@class,"items")]/table/tbody/tr'
   # Специальный инпут для ячейки с выпадающим списком
   WFEDITOR_PROPERTIES_ROLE_CELLWITHDROPDOWN_INPUT = '//span[contains(@class,"toolbar") and contains(@title,"Роли")]/following-sibling::div[contains(@class,"box")]//div[contains(@class,"items")]/table//tbody/tr/td/div[contains(@class,"combobox")]/div[contains(@class,"box")]/input'
   # Путь до span элемента выпадающего списка
   WFEDITOR_PROPERTIES_ROLE_CELLWITHDROPDOWN_DROPDOWN = '//span[contains(@class,"toolbar") and contains(@title,"Роли")]/following-sibling::div[contains(@class,"box")]//div[contains(@class,"items")]/table//tbody/tr/td/div[contains(@class,"combobox")]/div[contains(@class,"dropdown") and not(contains(@class,"display-none"))]/div[contains(@class,"items")]/table/tbody/tr/td[contains(@class,"last")]/div/span' 

   # Кнопка создания Переменной процесса
   WFEDITOR_PROPERTIES_INSERT_VARIABLE = '//span[contains(@class,"toolbar")]/div[text()="Переменные"]/following-sibling::div[contains(@class,"group")]/a[contains(@title,"Insert")]'
   # Кнопка удаления Переменной процесса
   WFEDITOR_PROPERTIES_DELETE_VARIABLE = '//span[contains(@class,"toolbar")]/div[text()="Переменные"]/following-sibling::div[contains(@class,"group")]/a[contains(@title,"Delete")]'
   # Строки таблицы Переменных
   WFEDITOR_PROPERTIES_VARIABLE_TRS = '//span[contains(@class,"toolbar") and contains(@title,"Переменные")]/following-sibling::div[contains(@class,"box")]/div/div[contains(@class,"items")]/table/tbody/tr'
   # Кнопка раскрытия выпадающего списка типа переменной
   WFEDITOR_PROPERTIES_VARIABLE_CELLWITHDROPDOWN_BUTTON = '//span[contains(@class,"toolbar") and contains(@title,"Переменные")]/following-sibling::div[contains(@class,"box")]//div[contains(@class,"items")]/table//tbody/tr/td/div[contains(@class,"combobox")]/div[contains(@class,"box")]/a'
   # Путь до div элемента выпадающего списка. У div есть атрибут text
   WFEDITOR_PROPERTIES_VARIABLE_CELLWITHDROPDOWN_DROPDOWN = '//span[contains(@class,"toolbar") and contains(@title,"Переменные")]/following-sibling::div[contains(@class,"box")]//div[contains(@class,"items")]/table//tbody/tr/td/div[contains(@class,"combobox")]/div[contains(@class,"dropdown") and not(contains(@class,"display-none"))]/div[contains(@class,"items")]/table/tbody/tr/td/div/div'

   # Кнопка создания Стадии процесса
   WFEDITOR_PROPERTIES_INSERT_STAGE = '//span[contains(@class,"toolbar")]/div[text()="Стадии"]/following-sibling::div[contains(@class,"group")]/a[contains(@title,"Insert")]'
   # Кнопка удаления Стадии процесса
   WFEDITOR_PROPERTIES_DELETE_STAGE = '//span[contains(@class,"toolbar")]/div[text()="Стадии"]/following-sibling::div[contains(@class,"group")]/a[contains(@title,"Delete")]'
   # Строки таблицы Стадий
   WFEDITOR_PROPERTIES_STAGEE_TRS = '//span[contains(@class,"toolbar") and contains(@title,"Стадии")]/following-sibling::div[contains(@class,"box")]/div/div[contains(@class,"items")]/table/tbody/tr'

   '''Окно настроек доступа для роли'''

   # Инпут доступа к документам
   WFEDITOR_PROPERTIES_SHARE_INPUT = '//div[contains(@class,"access-editor")]/div[contains(@class,"body")]/div[contains(@class,"row")]/div/div//span[contains(@title,"документам")]/ancestor::div[contains(@class,"row")][1]//div[contains(@class,"combobox")]/div[contains(@class,"box")]/input'
   # Стрелка выпадающего список с доступами к документу
   WFEDITOR_PROPERTIES_SHARE_SHOW_LIST = '//div[contains(@class,"access-editor")]/div[contains(@class,"body")]/div[contains(@class,"row")]/div/div//span[contains(@title,"документам")]/ancestor::div[contains(@class,"row")][1]//div[contains(@class,"combobox")]/div[contains(@class,"box")]/a'
   # Строки выпадающего списка с доступами к документу
   WFEDITOR_PROPERTIES_SHARE_LIST = '//div[contains(@class,"access-editor")]/div[contains(@class,"body")]/div[contains(@class,"row")]/div/div//span[contains(@title,"документам")]/ancestor::div[contains(@class,"row")][1]//div[contains(@class,"combobox")]/div[contains(@class,"dropdown")and not(contains(@class,"display-none"))]/div[contains(@class,"items")]/table/tbody/tr'
   # Строки с чек-боксами с достпуами к полям
   WFEDITOR_PROPERTIES_SHARE_TRS = '//div[contains(@class,"access-editor")]/div[contains(@class,"body")]/div[contains(@class,"row")]/div/div//span[contains(@title,"полям")]/ancestor::div[contains(@class,"row")][1]//div[contains(@class,"items")]/table/tbody/tr'
   # Кнопка "Готово"
   WFEDITOR_PROPERTIES_SHARE_READY = '//div[contains(@class,"access-editor")]/div[contains(@class,"footer")]/a/span[text()="Готово"]'
   # Кнопка "Отменить"
   WFEDITOR_PROPERTIES_SHARE_CANCEL = '//div[contains(@class,"access-editor")]/div[contains(@class,"footer")]/a/span[text()="Отменить"]'

   '''Окно выбора каталога'''
   # Выбор секции в которой нахожится каталог (text() последнего span равен нужной секции)
   WFEDITOR_PROPERTIES_CATALOG_SECTIONS = '//div[contains(@class,"window")]/div[contains(@class,"body")]//div[contains(@class,"btn-group")]/a[not(contains(@class,"disabled"))]/span'
   # Поиск каталога в айтемах (title последнего span содержит название нужного файла)
   WFEDITOR_PROPERTIES_CATALOG_ITEMS = '//div[contains(@class,"window")]/div[contains(@class,"body")]//div[contains(@class,"workspace")]/div[contains(@class,"items")]/table/tbody//tr//td[contains(@class,"first")]//span'
   # Кнопка "Выбрать" в окне выбора каталога
   WFEDITOR_PROPERTIES_CATALOG_SELECT = '//div[contains(@class,"window")]/div[contains(@class,"footer")]/a[not(contains(@class,"disabled"))]/span[text()="Выбрать"]'