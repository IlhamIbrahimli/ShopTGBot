import sqlite3
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from dbmanager import *

TOKEN = ''
bot = TeleBot(TOKEN)


def card_of_item(bot, message, row):
        
    info = f"""
Товар:   {row[1]}
Цвет:  {row[3]}
Цена:  {row[2]} рублей
"""
    with open(f'images/{row[4]}', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
    bot.send_message(message.chat.id, info, reply_markup=gen_markup(row[0]))

def gen_markup(id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Добавить в корзину", callback_data=f'buy_{id}'))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith("buy"):
        id = call.data[call.data.find("_")+1:]
        manager.buy_item(data=(call.message.chat.id,id,1))


@bot.message_handler(commands=['show_store'])
def show_store(message):
    rows = manager.show_items()
    for i in rows:
        card_of_item(bot,message,i)
        



if __name__ == '__main__':
    manager = StoreManager(DATABASE)
    bot.infinity_polling()  
