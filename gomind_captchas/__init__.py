from selenium.webdriver.common.by import By
from time import sleep
from PIL import Image
import io

from anticaptchaofficial.imagecaptcha import *
from anticaptchaofficial.recaptchav2proxyless import *
from anticaptchaofficial.hcaptchaproxyless import *
import os
import pyautogui as py
from dotenv import load_dotenv

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

__all__ = ['wait_element', 'send_keys', 'click']

load_dotenv()

CAPTCHA_KEY = os.getenv("CAPTCHA_KEY")

if CAPTCHA_KEY is None:
    raise Exception("CAPTCHA_KEY não foi definida no arquivo .env")

class WebWait:
    @staticmethod
    def wait_element(driver, time=10, by=By.XPATH, element=str):
        try:
            return WebDriverWait(driver, time).until(
                EC.presence_of_element_located((by, element))
            )
        except Exception as _:
            raise Exception(f"Elemento não encontrado: {_}")

    @staticmethod
    def send_keys(driver, time=10, by=By.XPATH, element=str, keys=str):
        try:
            elem = WebWait.wait_element(driver, time, by, element)
            elem.send_keys(keys)
        except Exception as _:
            raise Exception(f"Erro ao enviar keys: {_}")

    @staticmethod
    def click(driver, time=10, by=By.XPATH, element=str):
        try:
            elem = WebDriverWait(driver, time).until(
                EC.element_to_be_clickable((by, element))
            )
            elem.click()
        except Exception as _:
            raise Exception(f"Erro ao clicar em {element}: {_}")

class CaptchaSolver:

    @staticmethod
    def image_solver(driver, xpath_img=str, xpath_input=str, xpath_button=str):

        '''
        Função para resolver captcha de imagem\n
        :param driver: driver do selenium
        :param xpath_img: xpath da imagem do captcha
        :param xpath_input: xpath do input onde será inserido o captcha
        :param xpath_button: xpath do botão de submit
        
        :raises: Exception caso ocorra algum erro ao resolver o captcha de imagem'''

        try:
            image_captcha = WebWait.wait_element(driver, by=By.XPATH, element=xpath_img, time=20)
            src = image_captcha.get_attribute("src")
            print("Capturando captcha em Location: {captcha_file_location}")
            captcha_file_location = "image.png"

            print(f"Downloading image: {src}\nLocation: {captcha_file_location}")

            image_binary = image_captcha.screenshot_as_png
            img = Image.open(io.BytesIO(image_binary))
            img.save(captcha_file_location, )

            solver = imagecaptcha()
            solver.set_verbose(1)
            solver.set_key(CAPTCHA_KEY)

            captcha_text = solver.solve_and_return_solution(captcha_file_location)

            if captcha_text != 0:
                print(f"captcha text {captcha_text} ")
                WebWait.send_keys(driver, by=By.XPATH, element=xpath_input, keys=captcha_text)
                sleep(0.5)
                WebWait.click(driver, by=By.XPATH, element=xpath_button)
                print("Captcha resolvido!")
            else:
                print(f"task finished with error {solver.error_code}")
                raise Exception("Captcha não foi resolvido pelo anticaptcha")
        except Exception as _:
            raise Exception(f"Erro ao resolver captcha: {_}")
        
    @staticmethod
    def recaptcha_solver(driver, xpath_submit, xpath_iframe, site_token=str, url=str, by=By.XPATH):

        '''
        Função para resolver recaptcha v2\n
        :param driver: driver do selenium
        :param site_token: token onde o recaptcha está presente (buscar no código fonte da página, e coletar com get_attribute())
        :param url: url do site onde o recaptcha está presente
        :param by: tipo de busca do elemento (default: By.XPATH)
        :param xpath_submit: Utilizado no final da função para clicar no botão de submit (ex: botão de login, botão de confirmar, etc) NÃO utilizar xpath do botão de submit do recaptcha
        :param xpath_iframe: xpath do iframe onde o recaptcha está presente
        '''


        solver = recaptchaV2Proxyless()
        solver.set_verbose(1)
        solver.set_key(CAPTCHA_KEY)
        solver.set_website_url(url)
        solver.set_website_key(site_token)

        solver.set_soft_id(0)

        g_response = solver.solve_and_return_solution()
        if g_response != 0:
            print(f"g-response: {g_response}")
        else:
            print(f"Ocorreu um erro {solver.error_code}")

        url = url
        g_recaptcha_response = WebWait.wait_element(driver, by=By.ID, element="g-recaptcha-response", time=10)

        driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "{}";'.format(g_response))
        
        recaptcha_response = driver.find_element(By.ID, "g-recaptcha-response").get_attribute('innerHTML')
        print(f"Recaptcha response preenchido: {recaptcha_response}") # target textarea that is supposed to be injected with the token, I found upon some research

        driver.switch_to.frame(WebWait.wait_element(driver, element=xpath_iframe, time=5))

        input = driver.find_element(By.XPATH, '//*[@id="recaptcha-token"]')
        driver.execute_script(f"arguments[0].setAttribute('value', '{g_response}')", input)
        time.sleep(1)

        py.press('tab')
        py.press('esc')
        driver.switch_to.default_content()
        time.sleep(1)
        WebWait.click(driver, time=5, by=by, element=xpath_submit)
