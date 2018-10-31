__author__ = 'alexsviridov'

# import telebot

BOT_TOKEN = "660361487:AAFBBtv8y1pfqY-pPekyT3Qbom9RMWD0Glg"

# Настройки
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os


from DB import BotDatabase

#BOT_TOKEN = "TOKEN"
PORT = int(os.environ.get('PORT', '8443'))
updater = Updater(BOT_TOKEN)


dispatcher = updater.dispatcher

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class CalcBot:
    Value = 0.0

    def __init__(self):
        self.db = BotDatabase()
        self.Value = self.db.getValue()
        logging.log(logging.DEBUG, "--load value from DB %s" % self.Value)

    def parseValue(self, text):
        s = text.split()
        v = s[0]
        t = " ".join(s[1:])[:20]

        logging.log(logging.DEBUG, "--parse %s --  %s" % (v,t))

        try:
            return (float(v), t)
        except ValueError:
            return (0.0, t)

    def calulate(self, text):
        p = self.parseValue(text)
        self.Value += p[0]
        self.db.setValue(self.Value)
        self.db.setLog(p[0], p[1])

    def __del__(self):
        pass #self.db.close()

calc = CalcBot()


# Обработка команд
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся? \n %s' % os.environ['DATABASE_URL'])

def listCommand(bot, update):
    cur = calc.db.getLog()
    list = ""
    for record in cur:
        list += "{:%d-%m-%Y %H:%M}, {}, {:.2} \n".format( record[1], record[2], record[3] )
    list += "current value = %10.2f" % calc.Value

    bot.send_message(chat_id=update.message.chat_id, text=list)

def textMessage(bot, update):
    calc.calulate(update.message.text)
    response = '>>> ' + update.message.text + '\n = %10.2f' % calc.Value
#    response = '>> ' + update.message.text
    bot.send_message(chat_id=update.message.chat_id, text=response)


# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
list_command_handler = CommandHandler('list', listCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)

# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(list_command_handler)
dispatcher.add_handler(text_message_handler)

# Начинаем поиск обновлений
#updater.start_polling(clean=True)

updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=BOT_TOKEN)
updater.bot.set_webhook("https://peaceful-hamlet-47591.herokuapp.com/" + BOT_TOKEN)

# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()