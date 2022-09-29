# -*- coding: utf-8 -*-
import paints_mysql


class Color:
    def __init__(self, id, name, which_base, which_second_base):
        self.id = id
        self.name = name
        self.which_base = which_base
        self.which_second_base = which_second_base

    # funkcja sprawdzająca czy obiekt znajduje się w bazie danych
    def check_color_in_database(self):
        paints_mysql.mycursor.execute(f"""SELECT name FROM color
                                        WHERE color.name = '{self.name}'""")
        if paints_mysql.mycursor.fetchone():
            return False
        return True

    # funkcja, która dodaje utworzony kolor do bazy danych
    def add_new_color_to_db(self):
        paints_mysql.mycursor.execute(f"""INSERT INTO color (name, first_base, second_base)
                                        VALUES ('{self.name}', '{self.which_base}', '{self.which_second_base}')""")

        paints_mysql.db.commit()

    # funkcja, która pobiera id koloru z obiektu
    def get_color_id(self):
        paints_mysql.mycursor.execute(f"""SELECT id FROM color
                                        WHERE color.name = '{self.name}'""")

        result = paints_mysql.mycursor.fetchone()

        return result[0]

    # funkcja, która pobiera id kolorantu
    @staticmethod
    def get_kolorant_id(kolorant_name):
        paints_mysql.mycursor.execute(f"""SELECT id FROM kolorant
                                        WHERE kolorant.name = '{kolorant_name}'""")

        result = paints_mysql.mycursor.fetchone()

        return result[0]

    # funkcja, która dodaje ilość kolornatu w celu stworzenia koloru
    def add_pigments_to_db(self):
        color_id = Color.get_color_id(self)
        paints_mysql.mycursor.execute("SELECT name FROM kolorant")

        result = paints_mysql.mycursor.fetchall()

        for row in result:
            print(row[0])

        while True:
            print("Proszę wybrać wpisać nazwę pigmentu, w celu wyjścia z wybierania ilości koloranu, proszę wpisać 'exit'.")
            user_input = input()
            if user_input == 'exit':
                break
            else:
                try:
                    kolorant_id = Color.get_kolorant_id(user_input)
                    print("Proszę podać ilość w ml.")
                    user_quantity = float(input())
                    paints_mysql.mycursor.execute(f"""INSERT INTO color_pigment (color_id, kolorant_id, quantity)
                                                    VALUES ('{color_id}', '{kolorant_id}', '{user_quantity}')""")
                    paints_mysql.db.commit()
                except TypeError:
                    print("Nie ma takiego kolorantu.")

    # funkcja, która na podstawie id koloru pobiera ilość oraz nazwę koloru potrzebne do jego utworzenia
    def take_pigments_from_color(self):
        paints_mysql.mycursor.execute(f"""SELECT kolorant.id, color_pigment.quantity
                                            FROM color_pigment
                                            INNER JOIN kolorant ON kolorant.id = color_pigment.kolorant_id 
                                            INNER JOIN color ON color.id = color_pigment.color_id
                                            WHERE color_id = {self.id}
                                            """)

        result = paints_mysql.mycursor.fetchall()

        pigments_dict = dict()

        for row in result:
            pigments_dict[row[0]] = row[1]

        return pigments_dict

    @staticmethod
    def color_list():
        paints_mysql.mycursor.execute("""SELECT name FROM color
                                        ORDER BY name""")
        result = paints_mysql.mycursor.fetchall()

        print("Lista kolorów:")

        for colors in result:
            print(colors[0])
