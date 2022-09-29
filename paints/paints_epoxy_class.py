from paints_paints_class import Paints
import paints_mysql


class EpoxyPaints(Paints):
    def __init__(self, id, name, capacity, value, first_base, second_base, type_of_paint):
        super().__init__(id, name, capacity, value, first_base, second_base, type_of_paint)

    # funkcja, która mno¿y iloœæ potrzebnego pigmentu do zadozowania farby razy 1.5
    @staticmethod
    def show_pigments_to_color(pigments):
        show_pigments = dict()
        for k, v in pigments.items():
            paints_mysql.mycursor.execute(f"""SELECT kolorant.name FROM kolorant
                                                WHERE kolorant.id = {k}
                                                """)

            result = paints_mysql.mycursor.fetchall()

            for row in result:
                print(f"{row[0]} - {round(float(v) * 1.5, 2)} ml")
                show_pigments[k] = round(float(v) * 1.5, 2)

        return show_pigments
