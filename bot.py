import time
import telebot
from config import token
from parsers import parser
from time import sleep

bot = telebot.TeleBot(token)
name = ''
price_category = 0
l = 0
k = 10
now_prod = 0
flag = False
@bot.message_handler(content_types=['text'])
def search_producte(message):
    global k
    global l
    global name
    global flag
    global now_prod
    if message.text.lower() == '/start':
        bot.send_message(message.from_user.id,'Пожалуйста введите название или бренд для поиска.')
        bot.register_next_step_handler(message,get_dis)
    elif message.text.lower() == '/help':
        bot.send_message(message.from_user.id,'Чтобы начать поиск введите /start (начать новый поиск),вводите название или бренд,\nвведите /help для информационной сводки,\nвведя /next_page выводит следующие 10 значений(вторым сообщением вводите Ok),\nкоманда /clear очищает поиск,\nкоманда /break завершает поиск,\n/contnue выводит с того места где остановились')
    elif message.text.lower() == '/next_page':
        flag = False
        l += 10
        k += 10
        bot.register_next_step_handler(message,get_data)
    elif message.text.lower() == '/continue':
        flag = False
        l = now_prod
        bot.register_next_step_handler(message,get_data)
    elif message.text.lower() == '/clear':
        name =''
        l = 0
        k = 10
    elif message.text.lower() == '/break':
        flag = True
def get_dis(message):
    global price_category
    sk = message.text
    bot.send_message(message.from_user.id,'Ценовая категория(вторым сообщением Ok)')
    global name
    name = sk
    bot.register_next_step_handler(message,prices)
def prices(message):
    global price_category
    pr_st = message.text.lower()
    if pr_st != '/pass':
        price_category = int(pr_st)
    elif pr_st == '/pass':
        price_category = 0
    bot.register_next_step_handler(message,get_data)
def get_data(message):
    global name
    global l
    global k
    global flag
    global now_prod
    bot.send_message(message.from_user.id,'Начинаю загрузгу данных!')
    if price_category == 0:
        kl = parser(name,pr = 10000000)
    else:
        kl = parser(name,pr=price_category)
    bot.send_message(message.from_user.id,'Загрузка данных закончена!')
    sleep(5)
    for i in kl[l:k]:
        image = i['image']
        body = i['body']
        bot.send_photo(message.from_user.id,image)
        bot.send_message(message.from_user.id,body)
        if flag:
            break
        else:
            now_prod += 1
            sleep(15)
    bot.send_message(message.from_user.id,'Закончил')




bot.polling(none_stop=True,timeout=60)
