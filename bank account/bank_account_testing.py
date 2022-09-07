# -*- coding: utf-8 -*-
import json, datetime
from urllib.request import urlopen


class BankAccount:
    def __init__(self, login, pin, balance, acc_number):
        self.currency = None
        self._login = login
        self._pin = pin
        self._balance = balance
        self._acc_number = acc_number

    def balance(self):
        return self._balance

    def withdraw_money(self, amount):
        if amount > self._balance or amount < 0:
            print("Brak środków na koncie.")
            return False

        else:
            self._balance -= amount
            print(f"Wypłacono {amount} zł. Stan konta wynosi {self._balance} zł.")

    def deposit_money(self, amount):
        if amount <= 0:
            print("Zła kwota.")
            return False

        else:
            self._balance += amount
            print(f"Wpłacono {amount} zł. Stan konta wynosi {self._balance} zł.")

    def name_and_pin(self):
        return f"Nazwa: {self._login}, pin: {self._pin}"

    def account_number(self):
        return f"Twój numer konta to {self._acc_number}"

    def json_list(self, history):
        list_history = []

        list_history.insert(0, history)

        with open(f"{self._login}.json") as read_file:
            history_adding = json.load(read_file)
            exchange_dict_history = history_adding["other_currency"]
            history_adding = history_adding["history"]

        data_bank_acc = {
            "login": self._login,
            "pin": self._pin,
            "balance": self._balance,
            "acc_number": self._acc_number,
            "history": [],
            "other_currency": []
        }

        for x in list_history:
            history_adding.insert(0, x)

        for x in history_adding:
            data_bank_acc["history"].append(x)

        for i in exchange_dict_history:
            data_bank_acc["other_currency"].append(i)

        with open(f"{self._login}.json", "w") as file:
            json.dump(data_bank_acc, file, indent=2)

    @staticmethod
    def exchange_rates():
        global exchange_dict
        with urlopen("https://api.nbp.pl/api/exchangerates/tables/A?format=json") as response:
            source = response.read()

        data_exchange_rates = json.loads(source)

        exchange_dict = dict()

        for exchange_data in data_exchange_rates[0]["rates"]:
            print(f"Waluta: {exchange_data['currency']}, Kod: {exchange_data['code']}, Kurs: {exchange_data['mid']}")
            name = exchange_data['code']
            rate = exchange_data['mid']
            exchange_dict[name] = rate

    def change_money(self, amount, name_code):
        if amount > self._balance or amount < 0:
            print(f"Zbyt mało środków na koncie")

        else:
            new_amount = float(amount / exchange_dict[name_code])
            new_amount = round(new_amount, 2)
            self._balance = round(self._balance - amount, 2)
            self.currency = round(new_amount, 2)

            other_currency_dict = dict()

            with open(f"{self._login}.json") as read_file:
                data_bank = json.load(read_file)

            try:
                for history_currency in data_bank["other_currency"][0].items():
                    keys, values = history_currency
                    other_currency_dict[keys] = values

                for currency in data_bank["other_currency"][0].keys():
                    if currency == name_code:
                        data_bank["other_currency"][0][name_code] += round(self.currency, 2)
                        break
                    else:
                        other_currency_dict.setdefault(name_code, self.currency)
                        data_bank["other_currency"] = list()
                        data_bank["other_currency"].append(other_currency_dict)
            except IndexError:
                other_currency_dict.setdefault(name_code, self.currency)
                data_bank["other_currency"].append(other_currency_dict)

            with open(f"{self._login}.json", "w") as file:
                json.dump(data_bank, file, indent=2)

            return True


class MoneyTransfer:
    def __init__(self, from_who, to_who, how_much, acc_number):
        self.from_who = from_who
        self.to_who = to_who
        self.how_much = how_much
        self.acc_number = acc_number

    @classmethod
    def date_time(cls):
        cls.date = datetime.datetime.today().strftime("%d-%m-%Y %H:%M")

        return cls.date

    @staticmethod
    def deposit_money(amount):
        return f"{MoneyTransfer.date_time()} Wpłata na konto w wysokości {amount} zł."

    @staticmethod
    def withdraw_money(amount):
        return f"{MoneyTransfer.date_time()} Wypłata z konta w wysokości {amount} zł."

    def exchange_money(self):
        return f"{MoneyTransfer.date_time()} Wymieniłeś {self.from_who} zł na {self.to_who} {self.how_much}"

    def to_what_account(self):
        return f"{MoneyTransfer.date_time()} Przelew przychodzący od {self.from_who} na kwotę {self.how_much} zł."

    def from_what_account(self):
        return f"{MoneyTransfer.date_time()} Przelew wychodzący do {self.to_who} na nr konta {self.acc_number} na kwotę {self.how_much} zł"