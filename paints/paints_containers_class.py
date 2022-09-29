# -*- coding: utf-8 -*-
import paints_mysql


class Containers:
    def __init__(self, id, name, capacity, value, kolorant):
        self.id = id
        self.name = name
        self.capacity = capacity
        self.value = value
        self.kolorant = kolorant

    # funkcja, która poprzez stworzenie odpowiedniego obiektu zbiornika, przypisuje do niego ilośc kolorantu
    # z bazy danych
    def capacity_from_sql(self):
        paints_mysql.mycursor.execute(f"""SELECT name, capacity FROM containers""")
        result = paints_mysql.mycursor.fetchall()

        for x in result:
            k, v = x
            if k == self.name:
                self.capacity = v

    # funkcja dodawania ilości kolorantu do zbiornika
    def adding_amount_to_containers(self, add_amount):
        Containers.capacity_from_sql(self)
        if float(self.capacity) + add_amount > 6000:
            print("Maksymalna ilość w zbiorniku może wynieść 6000ml.")
            return False

        else:
            self.capacity = float(self.capacity) + add_amount
            print(f"Dodano {add_amount} ml do {self.name}.")
            return True

    def containers_capacity(self):
        return f"Pojemność {self.name} wynosi {self.capacity} {self.value}"

    # wyświetlanie ilości oraz nazwy kolorantu w zbiorniku
    @staticmethod
    def show_pigments_in_containers():
        paints_mysql.mycursor.execute("""SELECT containers.name, containers.capacity, containers.value, kolorant.name
                                        FROM containers
                                        INNER JOIN kolorant
                                        WHERE containers.id = kolorant.id""")
        result = paints_mysql.mycursor.fetchall()

        for row in result:
            print(f"{row[0]} - {row[1]} {row[2]} - {row[3]}")

    # funkcja do odejmowania ilości kolorantu w zbiorniku, który został zadozowany do farby
    # jeżeli ilość kolorantu w zbiorniku miałby wynieść poniżej 0, to następuje przypisane 0 do zbiornika
    # ponieważ zbiornik nie może być na minusie
    @staticmethod
    def subtract_pigments_from_container(show_pigments):
        for k, v in show_pigments.items():
            paints_mysql.mycursor.execute(f"""UPDATE containers
                                                 SET capacity = IF(capacity - {v} < 0, 0, capacity - {v})
                                                 WHERE kolorant_id = {k}
                                                 
                                                """)

            paints_mysql.db.commit()