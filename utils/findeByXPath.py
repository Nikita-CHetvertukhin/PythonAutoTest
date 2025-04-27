from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Проверяет, что элемент присутствует в DOM дереве.
def finde_Xpath_located(driver,path):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, path)))

#Проверяет, что элемент видим.
def finde_Xpath_visible(driver, path):
    return WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, path)))

# Проверяет, что элемент кликабелен.
def finde_Xpath_clickable(driver, path):
    return WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, path)))

# Проверяет, что элемент не видим.
def finde_Xpath_invisible(driver, path):
    return WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.XPATH, path)))

