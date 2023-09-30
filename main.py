import WhatsAppClass as ws


excel_path = 'contatos.xlsx'
user_data_directory = '/Users/user/Library/Application Support/Google/Chrome/Selenium' 
bot = ws.WhatsAppBot(user_data_directory, excel_path)
bot.send_messages()
bot.close()
