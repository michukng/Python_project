import paints_mysql

class History:
    def __init__(self, coloring_date, paint_id, color_id, counter):
        self.coloring_date = coloring_date
        self.paint_id = paint_id
        self.color_id = color_id
        self.counter = counter

    def adding_to_history(self):
        paints_mysql.mycursor.execute(f"""INSERT INTO coloring_history (coloring_date, paint_id, color_id, amount)
                                                            VALUES ('{self.coloring_date}', {self.paint_id}, {self.color_id}, {self.counter})""")

        paints_mysql.db.commit()    