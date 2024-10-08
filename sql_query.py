import csv
import datetime
import sqlite3

now_data = datetime.datetime.now(datetime.UTC).strftime("%H:%M-%d.%m.%Y")


class SQL_atm:

    @staticmethod
    def create_table():
        """Create table Users_data"""
        with sqlite3.connect("atm.db") as db:
            cur = db.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS Users_data(
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Number_card INTEGER NOT NULL,
            Pin_code INTEGER NOT NULL,
            Balance INTEGER NOT NULL);""")
            print("Create table Users_data")

    @staticmethod
    def insert_users(data_users):
        """Create new user"""
        with sqlite3.connect("atm.db") as db:
            cur = db.cursor()
            cur.execute("""INSERT INTO Users_data (Number_card, Pin_code, Balance) VALUES(?, ?, ?);""", data_users)
            print("Create new user")

    @staticmethod
    def input_card(number_card):
        """Input and check card"""
        try:
            with sqlite3.connect("atm.db") as db:
                cur = db.cursor()
                cur.execute(f"""SELECT Number_card FROM Users_data WHERE Number_card = {number_card}""")
                result_card = cur.fetchone()
                if result_card == None:
                    print("Insert unknown number of card")
                    return False
                else:
                    print(f"Insert number card {number_card}")
                    return True
        except:
            print("You entered an incorrect card number")

    @staticmethod
    def input_code(number_card):
        """Input and check PIN code"""
        pin_code = input("Input pin-code: ")
        with sqlite3.connect("atm.db") as db:
            cur = db.cursor()
            cur.execute(f"""SELECT Pin_code FROM Users_data WHERE Number_card = {number_card}""")
            result_code = cur.fetchone()
            input_pin = result_code[0]
            try:
                if input_pin == int(pin_code):
                    print("Input right pin-code!")
                    return True
                else:
                    print("Wrong pin-code")
                    return False
            except:
                print("Wrong pin-code")
                return False

    @staticmethod
    def info_balance(number_card):
        """Card balance"""
        with sqlite3.connect("atm.db") as db:
            cur = db.cursor()
            cur.execute(f"""SELECT Balance FROM Users_data WHERE Number_card = {number_card}""")
            result_info_balance = cur.fetchone()
            balance_card = result_info_balance[0]
            print(f"Card balance: {balance_card}")

    @staticmethod
    def withdraw_money(number_card):
        """Withdrawing money"""
        amount = input("Input withdraw summ: ")
        with sqlite3.connect("atm.db") as db:
            cur = db.cursor()
            cur.execute(f"""SELECT Balance FROM Users_data WHERE Number_card = {number_card};""")
            result_info_balance = cur.fetchone()
            balance_card = result_info_balance[0]
            try:
                if int(amount) > balance_card:
                    print("Account has insufficient funds")
                    return False
                else:
                    cur.execute(
                        f"""UPDATE Users_data SET Balance = Balance - {amount} WHERE Number_card = {number_card};""")
                    db.commit()
                    SQL_atm.info_balance(number_card)
                    SQL_atm.report_operation_1(now_data, number_card, "2", amount, "")
                    return True

            except:
                print("Wrong action with balance")
                return False

    @staticmethod
    def deposit_money(number_card):
        """Deposit money to account"""
        amount = input("Input deposit summ: ")
        with sqlite3.connect("atm.db") as db:
            try:
                cur = db.cursor()
                cur.execute(
                    f"""UPDATE Users_data SET Balance = Balance + {amount} WHERE Number_card = {number_card};""")
                db.commit()
                SQL_atm.info_balance(number_card)
                SQL_atm.report_operation_1(now_data, number_card, "3", amount, "")
            except:
                print("Wrong action with balance")
                return False

    @staticmethod
    def transfer_money(number_card):
        """Transfer money between accounts"""
        account = input("Input number card to transfer money: ")
        if account != number_card:
            result = SQL_atm.input_card(account)
            if result:
                transfer_summ = input("Input summ to transfer: ")
                if int(transfer_summ) > 0:
                    with sqlite3.connect("atm.db") as db:
                        cur = db.cursor()
                        cur.execute(f"""SELECT Balance FROM Users_data WHERE Number_card = {number_card};""")
                        result_info_balance = cur.fetchone()
                        balance_card = result_info_balance[0]
                        try:
                            if int(transfer_summ) > balance_card:
                                print("Account has insufficient funds")
                                return False
                            else:
                                cur.execute(
                                    f"""UPDATE Users_data SET Balance = Balance - {transfer_summ} WHERE Number_card = {number_card};""")
                                cur.execute(
                                    f"""UPDATE Users_data SET Balance = Balance + {transfer_summ} WHERE Number_card = {account};""")
                                db.commit()
                                SQL_atm.info_balance(number_card)
                                SQL_atm.report_operation_1(now_data, number_card, "2", transfer_summ, account)
                                SQL_atm.report_operation_2(now_data, account, "3", transfer_summ, number_card)
                                return True
                        except:
                            print("Wrong action with balance")
                            return False
                else:
                    print("Input correct summ to transfer!")
            else:
                print("There is no user with this card number!")
        else:
            print("Input another user's card number!")

    @staticmethod
    def input_operation(number_card):
        """Operation menu"""
        while True:
            operation = input("Operation menu: \n"
                              "1. Get balance\n"
                              "2. Withdraw money\n"
                              "3. Deposit money\n"
                              "4. Exit\n"
                              "5. Transfer money\n")

            if operation == '1':
                SQL_atm.info_balance(number_card)

            elif operation == '2':
                SQL_atm.withdraw_money(number_card)

            elif operation == '3':
                SQL_atm.deposit_money(number_card)

            elif operation == '4':
                print("Thanks! Goodbye!")
                return False

            elif operation == '5':
                SQL_atm.transfer_money(number_card)

            else:
                print("Wrong operation. Try another operation!")

    @staticmethod
    def report_operation_1(now_date, number_card, type_operation, amount, payee):
        """Operation report:
        1. withdraw money
        2. deposit money
        3. transfer money"""
        user_data = [
            (now_date, number_card, type_operation, amount, payee)
        ]
        with open("report_1.csv", "a", newline='') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerows(
                user_data
            )
        print("Data added to report sender")

    @staticmethod
    def report_operation_2(now_date, payee, type_operation, amount, sender):
        """Operation report:
        1. withdraw money
        2. deposit money
        3. transfer money"""
        user_data = [
            (now_date, payee, type_operation, amount, sender)
        ]
        with open("report_2.csv", "a", newline='') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerows(
                user_data
            )
        print("Data added to report payee")
