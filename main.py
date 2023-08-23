from whatsbot import WhatsAppBot


excel_path = 'contatos.xlsx'
user_data_directory = '/Users/user/Library/Application Support/Google/Chrome/Selenium' 
bot = WhatsAppBot(user_data_directory, excel_path)
bot.send_messages()
bot.close()