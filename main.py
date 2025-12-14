import telebot
from telebot import types

bot = telebot.TeleBot('8250733906:AAFHGj2dEuPoGrz-JUbDgrXm-oXKj-D4XmE')

user_states = {}
user_data = {}

class State:
    NAME = 1
    PRODUCT = 2
    TIME = 3

orders = {}
order_id = 1

def main_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("➕ Добавить заказ")
    kb.add("📖 Посмотреть заказы")
    kb.add("❌ Удалить заказ")
    return kb

@bot.message_handler(commands=['start', 'basket'])
def start(message):
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}! Я ваш бот-помощник.\nВыберите действие:",
        reply_markup=main_keyboard()
    )

@bot.message_handler(func=lambda m: m.text == "➕ Добавить заказ")
def add_order(message):
    user_states[message.chat.id] = State.NAME
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, "Как вас зовут?")

@bot.message_handler(func=lambda m: user_states.get(m.chat.id) == State.NAME)
def get_name(message):
    user_data[message.chat.id]["name"] = message.text
    user_states[message.chat.id] = State.PRODUCT
    bot.send_message(message.chat.id, "Что вы хотите заказать?")

@bot.message_handler(func=lambda m: user_states.get(m.chat.id) == State.PRODUCT)
def get_product(message):
    user_data[message.chat.id]["product"] = message.text
    user_states[message.chat.id] = State.TIME
    bot.send_message(message.chat.id, "К какому времени доставить заказ?")

@bot.message_handler(func=lambda m: user_states.get(m.chat.id) == State.TIME)
def get_time(message):
    global order_id

    user_data[message.chat.id]["time"] = message.text
    orders[order_id] = user_data[message.chat.id]

    bot.send_message(
        message.chat.id,
        f"✅ Заказ добавлен!\nID заказа: {order_id}"
    )

    order_id += 1
    user_states.pop(message.chat.id)
    user_data.pop(message.chat.id)

@bot.message_handler(func=lambda m: m.text == "📖 Посмотреть заказы")
def show_orders(message):
    if not orders:
        bot.send_message(message.chat.id, "❌ Заказов нет")
        return

    text = ""
    for oid, data in orders.items():
        text += (
            f"ID: {oid}\n"
            f"Имя: {data['name']}\n"
            f"Заказ: {data['product']}\n"
            f"Время: {data['time']}\n\n"
        )

    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text == "❌ Удалить заказ")
def delete_order(message):
    bot.send_message(message.chat.id, "Введите ID заказа для удаления:")

@bot.message_handler(func=lambda m: m.text.isdigit())
def delete_by_id(message):
    oid = int(message.text)
    if oid in orders:
        del orders[oid]
        bot.send_message(message.chat.id, "✅ Заказ удалён")
    else:
        bot.send_message(message.chat.id, "❌ Заказ не найден")

bot.polling(non_stop=True)