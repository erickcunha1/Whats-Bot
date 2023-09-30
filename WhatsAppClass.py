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
    """
    Classe para manipular e gerenciar números inválidos.

    Attributes:
        filename (str): O nome do arquivo para armazenar os números inválidos.

    Methods:
        create_file(): Cria o arquivo se não existir.
        check_and_add_number(number): Verifica e adiciona um número ao arquivo, se não estiver presente.
    """

    def __init__(self, filename='numeros_invalidos.txt'):
        self.filename = filename

    def create_file(self):
        """Cria o arquivo se ele não existir."""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                pass

    def check_and_add_number(self, number):
        """
        Verifica e adiciona um número ao arquivo se não estiver presente.

        Args:
            number (int): O número a ser verificado e adicionado.
        """
        with open(self.filename, mode='r') as file:
            lines = file.read()
        if str(number) not in lines:
            with open(self.filename, mode='a') as file:
                file.write(f'{number}\n')


class BrowserInitializer:
    """
    Classe para inicializar e configurar um navegador para interagir com o WhatsApp Web.

    Attributes:
        user_data_dir (str): O diretório para armazenar os dados do usuário do navegador.

    Methods:
        initialize_browser(): Inicializa o navegador e retorna a instância.
    """

    def __init__(self, user_data_dir):
        self.user_data_dir = user_data_dir

    def initialize_browser(self):
        """Inicializa o navegador com as configurações fornecidas."""
        service = Service(ChromeDriverManager().install())
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'user-data-dir={self.user_data_dir}')
        # chrome_options.add_argument('--headless=new')

        navegador = webdriver.Chrome(service=service, options=chrome_options)
        navegador.get('https://web.whatsapp.com/')
        sleep(15)
        return navegador


class WhatsAppMessenger:
    """
    Classe para enviar mensagens através do WhatsApp Web.

    Attributes:
        navegador: Instância do navegador para interação.
        invalid_numbers_handler: Instância do InvalidNumbersHandler para manipulação de números inválidos.

    Methods:
        wait_for_element(locator, timeout=4): Aguarda a presença de um elemento na página.
        send_message(name, number, message): Envia uma mensagem para um número do WhatsApp.
    """

    def __init__(self, navegador, invalid_numbers_handler):
        self.navegador = navegador
        self.invalid_numbers_handler = invalid_numbers_handler

    def wait_for_element(self, locator, timeout=4):
        """
        Aguarda a presença de um elemento na página.

        Args:
            locator: O localizador do elemento.
            timeout (int, opcional): O tempo máximo para aguardar, em segundos. O padrão é 4.

        Returns:
            WebElement: O elemento encontrado.
        """
        return WebDriverWait(self.navegador, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def send_message(self, name, number, message):
        """
        Envia uma mensagem para um número do WhatsApp.

        Args:
            name (str): O nome do destinatário.
            number (str): O número do destinatário.
            message (str): A mensagem a ser enviada.
        """
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


class WhatsAppBot:
    """
    Classe para automatizar o envio de mensagens pelo WhatsApp Web.

    Attributes:
        user_data_dir (str): O diretório para armazenar os dados do usuário do navegador.
        excel_data_path (str): O caminho para o arquivo Excel contendo os dados de contato e mensagem.

    Methods:
        send_messages(): Envia mensagens para os contatos listados no arquivo Excel.
        close(): Fecha o navegador.
    """

    def __init__(self, user_data_dir, excel_data_path):
        self.excel_data = pd.read_excel(excel_data_path)
        self.invalid_numbers_handler = InvalidNumbersHandler()
        self.invalid_numbers_handler.create_file()
        self.browser_initializer = BrowserInitializer(user_data_dir)
        self.navegador = self.browser_initializer.initialize_browser()
        self.whatsapp_messenger = WhatsAppMessenger(self.navegador, self.invalid_numbers_handler)

    def send_messages(self):
        """Envia mensagens para os contatos listados no arquivo Excel."""
        for index, row in self.excel_data.iterrows():
            self.whatsapp_messenger.send_message(row['Nome'], row['Telefone'], row['Mensagem'])

    def close(self):
        """Fecha o navegador."""
        self.navegador.quit()

