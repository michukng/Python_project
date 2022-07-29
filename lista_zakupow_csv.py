# Lista zakupów
import csv, sys

# Tworzenie nazwy pliku, nagłówka oraz listy, która przechowa naszą listę zakupów
file_name = "shopping.csv"
fieldnames = ["product", "amount", "unit"]
shopping_list = []

# Stworzenie wyjątku, gdyby pliku nie było na komputerze
try:
    with open(file_name, "r") as file:
        file_reader = csv.reader(file, delimiter="\t")
        # Pomijamy zapisanie nagłówka do listy
        next(file_reader)

        for items in file_reader:
            shopping_list.append(items)

except FileNotFoundError:
    with open(file_name, "w", newline="") as file:
        # Tworzenie pliku wraz z nagłówkiem
        write = csv.DictWriter(file, fieldnames=fieldnames, delimiter="\t")
        write.writeheader()

# Zapisanie listy do pliku csv
def writing_to_csv():
    with open(file_name, "w", newline="") as file:
        write = csv.DictWriter(file, fieldnames=fieldnames, delimiter="\t")

        write.writeheader()
        write = csv.writer(file, delimiter="\t")

        for items in shopping_list:
            write.writerow(items)

# Dodawanie produktów do listy zakupów
def add_to_list():
    adding_to_list = []
    checking_product = []

    for products in shopping_list:
        checking_product.append(products[0])
    product = input("Add product to shopping list: ")
    # Sprawdzenie czy produkt występuje w liście sprawdzającej
    if product in checking_product:
        # Jeśli produkt występuje w liście zakupów, program prosi o informację o ile podnieść dany produkt
        while True:
            try:
                how_much = int(input("This product is already in shopping list. How much do you want to increase it? "))
                break
            except ValueError:
                print("You must enter a number!")
        index = checking_product.index(product)
        adding = int(shopping_list[index][1]) + how_much
        shopping_list[index][1] = str(adding)
        writing_to_csv()
        print("Increased your product!")
    else:
        while True:
            try:
                amount = int(input("Amount: "))
                break
            except ValueError:
                print("You must enter a number!")
        unit = input("Unit: ")
        adding_to_list.append(product)
        adding_to_list.append(amount)
        adding_to_list.append(unit)
        shopping_list.append(adding_to_list)
        writing_to_csv()

# Usuniecie produktu z listy
def delete_prodcut():
    for position, items in enumerate(shopping_list, 1):
        print(f"{position}. %s" % items[0])
    while True:
        try:
            delete = int(input("\nWhich one product you want to remove? "))
            break
        except ValueError:
            print("You must enter a number!")
    shopping_list.pop(delete - 1)
    writing_to_csv()
    print("The product has been removed!")

# Wyświetlenie listy zakupów
def show_list():
    with open(file_name, "r") as file:
        file_reader = csv.reader(file, delimiter="\t")
        next(file_reader) #pomijanie nagłówka

        for items in file_reader:
            print("Product %s amount: %s unit: %s" % (items[0], items[1], items[2]))

# Wyświetlenie produktów
def show_products():
    with open(file_name, "r") as file:
        file_reader = csv.DictReader(file, delimiter="\t")
        print("Your products are: ")

        for items in file_reader:
            print(items['product'])


while True:
    try:
        print("""1. Add to list
2. Delete product
3. Show list
4. Show products
5. Exit""")
        user_choice = int(input("Choose number: "))
        if user_choice == 1:
            add_to_list()
        elif user_choice == 2:
            delete_prodcut()
        elif user_choice == 3:
            show_list()
        elif user_choice == 4:
            show_products()
        elif user_choice == 5:
            sys.exit()
        else:
            print("This number does not exist!")
    except ValueError:
        print("You must enter a number!")