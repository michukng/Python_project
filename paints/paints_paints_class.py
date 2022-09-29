# -*- coding: utf-8 -*-
import paints_mysql


class Paints:
    def __init__(self, id, name, capacity, value, first_base, second_base, type_of_paint):
        self.id = id
        self.name = name
        self.capacity = capacity
        self.value = value
        self.first_base = first_base
        self.second_base = second_base
        self.type_of_paint = type_of_paint

    # wyświetlenie potrzebnych pigmentów do zadozowania farby
    @staticmethod
    def show_pigments_to_color(pigments):
        show_pigments = dict()
        for k, v in pigments.items():
            paints_mysql.mycursor.execute(f"""SELECT kolorant.name FROM kolorant
                                            WHERE kolorant.id = {k}
                                            """)

            result = paints_mysql.mycursor.fetchall()

            for row in result:
                print(f"{row[0]} - {v} ml")
                show_pigments[k] = v

        # zwrócenie słownika z ilością i nazwą kolorantów
        return show_pigments

    # # funkcja do odejmowania ilości kolorantu w zbiorniku, który został zadozowany do farby
    # # jeżeli ilość kolorantu w zbiorniku miałby wynieść poniżej 0, to następuje przypisane 0 do zbiornika
    # # ponieważ zbiornik nie może być na minusie
    # @staticmethod
    # def subtract_pigments_from_container(show_pigments):
    #     for k, v in show_pigments.items():
    #         paints_mysql.mycursor.execute(f"""UPDATE containers
    #                                              SET capacity = IF(capacity - {v} < 0, 0, capacity - {v})
    #                                              WHERE kolorant_id = {k}
                                                 
    #                                             """)

    #         paints_mysql.db.commit()


    # funkcja do wyświetlania nazw farb
    @staticmethod
    def show_paints():
        paints_mysql.mycursor.execute("""SELECT name, type_of_paint FROM paints
                                            ORDER BY name""")
        result = paints_mysql.mycursor.fetchall()

        print("Lista farb:")

        for i in result:
            print(f"{i[0]} - rodzaj farby - {i[1]}")