class WorkflowEditorLocators:
   # Название процесса в тулбаре
   WFEDITOR_PROCESSNAME = '//body//div[contains(@class,"wfeditor")]/div[contains(@class,"toolbar")]/div[contains(@class,"label")]'
   # Кнопка "Действия"
   EDITOR_ACTIONS_BUTTON = '//div[@class="header"]/div[contains(@class,"content")]/div[contains(@class, "toolbar")]//div[contains(@class,"action")]/div'
   # Выпадающий список с кнопками из "Действия"
   EDITOR_ACTIONS_DROPDOWN = '//div[@class="header"]/div[contains(@class,"content")]/div[contains(@class, "toolbar")]//div[contains(@class,"action")]/div/div[contains(@class,"dropdown")]/div/table/tbody/tr'