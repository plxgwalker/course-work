"""
telebot - Module for work with Telegram API.
db.db - Class for work with SQLiteStudio data base.
"""
import telebot
from telebot import types
from db.db import DB


API_TOKEN = '5405008993:AAHERhjznn_4l5k9-5nBTgS-W0DDSqXYGfo'
bot = telebot.TeleBot(API_TOKEN, parse_mode="html")

DB = DB("db/tg_db.db")


@bot.message_handler(commands=["start"])
def start(message) -> None:
    """Start command in Telegram chat-bot.

    Args:
        message (_type_): Message which has been sent by user.
    """
    if DB.check_if_user_exists(message.from_user.id):
        reply = "You <b>have already registered</b> in our shop."
        bot.send_message(message.chat.id, reply)
        return

    reply = f"Hi, <b>{message.from_user.first_name}</b>. My name is Easy Shop, "
    reply += "I provide you a platform to buy or sell goods. Nice to meet You and best usage."

    user_id = message.from_user.id
    user_nickname = message.from_user.username
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name

    DB.add_new_user(user_id, user_nickname, user_first_name, user_last_name)

    bot.send_message(message.chat.id, reply)


@bot.message_handler(commands=["get_info"])
def get_info(message) -> None:
    """Get information about user from db.

    Args:
        message (_type_): Message which has been sent by user.
    """
    user_first_name = DB.user_first_name(message.from_user.id)
    user_last_name = DB.user_last_name(message.from_user.id)
    user_age = DB.user_age(message.from_user.id)
    user_city = DB.user_city(message.from_user.id)
    user_join_date = DB.user_join_date(message.from_user.id)

    bot.send_message(message.chat.id, DB.get_user_info(message.from_user.id, user_first_name,
                     user_last_name, user_age, user_city, user_join_date))


@bot.message_handler(commands=["edit_info"])
def edit_info(message) -> None:
    """Options of editing information about user.

    Args:
        message (_type_): Message which has been sent by user.
    """
    markup = types.InlineKeyboardMarkup()

    user_first_name = types.InlineKeyboardButton(
        text="First name", callback_data="user_f_name")
    user_last_name = types.InlineKeyboardButton(
        text="Last name", callback_data="user_l_name")
    user_age = types.InlineKeyboardButton(text="Age", callback_data="user_age")
    user_city = types.InlineKeyboardButton(
        text="City", callback_data="user_city")
    markup.add(user_first_name, user_last_name, user_age, user_city)

    reply = "Which information You want to add/modify?\n\nIt can be:\n- First name\n- Last name" \
            "\n- Age\n- City"
    bot.send_message(message.chat.id, reply, reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def edit_info_reply(callback):
    """Edit user parameter which will be chosen by him.

    Args:
        callback (function): Option of user.
    """
    if callback.data == "user_f_name":
        bot.send_message(callback.message.chat.id,
                         "\U0001FAE3 Sorry, that's test area for now.")
        # DB.edit_user_param(callback.message.chat.id, "user_fname", "Test")

    elif callback.data == "user_l_name":
        bot.send_message(callback.message.chat.id,
                         "\U0001FAE3 Sorry, that's test area for now.")

    elif callback.data == "user_age":
        bot.send_message(callback.message.chat.id,
                         "\U0001FAE3 Sorry, that's test area for now.")

    elif callback.data == "user_city":
        bot.send_message(callback.message.chat.id,
                         "\U0001FAE3 Sorry, that's test area for now.")


@bot.message_handler(commands=["add_order"])
def add_order(message) -> None:
    """Add new order to db.

    Args:
        message (_type_): Message which has been sent by user.
    """
    try:
        order = message.text.split("; ")
        user_id = message.from_user.id
        temp = order[0].split("-")
        order_title = temp[1]
        order_description = order[1]
        order_price = order[2]

        DB.add_order(int(user_id), str(order_title), str(
            order_description), int(order_price))

        reply = f"\U00002705 Order with title <b>{order_title}</b> has been added"
        bot.send_message(message.chat.id, reply)
    except:
        instruction = "\U00002757 Post your order <u>correctly</u>:\n" \
                      "\n<b>Structure</b>: /add_order -title; order description; order price" \
                      "\nExample: /add_order -Battle of water; Simple water for 300$; 300"
        bot.send_message(message.chat.id, instruction)


@bot.message_handler(commands=["show_orders"])
def get_orders(message):
    """Show all available orders in one message.

    Args:
        message (_type_): Message which has been sent by user.
    """
    orders = DB.show_orders()
    reply = "\U0001F5D2 Available orders:\n"
    for i in orders:
        order_id = i[0]
        order_title = i[2]
        order_price = i[3]
        order_description = i[4]
        order_date = i[5]
        reply += f"\n\U0001F194: {order_id}, <b>title</b>: {order_title}, " \
                 f"<b>description</b>: {order_description}, \U0001F4B0: {order_price}, \U0001F4C5: {order_date}\n"
    bot.send_message(message.chat.id, reply)


@bot.message_handler(commands=["buy_order"])
def buy_order(message):
    """Buy order by ID.

    Args:
        message (_type_): Message which has been sent by user.
    """
    try:
        order = message.text.split()
        order_id = order[1]
        DB.buy_order(order_id, message.from_user.id)
        DB.delete_order_row(order_id)

        reply = f"\U00002705 You have successfully bought order \U0001F194: {order_id}!"
        bot.send_message(message.chat.id, reply)
    except:
        reply = "\U00002757 Buy orders <u>correctly</u>:\n" \
                "\n<b>Structure</b>: /buy_order order ID" \
                "\nExample: /buy_order 5" \
                "\n\nTo see available orders use this command: /show_orders"
        bot.send_message(message.chat.id, reply)


@bot.message_handler(commands=["show_purchased_orders"])
def show_purchased_orders(message):
    """Show all purchased orders by user.

    Args:
        message (_type_): Message which has been sent by user.
    """
    try:
        result = DB.show_purchased_orders(message.from_user.id)
        reply = "\U0001F6CD <b>Purchased</b> items:\n"
        for i in result:
            reply += f"\n\U0001F194: {i[0]}, <b>Title</b>: {i[1]}, \U0001F4B0: {i[2]}"

        bot.send_message(message.chat.id, reply)
    except:
        reply = "\U0001FAE3 Sorry, but you have not purchased any item yet."
        bot.send_message(message.chat.id, reply)


if __name__ == "__main__":
    bot.set_my_commands([
        types.BotCommand("/start", "Signing up"),
        types.BotCommand("/get_info", "Get information about me"),
        types.BotCommand("/edit_info", "Edit profile information"),
        types.BotCommand("/add_order", "Post your order"),
        types.BotCommand("/show_orders", "List of available goods"),
        types.BotCommand("/buy_order", "Buy a thing"),
        types.BotCommand("/show_purchased_orders",
                         "Show your purchasing history")
    ])

    print("Telegram bot started")
    bot.polling(none_stop=True)
