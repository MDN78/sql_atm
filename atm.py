from sql_query import SQL_atm


class ATM():

    def atm_logic(self):
        SQL_atm.create_table()
        # SQL_atm.insert_users((1234, 1111, 10000))
        number_card = input("Input your card number: ")
        while True:
            if SQL_atm.input_card(number_card):
                if SQL_atm.input_code(number_card):
                    SQL_atm.info_balance(number_card)
                    SQL_atm.withdraw_money(number_card)
                    break
                else:
                    break
            else:
                break


start = ATM()
start.atm_logic()
