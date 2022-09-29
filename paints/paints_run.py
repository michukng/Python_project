# # -*- coding: utf-8 -*-
import datetime
import sys
from paints_history import History
import paints_mysql
from paints_paints_class import Paints
from paints_colours_class import Color
from paints_polyurethane_class import PolyurethanePaints
from paints_containers_class import Containers
from paints_epoxy_class import EpoxyPaints
from paitns_impregnats_paints import ImpregnatingPaints


# funkcja do dodawania pigmentu do zbiornika w bazie danych
def mysql_add_pigment(how_much, what_id):
    paints_mysql.mycursor.execute(f"""UPDATE containers
                            SET capacity = capacity + {how_much}
                            WHERE containers.id = {what_id}""")

    paints_mysql.db.commit()


# funkcja dodawania pigmentu do zbiornika
def add_pigment():
    # wyświetlanie z tabeli containers i kolorant w bazie danych - nazwy zbiornika, aktualnej ilości pigmentu w tym
    # zbiorniku, jednostki miary oraz nazwy kolorantu
    paints_mysql.mycursor.execute("""SELECT containers.name, containers.capacity, containers.value, kolorant.name
                                FROM containers
                                INNER JOIN kolorant
                                ON containers.kolorant_id = kolorant.id""")
    result = paints_mysql.mycursor.fetchall()

    for row in result:
        print(f"{row[0]} - {row[1]} {row[2]} - {row[3]}")

    while True:
        try:
            # wybranie zbiornika, do którego chcemy dodać pigment
            what_name = input("Do którego zbiornika chcesz dodać pigment? ")

            while True:
                try:
                    how_much = float(input("Ile ml dodać do zbiornika? "))
                    how_much = round(how_much, 2)
                    break
                except ValueError:
                    print("Błędna ilość.")

            # pobranie z bazy danych informacji o zbiorniku
            paints_mysql.mycursor.execute(f"SELECT * FROM containers WHERE name = '{what_name.capitalize()}'")
            result = paints_mysql.mycursor.fetchone()

            # utworzenie obiektu zbiornik
            container = Containers(result[0], result[1], result[2], result[3], result[4])

            # jeśli funkcja zwraca wartość False to następuje pass
            if not container.adding_amount_to_containers(how_much):
                pass
            else:
                # jeśli funkcja zwraca wartość True to zbiornik zostaje zaaktualizowany
                paints_mysql.mycursor.execute(f"""UPDATE containers
                                            SET capacity = {container.capacity}
                                            WHERE name = '{what_name}'""")

                paints_mysql.db.commit()
            break
        except TypeError:
            print("Błędny zbiornik.")


# funkcja do utworzenia nowego koloru przez użytkownika
def new_color():
    print("Do utworzenia nowego koloru, proszę podać: ")

    while True:
        # podanie nazwy koloru
        name_color = input("Nazwa koloru: ")
        name_color = name_color.upper()
        # utworzenie obiektu tylko i wyłącznie z nazwą koloru
        color = Color(None, name_color, None, None)

        # jeżeli funkcja zwraca wartość False, następuje wyświetlenie informacji, iż taki kolor istnieje
        if not color.check_color_in_database():
            print("Taki kolor już istnieje.")
        else:
            # jeżeli funkcja zwraca wartość True
            while True:
                first_base = input("Nazwa bazy (TCH, TVH, TCW): ")
                first_base = first_base.upper()
                print(first_base)

                if first_base == "TCH":
                    second_base = "TCL"
                    # tym razem utworzenie pełnego obiektu i dodanie nowego koloru do bazy danych razem
                    # z podanymi kolorantami i ich ilościami
                    color = Color(None, name_color, first_base, second_base)
                    color.add_new_color_to_db()
                    color.add_pigments_to_db()
                    break

                elif first_base == "TVH":
                    second_base = "TAL"
                    color = Color(None, name_color, first_base, second_base)
                    color.add_new_color_to_db()
                    color.add_pigments_to_db()
                    break

                elif first_base == "TCW":
                    color = Color(None, name_color, first_base, None)
                    color.add_new_color_to_db()
                    color.add_pigments_to_db()
                    break

                else:
                    print("Błędna baza.")
        break


# funkcja sprawdzająca czy jest taka farba w bazie danych
def checking_paint(paint_name):
    paints_mysql.mycursor.execute(f"""SELECT name FROM paints
                                    WHERE name = '{paint_name}'""")

    if paints_mysql.mycursor.fetchall():
        return True
    return False


# funkcja wyświetlająca kolory na podstawie otrzymanej bazy farby
def show_colors_base(first_base, second_base):
    # kolory, które w bazie danych mają bazy farb, zostają dodane do listy
    show_colors_base.list_color_to_pigment = list()
    paints_mysql.mycursor.execute(f"""SELECT name from color
                                    WHERE first_base = '{first_base}' 
                                    OR first_base = '{second_base}'
                                    OR second_base = '{second_base}'
                                    OR second_base = '{first_base}'
                                    ORDER BY name""")

    result = paints_mysql.mycursor.fetchall()

    print("Proszę wybrać kolor")
    for name in result:
        print(name[0])
        show_colors_base.list_color_to_pigment.append(name[0])


# funkcja do utworzenia klasy farby wybranej przez użytkownika
def which_paint(paint_name):
    # przechwycenie z bazy danych nazwy farby
    paints_mysql.mycursor.execute(f"""SELECT * FROM paints
                                    WHERE name = '{paint_name}'
                                    ORDER BY name""")
    result = paints_mysql.mycursor.fetchone()

    # jeżeli w kolumnie type_paint farba ma przypisaną nazwę "poliuretanowa" - następuje utworzenie obiektu
    # farby poliuretanowej
    if result[6] == "Poliuretanowa":
        paint = PolyurethanePaints(result[0], result[1], result[2], result[3], result[4], result[5], result[6])
        # przekazanie do funkcji kody baz farby
        show_colors_base(paint.first_base, paint.second_base)
    # jeżeli w kolumnie type_paint farba ma przypisaną nazwę "epoksydowa" - następuje utworzenie obiektu
    # farby epoksydowej
    elif result[6] == "Epoksydowa":
        paint = EpoxyPaints(result[0], result[1], result[2], result[3], result[4], result[5], result[6])
        show_colors_base(paint.first_base, paint.second_base)
    # jeżeli w kolumnie type_paint farba ma przypisaną nazwę "impregnat" - następuje utworzenie obiektu
    # farby impregnat
    elif result[6] == "Impregnat":
        paint = ImpregnatingPaints(result[0], result[1], result[2], result[3], result[4], result[5], result[6])
        show_colors_base(paint.first_base, paint.second_base)

    return paint


# funkcja do stworzenia obiektu koloru, w celu przechwycenia bazy farby (TCL, TAL, itd.) do wyświetlenia jaką bazę farby
# podstawic pod dozownik
def make_color_to_add_pigment(name_color):
    paints_mysql.mycursor.execute(f"""SELECT * FROM color
                                    WHERE color.name = '{name_color}'""")
    result = paints_mysql.mycursor.fetchone()

    color = Color(result[0], result[1], result[2], result[3])

    return color


# sprawdzanie pojemności zbiorników
def checking_container_capacity(pigments):
    for k, v in pigments.items():
        paints_mysql.mycursor.execute(f"""SELECT containers.name, containers.capacity 
                                        FROM containers
                                        WHERE containers.kolorant_id = {k}""")

        result = paints_mysql.mycursor.fetchall()

        # jeżeli w zbiorniku, w którym znajduje się kolorant potrzebny do stworzenia zakolorowanej farby
        # jego ilość jest mniejsza niż 1500ml program wyświetli nam informacje
        for row in result:
            if row[1] < 1500:
                print(f"Za mało pigmentu w {row[0]}!")


# funkcja do utworzenia daty, w celu dodania jej do historii dozowania
def today_date():
    date_now = datetime.date.today()
    date_now = date_now.strftime("%Y-%m-%d")
    return date_now


# funkcja do zapigmentowania farby
def add_pigment_to_paint():
    Paints.show_paints()

    print("W celu zapigmentowania farby proszę wpisać jej nazwę: ")

    while True:
        choose_paint = input()

        # funkcja informuje nas poprzez zwrócenie wartości False, że nie ma takiej farby w bazie danych
        if not checking_paint(choose_paint.title()):
            print("Błędna nazwa.")
        else:
            # przypisanie do zmiennej paint, zwróconej wartości z funkcji which_paint(), w której wartośc zwracana
            # to utworzony obiekt farby
            paint = which_paint(choose_paint)
            print("Proszę wybrać kolor:")

            while True:
                choose_color = input()
                # jeżeli kolor występuje w liście z funkcji show_colors_base
                # to następuje przypisanie bazy farby koloru do bazy farby poprzez zmienną x
                # w celu wyświetlenia informacji jaką bazę farby podstawić do dozowania
                if choose_color.upper() in show_colors_base.list_color_to_pigment:
                    color = make_color_to_add_pigment(choose_color)
                    if color.which_base == paint.first_base:
                        x = paint.first_base
                    elif color.which_second_base == paint.second_base:
                        x = paint.second_base
                    elif color.which_second_base == paint.first_base:
                        x = paint.first_base
                    elif color.which_base == paint.second_base:
                        x = paint.second_base
                    print("Proszę podać ilość puszek farby do zadozowania:")
                    while True:
                        try:
                            amount = int(input())
                            break
                        except ValueError:
                            print("Błędna ilość")
                    counter = 0

                    # odliczanie ilości podanej przez użytkownika
                    while counter < amount:
                        pigments = color.take_pigments_from_color()
                        print(f"Proszę podstawić farbę pod dozownik: {paint.name} w bazie {x}.")
                        print(f"Do końca zadania zostało {amount - counter} szt.")
                        # sprawdzanie stanu kolorantu w zbiorniku
                        checking_container_capacity(pigments)
                        # wyświetlena informacja o ilości i nazwie pigmentów z funkcji w klasie Paints
                        # potrzebnej do utworzenia zakolorowanej farby
                        show_pigments = paint.show_pigments_to_color(pigments)
                        print("Wpisz 'dozuj', bądź 'anuluj'.")
                        user_choice = input()
                        if user_choice.lower() == "dozuj":
                            # odjęcie pigmentów w bazie danych
                            Containers.subtract_pigments_from_container(show_pigments)
                            counter += 1

                        elif user_choice.lower() == "anuluj":
                            break
                        else:
                            print("Błędna opcja")
                    # jeżeli żadna farba nie została zadozowana to nastepuje wyjście z pętli bez zapisu do bazy danych
                    # informacji o utworzeniu farby w kolorze i jej ilości
                    if counter == 0:
                        break
                    else:
                        # jeżeli chociaż jedna farba została zadozowana to następuje zapisanie jej do historii
                        # w bazie danych oraz wyświetlenie informacji użytkownikowi ilości zapigmentowanych farb
                        coloring_date = today_date()
                        history = History(coloring_date, paint.id, color.id, counter)
                        history.adding_to_history()
                        print(f"Zadozowano {counter} szt {paint.name} na kolor {choose_color}.")
                        break
                else:
                    print("Błędny kolor.")
            break


# funkcja do wyświetlania historii farb
def show_history():
    paints_mysql.mycursor.execute("""SELECT coloring_history.coloring_date, paints.name, color.name, coloring_history.amount
                                    FROM coloring_history
                                    INNER JOIN paints ON coloring_history.paint_id = paints.id
                                    INNER JOIN color ON coloring_history.color_id = color.id""")

    result = paints_mysql.mycursor.fetchall()

    for row in result:
        print(f"{row[0]} - {row[1]} - {row[2]} - {row[3]} szt")


def main():
    while True:
        print("""Dozownik farb
Proszę wybrać opcje:

1. Lista farb.
2. Lista kolorów.
3. Dodaj pigment.
4. Stwórz nowy kolor.
5. Zapigmentuj farbę.
6. Stan pigmentów w zbiorniku.
7. Historia pigmentowania.
8. Wyjdź.""")
        try:
            user_choice = int(input())

            if user_choice == 1:
                Paints.show_paints()
                print("\n")

            elif user_choice == 2:
                Color.color_list()
                print("\n")

            elif user_choice == 3:
                add_pigment()
                print("\n")

            elif user_choice == 4:
                new_color()
                print("\n")

            elif user_choice == 5:
                add_pigment_to_paint()
                print("\n")

            elif user_choice == 6:
                Containers.show_pigments_in_containers()
                print("\n")

            elif user_choice == 7:
                show_history()
                print("\n")

            elif user_choice == 8:
                sys.exit()

            else:
                print("Błędna opcja.")
        except ValueError:
            print("Błędna opcja.")


if __name__ == "__main__":
    main()