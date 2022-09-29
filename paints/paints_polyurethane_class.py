from paints_paints_class import Paints


class PolyurethanePaints(Paints):
    def __init__(self, id, name, capacity, value, first_base, second_base, type_of_paint):
        super().__init__(id, name, capacity, value, first_base, second_base, type_of_paint)