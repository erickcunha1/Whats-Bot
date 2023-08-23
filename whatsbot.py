from WhatsAppClass import InvalidNumbersHandler
from WhatsAppClass import BrowserInitializer
from WhatsAppClass import WhatsAppMessenger
import pandas as pd


class WhatsAppBot:
    def __init__(self, user_data_dir, excel_data_path) -> None:
        
        self.excel_data = pd.read_excel(excel_data_path)
        self.invalid_numbers_handler = InvalidNumbersHandler()
        self.invalid_numbers_handler.create_file()
        self.browser_initializer = BrowserInitializer(user_data_dir)
        self.navegador = self.browser_initializer.initialize_browser()
        self.whatsapp_messenger = WhatsAppMessenger(self.navegador, self.invalid_numbers_handler)

    def send_messages(self):
        for index, row in self.excel_data.iterrows():
            self.whatsapp_messenger.send_message(row['Nome'], row['Telefone'], row['Mensagem'])

    def close(self):
        self.navegador.quit()