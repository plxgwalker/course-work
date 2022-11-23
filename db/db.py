import sqlite3


class DB:
    def __init__(self, db_file) -> None:
        """Initializing db."""
        self.connector = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connector.cursor()

    def check_if_user_exists(self, user_id: int) -> bool:
        """Check if user already exists in db."""
        result = self.cursor.execute("SELECT user_info.user_id FROM user_info WHERE user_id = "+str(user_id)+";")
        return bool(len(result.fetchall()))

    def add_new_user(self, user_id: int, user_nickname: str, user_first_name: str, user_last_name: str) -> None:
        """Adding new user to db."""
        self.cursor.execute("INSERT INTO user_info (user_id, user_nickname, user_fname, user_lname) VALUES (?, ?, ?, ?)"
                            , (user_id, user_nickname, user_first_name, user_last_name))
        self.connector.commit()

    def get_user_info(self, user_id: int, user_first_name, user_last_name, user_age, user_city, user_join_date) -> str:
        self.cursor.execute("SELECT * FROM user_info WHERE user_id = "+str(user_id)+";")
        info = self.cursor.fetchone()
        user_info = f"\U0001F5D3 Information about You:\n\n\U0001F194: {info[0]}{user_first_name}" \
                    f"{user_last_name}{user_age}{user_city}{user_join_date}" \
                    f"\n\nYou can add or modify your information running a command /edit_info."
        self.connector.commit()
        return user_info

    def user_first_name(self, user_id: int) -> str:
        user_first_name = self.cursor.execute("SELECT user_info.user_fname FROM user_info WHERE user_id = "+str(user_id)+";")
        return f"\n<b>First name:</b> {user_first_name.fetchone()[0]}"

    def user_last_name(self, user_id: int) -> str:
        user_last_name = self.cursor.execute("SELECT user_info.user_lname FROM user_info WHERE user_id = "+str(user_id)+";")
        return f"\n<b>Last name:</b> {user_last_name.fetchone()[0]}"

    def user_age(self, user_id: int) -> str:
        user_age = self.cursor.execute("SELECT user_info.user_age FROM user_info WHERE user_id = "+str(user_id)+";")
        return f"\n<b>Age:</b> {user_age.fetchone()[0]}"

    def user_city(self, user_id: int) -> str:
        user_city = self.cursor.execute("SELECT user_info.user_location FROM user_info WHERE user_id = "+str(user_id)+";")
        return f"\n<b>City:</b> {user_city.fetchone()[0]}"

    def user_join_date(self, user_id: int) -> str:
        user_join_date = self.cursor.execute("SELECT user_info.user_join_date FROM user_info WHERE user_id = "+str(user_id)+";")
        return f"\n<b>\U0001F4C5 Join date:</b> {user_join_date.fetchone()[0]}"

    def edit_user_param(self, user_id: int, user_column: str, user_val: str) -> None:
        self.cursor.execute(f"UPDATE user_info SET '{user_column}' = '{user_val}' WHERE user_id = '{str(user_id)}';")
        self.connector.commit()

    def add_order(self, user_id: int, order_title: str, order_description: str, order_price) -> None:
        self.cursor.execute("INSERT INTO orders (user_id, order_title, order_description, order_price) "
                            "VALUES(?, ?, ?, ?)", (user_id, order_title, order_description, order_price))
        self.connector.commit()

    def show_orders(self) -> list:
        self.cursor.execute("SELECT * FROM orders;")
        result = self.cursor.fetchall()
        return result

    def buy_order(self, order_id: int, user_id: int) -> None:
        self.cursor.execute("SELECT * FROM orders WHERE order_id = "+str(order_id)+";")
        result = self.cursor.fetchone()
        self.cursor.execute("INSERT INTO orders_purchased (order_id, order_title, order_price, user_id) "
                            "VALUES (?, ?, ?, ?)", (result[0], result[2], result[3], str(user_id)))
        self.connector.commit()

    def delete_order_row(self, order_id: str) -> None:
        self.cursor.execute("DELETE FROM orders WHERE order_id = "+str(order_id)+";")
        self.connector.commit()

    def show_purchased_orders(self, user_id: int) -> list:
        self.cursor.execute(f"SELECT * FROM orders_purchased WHERE user_id = {user_id};")
        result = self.cursor.fetchall()
        return result
