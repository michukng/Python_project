# -*- coding: utf-8 -*-
import paints_mysql


class Pigments:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __iter__(self):
        return self.id, self.name