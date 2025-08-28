from locators.base_locators import BaseLocators

class WorkflowsLocators(BaseLocators):
    # Заголовок активного раздела в "Рабочие процессы"
    WORKFLOWS_TITLE = '//div[contains(@class, "finder") and not(contains(@class, "none"))]/div[@class="body"]/div[not(contains(@class, "inactive"))]//a[contains(@class, "folder") and contains(@class, "btn")]'
    # Столбцы body
    WORKFLOWS_COLUMNS = '//div[contains(@class,"finder") and not(contains(@class,"none"))]//div[contains(@class, "workspace") and not(contains(@class,"inactive"))]//div[@class="scroller headers"]/table/tbody/tr[@class="header"]'

    # Кнопка "Создать процесс"
    WORKFLOWS_CREATE = '//div[contains(@class,"body")]//div[contains(@class,"finder") and not(contains(@class,"none"))]/div[@class="body"]/div[contains(@class,"workspace")and not(contains(@class,"inactive"))]/div/div/a[contains(@class,"create")]/span'
    # Активное textarea для ввода названия процесса
    WORKFLOWS_TEXTAREA = '//div[contains(@class,"finder") and not(contains(@class,"none"))]//div[contains(@class, "tab") and not(contains(@class,"inactive"))]//div[@class="scroller items"]/table/tbody/tr[contains(@class,"active")]/td[contains(@class,"edit")]//textarea'
    # Поиск всех строк в столбце "Название" в body рабочих процессов
    WORKFLOWS_LIST = '//div[contains(@class,"finder") and not(contains(@class,"none"))]//div[contains(@class, "tab") and not(contains(@class,"inactive"))]//div[@class="scroller items"]/table/tbody/tr/td[contains(@class,"column")and contains(@class,"first")]/div'
    # Активный процесс в body рабочих процессов
    WORKFLOWS_ACTIVE = '//div[contains(@class,"finder") and not(contains(@class,"none"))]//div[contains(@class, "tab") and not(contains(@class,"inactive"))]//div[@class="scroller items"]/table/tbody/tr[contains(@class,"active")]/td[contains(@class,"column")and contains(@class,"first")]/div/span'
    # Элементы dropdown при нажатии ПКМ по процессу
    WORKFLOWS_DROPDOWN = '//body/div[contains(@class,"dropdown")and not(contains(@class, "display-none"))]/div/table/tbody/tr'