"""
TODO:
    * show_orders
"""
import telebot
from telebot import types
from db.db import DB

API_TOKEN = '5405008993:AAHERhjznn_4l5k9-5nBTgS-W0DDSqXYGfo'
bot = telebot.TeleBot(API_TOKEN, parse_mode="html")

DB = DB("db/tg_db.db")


@bot.message_handler(commands=["start"])
def start(message) -> None:
    if DB.check_if_user_exists(message.from_user.id):
        reply = f"You <b>have already registered</b> in our shop."
        bot.send_message(message.chat.id, reply)
        return

    reply = f"Hi, <b>{message.from_user.first_name}</b>. My name is Easy Shop, I provide you a platform to buy or " \
            f"sell goods. Nice to meet You and best usage."

    user_id = message.from_user.id
    user_nickname = message.from_user.username
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name

    DB.add_new_user(user_id, user_nickname, user_first_name, user_last_name)

    bot.send_message(message.chat.id, reply)


@bot.message_handler(commands=["get_info"])
def get_info(message) -> None:
    user_first_name = DB.user_first_name(message.from_user.id)
    user_last_name = DB.user_last_name(message.from_user.id)
    user_age = DB.user_age(message.from_user.id)
    user_city = DB.user_city(message.from_user.id)
    user_join_date = DB.user_join_date(message.from_user.id)
    bot.send_message(message.chat.id, DB.get_user_info(message.from_user.id, user_first_name, user_last_name, user_age,
                                                       user_city, user_join_date))


@bot.message_handler(commands=["edit_info"])
def edit_info(message) -> None:
    markup = types.InlineKeyboardMarkup()

    user_first_name = types.InlineKeyboardButton(text="First name", callback_data="user_f_name")
    user_last_name = types.InlineKeyboardButton(text="Last name", callback_data="user_l_name")
    user_age = types.InlineKeyboardButton(text="Age", callback_data="user_age")
    user_city = types.InlineKeyboardButton(text="City", callback_data="user_city")
    markup.add(user_first_name, user_last_name, user_age, user_city)

    reply = f"Which information You want to add/modify?\n\nIt can be:\n- First name\n- Last name" \
            f"\n- Age\n- City"
    bot.send_message(message.chat.id, reply, reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def edit_info_reply(callback):
    if callback.data == "user_f_name":
        bot.send_message(callback.message.chat.id, f"Ok, cool. Now type your new first name down below.")
        DB.edit_user_param(callback.message.chat.id, "user_fname", "Test")
    elif callback.data == "user_l_name":
        bot.send_message(callback.message.chat.id, f"Ok, cool. Now type your new first name down below.")
        DB.edit_user_param(callback.message.chat.id, "user_lname", "Test")


@bot.message_handler(commands=["add_order"])
def add_order(message) -> None:
    try:
        order = message.text.split("; ")
        user_id = message.from_user.id
        temp = order[0].split("-")
        order_title = temp[1]
        order_description = order[1]
        order_price = order[2]

        DB.add_order(int(user_id), str(order_title), str(order_description), int(order_price))

        reply = f"Order with title <b>{order_title}</b> has been added"
        bot.send_message(message.chat.id, reply)
    except:
        instruction = f"\U00002757Post your order <u>correctly</u>:\n" \
                      f"\n<b>Structure</b>: /add_order -title; order description; order price" \
                      f"\nExample: /add_order -Battle of water; Simple water for 300$; 300"
        bot.send_message(message.chat.id, instruction)


if __name__ == "__main__":
    bot.set_my_commands([
        types.BotCommand("/start", "Signing up"),
        types.BotCommand("/get_info", "Get information about me"),
        types.BotCommand("/edit_info", "Edit profile information"),
        types.BotCommand("/add_order", "Post your order")
    ])
    bot.polling(none_stop=True)
