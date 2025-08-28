from locators.base_locators import BaseLocators

class GenerationLocators(BaseLocators):
    # Любая ошибка в сообщениях о ходе генерации ERROR
    GENERATION_ERROR = '//div[contains(@class, "job-monitor")]//div[contains(@class, "messages")]//p[contains(text(), "Ошибка")]'
    # Прогресс генерации
    GENERATION_PROGRESS ='//td[contains(@class, "column last")]//div[contains(@class, "cell")]//span[contains(@class, "text")]'