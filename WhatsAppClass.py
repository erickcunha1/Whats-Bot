import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os


class InvalidNumbersHandler:
    def __init__(self, filename='numeros_invalidos.txt'):
        self.filename = filename

    def create_file(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                pass

    def check_and_add_number(self, number):
        with open(self.filename, mode='r') as file:
            lines = file.read()
        if str(number) not in lines:
            with open(self.filename, mode='a') as file:
                file.write(f'{number}\n')


class BrowserInitializer:
    def __init__(self, user_data_dir):
        self.user_data_dir = user_data_dir

    def initialize_browser(self):
        service = Service(ChromeDriverManager().install())
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'user-data-dir={self.user_data_dir}')
        # chrome_options.add_argument('--headless=new')

        navegador = webdriver.Chrome(service=service, options=chrome_options)
        navegador.get('https://web.whatsapp.com/')
        sleep(15)
        return navegador


class WhatsAppMessenger:
    def __init__(self, navegador, invalid_numbers_handler):
        self.navegador = navegador
        self.invalid_numbers_handler = invalid_numbers_handler

    def wait_for_element(self, locator, timeout=4):
        return WebDriverWait(self.navegador, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def send_message(self, name, number, message):
        text = message.replace('fulano', name)
        message_url = f'https://web.whatsapp.com/send?phone={number}&text={text}'

        self.navegador.get(message_url)
        send_button_locator = (By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span')
        continue_button_locator = (By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]')

        try:
            send_button = self.wait_for_element(send_button_locator)
        except:
            self.invalid_numbers_handler.check_and_add_number(number)
            continue_button = self.wait_for_element(continue_button_locator, timeout=4)
            continue_button.click()
        else:
            send_button.click()
            sleep(1)

