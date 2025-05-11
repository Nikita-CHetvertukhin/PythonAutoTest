from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.base_page import BasePage  # Импорт базового класса, содержащего общие методы для работы со страницами
from locators.workflow_editor_locators import WorkflowEditorLocators
from utils.element_searching import XPathFinder

class WorkflowEditorPage(BasePage):
    """Класс, представляющий страницу "Редактор рабочего процесса" в приложении.
    Наследует BasePage, что позволяет использовать общие методы работы со страницами.
    """

    def verify_process_name(self, name):
        """Проверяет, что текст label в тулбаре совпадает с name."""
        try:
            # Ожидание появления label и текста внутри него
            WebDriverWait(self.driver, 5).until(
                EC.text_to_be_present_in_element((By.XPATH, WorkflowEditorLocators.WFEDITOR_PROCESSNAME), name)
            )

            label_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, WorkflowEditorLocators.WFEDITOR_PROCESSNAME))
            )

            label_text = label_element.text.strip()

            # Проверяем соответствие
            if label_text == name:
                self.logger.info(f"Название открытого процесса совпадает: '{label_text}' == '{name}'")
                return True
            else:
                self.logger.warning(f"Несоответствие названия открытого процесса: '{label_text}' != '{name}'")
                return False

        except Exception as e:
            self.logger.error(f"Ошибка при проверке названия процесса: {e}")
            return False

    def action_from_document(self, action_name):
        """Нажимает 'Действия', внутри документа и кликает по элементу action_name"""
        xpath = XPathFinder(self.driver)
        # Кнопка "Действия"
        EDITOR_ACTIONS_BUTTON = '//div[@class="header"]/div[contains(@class,"content")]/div[contains(@class, "toolbar")]//div[contains(@class,"action")]/div'
        # Выпадающий список с кнопками из "Действия"
        EDITOR_ACTIONS_DROPDOWN = '//div[@class="header"]/div[contains(@class,"content")]/div[contains(@class, "toolbar")]//div[contains(@class,"action")]/div/div[contains(@class,"dropdown")]/div/table/tbody/tr'
        
        self.logger.info("Клик по кнопке 'Действия'")
        action_button = xpath.find_visible(WorkflowEditorLocators.EDITOR_ACTIONS_BUTTON, timeout=1)
        action_button.click()

        self.logger.info(f"Клик по кнопке {action_name}")
        action_xpath = xpath.find_located(f'{WorkflowEditorLocators.EDITOR_ACTIONS_DROPDOWN}/td[@title="{action_name}"]', timeout=3, few=False)
        action_xpath.click()