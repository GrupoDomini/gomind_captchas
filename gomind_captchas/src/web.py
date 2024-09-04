from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def wait_element(driver, time=10, by=By.XPATH, element=str):
    try:
        element = WebDriverWait(driver, time).until(
            EC.presence_of_element_located((by, element))
        )
        return element
    except Exception as _:
        raise Exception(f"Elemento não encontrado: {_}")

def send_keys(driver, time=10, by=By.XPATH, element=str, keys=str):
    try:
        element = wait_element(driver, time, by, element)
        element.send_keys(keys)
    except Exception as _:
        raise Exception(f"Erro ao enviar keys: {_}")

def click(driver, time=10, by=By.XPATH, element=str):
    try:
        element = WebDriverWait(driver, time).until(EC.element_to_be_clickable((by, element)))
        element.click()
    except Exception as _:
        raise Exception(f"Erro ao clicar: {_}")
    



