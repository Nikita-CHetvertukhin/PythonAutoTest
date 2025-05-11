class WorkflowAdministrationLocators:
    # Столбцы Navigator Listbox со списком задач
    COLUMN_NAVIGATOR_LISTBOX = '//div[contains(@class, "body")]/div[contains(@class, "navigator")]/div[contains(@class, "box")]//div[@class="scroller headers"]/table/tbody/tr[@class="header"]'
    # Скроллер Navigator Listbox со списком задач
    SCROLLER_NAVIGATION_LISTBOX = '//div[contains(@class, "body")]/div[contains(@class, "navigator")]/div[contains(@class, "box")]//div[@class="scroller items"]'
    #ntcn
    COLUMN = '//div[contains(@class, "fieldset")]//table/tbody/tr[@class="header"]'
    #ntcn
    SCROLLER = '//div[contains(@class, "fieldset")]//div[not(contains(@class, "display-none"))]/div[@class="scroller items"]'