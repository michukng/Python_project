# -*- coding: utf-8 -*-
import bank_account_testing, sys, os.path, random, json


def login():
    global bank_acc
    while True:
        login_acc = input("Proszę o podanie loginu: ")

        if login_acc == 'rejestracja':
            register()
            break

        elif login_acc == 'exit':
            sys.exit()

        while True:
            try:
                pin = int(input("Proszę o podanie pinu: "))
                break

            except ValueError:
                print("Błędny pin.")

        try:
            with open(f"{login_acc}.json", "r") as file:
                acc_data = json.load(file)

                bank_acc = bank_account_testing.BankAccount(acc_data["login"], acc_data["pin"], float(acc_data["balance"]),
                                                                                                acc_data["acc_number"])

                if pin == int(bank_acc._pin):
                    break

                else:
                    print("Zły login lub pin.")
                    print("Jeśli Pan/Pani nie posiada u nas konta, prosimy wpisać 'rejestracja' w celu założenia konta")
                    print("Żeby zakończyć działanie programu prosimy wpisać 'exit'")

        except FileNotFoundError:
            print("Zły login lub pin.")
            print("Jeśli Pan/Pani nie posiada u nas konta, prosimy wpisać 'rejestracja' w celu założenia konta")
            print("Żeby zakończyć działanie programu prosimy wpisać 'exit'")


def adding_json():
    try:
        with open(f"{bank_acc._login}.json") as read_file:
            history_adding = json.load(read_file)
            history_adding = history_adding["history"]

        data_bank_acc = {
            "login": bank_acc._login,
            "pin": bank_acc._pin,
            "balance": bank_acc._balance,
            "acc_number": bank_acc._acc_number,
            "history": [],
            "other_currency": []
        }

        for history in history_adding:
            data_bank_acc["history"].append(history)

        with open(f"{bank_acc._login}.json", "w") as file:
            json.dump(data_bank_acc, file, indent=2)

    except FileNotFoundError:
        data_bank_acc = {
            "login": bank_acc._login,
            "pin": bank_acc._pin,
            "balance": bank_acc._balance,
            "acc_number": bank_acc._acc_number,
            "history": [],
            "other_currency": []
        }

        with open(f"{bank_acc._login}.json", "w") as file:
            json.dump(data_bank_acc, file, indent=2)


def reading_json():
    with open(f"{bank_acc._login}.json") as read_file:
        read_history = json.load(read_file)

        for history in read_history["history"]:
            print(history)


def reading_json_currency():
    with open(f"{bank_acc._login}.json") as read_file:
        read_currency = json.load(read_file)

        for currency in read_currency["other_currency"][0].items():
            keys, values = currency
            print(f"{keys}: {values}")


def register():
    global bank_acc
    print("W celu założenia konta internetowego, prosimy o podanie loginu, który składa się z 2 liter oraz 4 cyfr: ")

    while True:
        login_acc = input()

        if len([x for x in login_acc if x.isdigit()]) != 4 or len([x for x in login_acc if x.isalpha()]) != 2:
            print("Za mało liter bądź cyfr.")

        elif os.path.exists(f"{login_acc}.json"):
            print("Takie konto już istnieje.")
            print("Proszę podać nowy login.")

        else:
            break

    while True:

        pin = input("Proszę o podanie pinu złożonego z 4 liczb: ")

        if len([x for x in pin if x.isdigit()]) != 4:
            print("Zły pin")

        else:
            break

    bank_acc = login_acc

    acc_number = 6299403450

    for x in range(4):
        random_acc_number = random.randint(1, 9999)

        while len(str(random_acc_number)) < 4:
            random_acc_number = str(random_acc_number)
            random_acc_number += "0"
            random_acc_number = random_acc_number[::-1]

        acc_number = str(acc_number) + str(random_acc_number)

    while True:
        try:
            with open("numbers_of_all_accounts.json") as file_read:
                checking_numbers = json.load(file_read)
                for data in checking_numbers['account']:
                    if str(acc_number) in data['acc_number']:
                        for x in range(4):
                            random_acc_number = random.randint(1, 9999)

                            while len(str(random_acc_number)) < 4:
                                random_acc_number = str(random_acc_number)
                                random_acc_number += "0"
                                random_acc_number = random_acc_number[::-1]

                            acc_number = str(acc_number) + str(random_acc_number)

                else:
                    with open("numbers_of_all_accounts.json") as read_file:
                        number_accounts = json.load(read_file)

                        number_accounts["account"].append({
                            "login": login_acc,
                            "acc_number": acc_number
                        })

                    with open("numbers_of_all_accounts.json", "w") as new_file:
                        json.dump(number_accounts, new_file, indent=2)

                    break

        except FileNotFoundError:
            with open("numbers_of_all_accounts.json", "w") as new_file:

                number_accounts = {
                    "account": [
                        {
                            "login": login_acc,
                            "acc_number": acc_number
                        }
                    ]
                }

                json.dump(number_accounts, new_file, indent=2)

        break

    bank_acc = bank_account_testing.BankAccount(login_acc, pin, balance=0, acc_number=acc_number)

    adding_json()
    print(f"Konto o nazwie {bank_acc._login} zostało założone.")


def transfer():
    while True:
        user_choice_account = input("Proszę o podanie numeru konta, na który przelać pieniądze: ")

        if len([x for x in user_choice_account if x.isdigit()]) != 26:
            print("Błędny numer konta.")

        else:
            with open("numbers_of_all_accounts.json") as read_file:
                chcecking_number_account = json.load(read_file)

            for data_account in chcecking_number_account["account"]:
                if user_choice_account in data_account["acc_number"]:
                    name_account = data_account["login"]
                    while True:
                        try:
                            user_choice_amount = float(input("Jaką kwotę przelać na to konto? "))


                            if user_choice_amount > bank_acc._balance:
                                print("Brak środków na koncie.")

                            elif user_choice_amount < 0:
                                print("Błędna kwota.")

                            else:
                                new_transfer = bank_account_testing.MoneyTransfer(bank_acc._login, name_account, user_choice_amount, user_choice_account)
                                with open(f"{name_account}.json") as read_file:
                                    data_bank_acc = json.load(read_file)

                                    data_bank_acc["balance"] += user_choice_amount

                                data_bank_acc["history"].insert(0, new_transfer.to_what_account())

                                with open(f"{name_account}.json", "w") as file:
                                    json.dump(data_bank_acc, file, indent=2)

                                bank_acc._balance -= user_choice_amount

                                bank_acc.json_list(new_transfer.from_what_account())

                                print(f"Przelałeś {user_choice_amount} zł na konto {user_choice_account}. Twoje saldo wynosi: {bank_acc._balance} zł.")
                            break

                        except ValueError:
                            print("Zła kwota.")

                    break
            else:
                print("Nie ma takiego numeru konta.")
        break


def change_pin():
    while True:
        new_pin = input("W celu zmiany pinu, proszę podać nowy pin składający się z 4 cyfr: ")

        if len([x for x in new_pin if x.isdigit()]) != 4:
            print("Zły pin.")

        else:
            break

    bank_acc._pin = new_pin
    adding_json()

    print(f"Twój nowy pin to {new_pin}.")


def exchange():
    bank_acc.exchange_rates()

    while True:
        try:
            name_code = input("\nW celu wymiany waluty proszę o podanie kodu waluty: ")
            name_code = name_code.upper()

            amount_to_change = float(input("Jaką kwotę wymienić? "))

            if not bank_acc.change_money(amount_to_change, name_code):
                break
            else:
                changing_money_transfer = bank_account_testing.MoneyTransfer(amount_to_change, bank_acc.currency, name_code, None)
                bank_acc.json_list(bank_account_testing.MoneyTransfer.exchange_money(changing_money_transfer))
            break
        except KeyError:
            print("Nie ma takiej waluty.")
        except ValueError:
            print("Błędna kwota")


while True:
    print("Witamy w bankowości internetowej.")
    print("Czy posiada Pan/Pani u nas konto? T/N: ")

    user_choice = input()
    user_choice = user_choice.upper()

    if user_choice == "T":
        login()
        while True:
            print("""1. Saldo.
2. Wpłata gotówki.
3. Wypłata gotówki.
4. Przelew.
5. Wyświetlenie nazwy i pinu.
6. Wyświetlenie numeru konta.
7. Zmiana pinu.
8. Historia przelewów.
9. Kursy walut.
10. Wymiana walut.
11. Pogląd innych walut.
12. Wyjście z programu.""")

            try:
                user_choice = int(input())
            except ValueError:
                print("Proszę o podanie liczby.")

            if user_choice == 1:
                print(f"Twój stan konta: {bank_acc.balance()} zł.")

            elif user_choice == 2:
                while True:
                    try:
                        amount = float(input("Ile pieniędzy wpłacić? "))
                        if bank_acc.deposit_money(amount) == False:
                            break
                        else:
                            transfer_adding_history_deposit = bank_account_testing.MoneyTransfer.deposit_money(amount)
                            bank_acc.json_list(transfer_adding_history_deposit)
                            break
                    except ValueError:
                        print("Podana kwota jest kwotą nieprawidłową.")

            elif user_choice == 3:
                while True:
                    try:
                        amount = float(input("Ile pieniędzy wypłacić? "))
                        if bank_acc.withdraw_money(amount) == False:
                            break
                        else:
                            transfer_adding_history_withdraw = bank_account_testing.MoneyTransfer.withdraw_money(amount)
                            bank_acc.json_list(transfer_adding_history_withdraw)
                            break
                    except ValueError:
                        print("Podana kwota jest kwotą nieprawidłową.")

            elif user_choice == 4:
                transfer()

            elif user_choice == 5:
                print(bank_acc.name_and_pin())

            elif user_choice == 6:
                print(bank_acc.account_number())

            elif user_choice == 7:
                change_pin()

            elif user_choice == 8:
                reading_json()

            elif user_choice == 9:
                bank_acc.exchange_rates()

            elif user_choice == 10:
                exchange()

            elif user_choice == 11:
                reading_json_currency()

            elif user_choice == 12:
                sys.exit()

    elif user_choice == "N":
        register()

    else:
        print("Zła opcja.")