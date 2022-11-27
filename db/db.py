"""sqlite3 - Module for working with SQLiteStudio data bases."""
import sqlite3


class DB:
    """Class represents work with data base.

    Args:
        db_file (file.db): File of data base.

    Methods:
        check_if_user_exists (user_id):
            Checks if user exists in data base.

        add_new_user (user_id: int, user_nickname: str, user_first_name: str,
                     user_last_name: str):
            Adds information about user to data base.

        get_user_info (user_id: int, user_first_name, user_last_name, user_age,
                      user_city, user_join_date):
            Shows information about user.

        user_first_name (user_id: int):
            Returns first name of user.

        user_last_name (user_id: int):
            Returns last name of user.

        user_age (user_id: int):
            Returns user age.

        user_city (user_id: int):
            Returns user city.

        user_join_date (user_id: int):
            Returns user registration date in data base.

        edit_user_param (user_id: int, user_column: str, user_val: str):
            Edits information by parameter in column.

        add_order (user_id: int, order_title: str, order_description: str, order_price):
            Adds new order information to 'orders' table.

        show_orders ():
            Returns list of available orders from 'orders' table.

        buy_order (order_id: int, user_id: int):
            Copy order information from 'orders' table to 'purchased_orders' table.

        delete_order_row (order_id: str):
            Deletes row where is matched 'order_id'.

        show_purchased_orders(user_id: int):
            Returns list of purchased orders by 'user_id'.
    """

    def __init__(self, db_file) -> None:
        """Initializing a data base file."""
        self.connector = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connector.cursor()

    def check_if_user_exists(self, user_id: int) -> bool:
        """SQL request for checking if user exists in table 'user_info'.

        Args:
            user_id (int): ID of current user.

        Returns:
            bool: True if user with this ID exists, False otherwise.
        """
        result = self.cursor.execute(
            "SELECT user_info.user_id FROM user_info WHERE user_id = "+str(user_id)+";")
        return bool(len(result.fetchall()))

    def add_new_user(self, user_id: int, user_nickname: str, user_first_name: str,
                     user_last_name: str) -> None:
        """SQL request for inserting new user to 'user_info' table.

        Args:
            user_id (int): ID of current user.
            user_nickname (str): Nickname of current user.
            user_first_name (str): First name of current user.
            user_last_name (str): Last name of current user.
        """
        self.cursor.execute("INSERT INTO user_info (user_id, user_nickname, user_fname, user_lname) VALUES (?, ?, ?, ?)",
                            (user_id, user_nickname, user_first_name, user_last_name))
        self.connector.commit()

    def get_user_info(self, user_id: int, user_first_name, user_last_name, user_age, user_city,
                      user_join_date) -> str:
        """SQL request for selecting all information about current user.

        Args:
            user_id (int): ID of current user.
            user_first_name (str): First name of current user.
            user_last_name (str): Last name of current user.
            user_age (int): Age of current user.
            user_city (str): Location of current user.
            user_join_date (str): Date of registration user to data base.

        Returns:
            str: String of all information about user.
        """
        self.cursor.execute(
            "SELECT * FROM user_info WHERE user_id = "+str(user_id)+";")
        info = self.cursor.fetchone()
        user_info = f"\U0001F5D3 Information about You:\n\n\U0001F194: {info[0]}{user_first_name}" \
                    f"{user_last_name}{user_age}{user_city}{user_join_date}" \
                    f"\n\nYou can add or modify your information running a command /edit_info."
        self.connector.commit()
        return user_info

    def user_first_name(self, user_id: int) -> str:
        """SQL request for selecting first name information of user.

        Args:
            user_id (int): ID of current user.

        Returns:
            str: String of user first name.
        """
        user_first_name = self.cursor.execute(
            "SELECT user_info.user_fname FROM user_info WHERE user_id = "+str(user_id)+";")
        return f"\n<b>First name:</b> {user_first_name.fetchone()[0]}"

    def user_last_name(self, user_id: int) -> str:
        """SQL request for selecting last name information of user.

        Args:
            user_id (int): ID of current user.

        Returns:
            str: String of user last name.
        """
        user_last_name = self.cursor.execute(
            "SELECT user_info.user_lname FROM user_info WHERE user_id = "+str(user_id)+";")
        return f"\n<b>Last name:</b> {user_last_name.fetchone()[0]}"

    def user_age(self, user_id: int) -> str:
        """SQL request for selecting age information of user.

        Args:
            user_id (int): ID of current user.

        Returns:
            str: String of user age.
        """
        user_age = self.cursor.execute(
            "SELECT user_info.user_age FROM user_info WHERE user_id = "+str(user_id)+";")
        return f"\n<b>Age:</b> {user_age.fetchone()[0]}"

    def user_city(self, user_id: int) -> str:
        """SQL request for selecting city information of user.

        Args:
            user_id (int): ID of current user.

        Returns:
            str: String of user city.
        """
        user_city = self.cursor.execute(
            "SELECT user_info.user_location FROM user_info WHERE user_id = "+str(user_id)+";")
        return f"\n<b>City:</b> {user_city.fetchone()[0]}"

    def user_join_date(self, user_id: int) -> str:
        """SQL request for selecting first name information of user.

        Args:
            user_id (int): ID of current user.

        Returns:
            str: String of user registration date to data base.
        """
        user_join_date = self.cursor.execute(
            "SELECT user_info.user_join_date FROM user_info WHERE user_id = "+str(user_id)+";")
        return f"\n<b>\U0001F4C5 Join date:</b> {user_join_date.fetchone()[0]}"

    def edit_user_param(self, user_id: int, user_column: str, user_val: str) -> None:
        """SQL request for updating information of user.

        Args:
            user_id (int): ID of current user.
            user_column (str): Column which user wants to update.
            user_val (str): Value of column which user wants to update.
        """
        self.cursor.execute(
            f"UPDATE user_info SET '{user_column}' = '{user_val}' WHERE user_id = '{str(user_id)}'")
        self.connector.commit()

    def add_order(self, user_id: int, order_title: str, order_description: str,
                  order_price) -> None:
        """SQL request for inserting new data to 'orders' table.

        Args:
            user_id (int): ID of current user.
            order_title (str): Title of current order.
            order_description (str): Description of current order.
            order_price (_type_): Price of current order.
        """
        self.cursor.execute("INSERT INTO orders (user_id, order_title, order_description, order_price) "
                            "VALUES(?, ?, ?, ?)", (user_id, order_title, order_description, order_price))
        self.connector.commit()

    def show_orders(self) -> list:
        """SQL request for selecting all information about available orders.

        Returns:
            list: List of all orders and their information.
        """
        self.cursor.execute("SELECT * FROM orders;")
        result = self.cursor.fetchall()
        return result

    def buy_order(self, order_id: int, user_id: int) -> None:
        """SQL request for copying information about order from 'orders' and inserting it to
           'orders_purchased'.

        Args:
            order_id (int): ID of current order.
            user_id (int): ID of current user.
        """
        self.cursor.execute(
            "SELECT * FROM orders WHERE order_id = "+str(order_id)+";")
        result = self.cursor.fetchone()
        self.cursor.execute("INSERT INTO orders_purchased (order_id, order_title, order_price, user_id) "
                            "VALUES (?, ?, ?, ?)", (result[0], result[2], result[3], str(user_id)))
        self.connector.commit()

    def delete_order_row(self, order_id: str) -> None:
        """SQL request for deleting 'order_id' information from 'orders' table.

        Args:
            order_id (str): ID of current order.
        """
        self.cursor.execute(
            "DELETE FROM orders WHERE order_id = "+str(order_id)+";")
        self.connector.commit()

    def show_purchased_orders(self, user_id: int) -> list:
        """SQL request for selecting all purchased goods of current user.

        Args:
            user_id (int): ID of current user.

        Returns:
            list: List of user's purchased goods.
        """
        self.cursor.execute(
            f"SELECT * FROM orders_purchased WHERE user_id = {user_id};")
        result = self.cursor.fetchall()
        return result
