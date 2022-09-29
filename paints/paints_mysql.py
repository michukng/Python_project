# import paints_objects
import mysql.connector

# po = paints_objects

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="admin1995",
    database="testforpaints"
)

mycursor = db.cursor()


# mycursor.execute(f"INSERT INTO kolorant (name) VALUES ('{po.Kolorant_01.name}')")
# mycursor.execute(f"INSERT INTO kolorant (name) VALUES ('{po.Kolorant_02.name}')")
# mycursor.execute(f"INSERT INTO kolorant (name) VALUES ('{po.Kolorant_03.name}')")
# mycursor.execute(f"INSERT INTO kolorant (name) VALUES ('{po.Kolorant_04.name}')")
# mycursor.execute(f"INSERT INTO kolorant (name) VALUES ('{po.Kolorant_05.name}')")
# mycursor.execute(f"INSERT INTO kolorant (name) VALUES ('{po.Kolorant_06.name}')")
# mycursor.execute(f"INSERT INTO kolorant (name) VALUES ('{po.Kolorant_07.name}')")
# mycursor.execute(f"INSERT INTO kolorant (name) VALUES ('{po.Kolorant_08.name}')")
# mycursor.execute(f"INSERT INTO kolorant (name) VALUES ('{po.Kolorant_09.name}')")
# mycursor.execute(f"INSERT INTO kolorant (name) VALUES ('{po.Kolorant_10.name}')")
# mycursor.execute(f"INSERT INTO kolorant (name) VALUES ('{po.Kolorant_11.name}')")
# mycursor.execute(f"INSERT INTO kolorant (name) VALUES ('{po.Kolorant_12.name}')")
#
# db.commit()
#
#
# containers_list = [po.Containers_01.__iter__(), po.Containers_02.__iter__(), po.Containers_03.__iter__(),
#                    po.Containers_04.__iter__(), po.Containers_05.__iter__(), po.Containers_06.__iter__(),
#                    po.Containers_07.__iter__(), po.Containers_08.__iter__(), po.Containers_09.__iter__(),
#                    po.Containers_10.__iter__(), po.Containers_11.__iter__(), po.Containers_12.__iter__()]
#
# mycursor.executemany(f"""INSERT INTO containers
#                     (name, capacity, value)
#                      VALUES (%s, %s, %s)""", containers_list)
#
# db.commit()

# mycursor.execute("""UPDATE containers, kolorant
#                     SET containers.kolorant_name = kolorant.name
#                     WHERE containers.id = kolorant.id""")
#
# db.commit()

# color_list = [po.VTV_5750.__iter__(), po.LAR_1007.__iter__(), po.LAR_7016.__iter__(), po.LAR_7035.__iter__()]
#

# mycursor.executemany("""INSERT INTO color (name, first_base, second_base)
#                         VALUES (%s, %s, %s)""", colors_list)
#
# db.commit()
#
# mycursor.execute("""INSERT INTO color_pigment (color_id, kolorant_id, quantity)
#                     VALUES (1, 3, 15)""")
#
# mycursor.execute("""INSERT INTO color_pigment (color_id, kolorant_id, quantity)
#                     VALUES (1, 1, 30)""")
#
# mycursor.execute("""INSERT INTO color_pigment (color_id, kolorant_id, quantity)
#                     VALUES (1, 5, 45)""")
#
# mycursor.execute("""INSERT INTO color_pigment (color_id, kolorant_id, quantity)
#                     VALUES (2, 2, 15.5)""")
#
# mycursor.execute("""INSERT INTO color_pigment (color_id, kolorant_id, quantity)
#                     VALUES (2, 4, 315)""")
#
# mycursor.execute("""INSERT INTO color_pigment (color_id, kolorant_id, quantity)
#                     VALUES (3, 10, 17.6)""")
#
# mycursor.execute("""INSERT INTO color_pigment (color_id, kolorant_id, quantity)
#                     VALUES (3, 9, 13.5)""")
#
# mycursor.execute("""INSERT INTO color_pigment (color_id, kolorant_id, quantity)
#                     VALUES (3, 5, 135)""")
#
# mycursor.execute("""INSERT INTO color_pigment (color_id, kolorant_id, quantity)
#                     VALUES (4, 2, 15.5)""")
#
# mycursor.execute("""INSERT INTO color_pigment (color_id, kolorant_id, quantity)
#                     VALUES (4, 5, 90)""")
#
# mycursor.execute("""INSERT INTO color_pigment (color_id, kolorant_id, quantity)
#                     VALUES (4, 6, 95)""")
#
# mycursor.execute("""INSERT INTO color_pigment (color_id, kolorant_id, quantity)
#                     VALUES (4, 2, 94)""")

# db.commit()
# paints_list = [po.Poliupur_20.__iter__(), po.Poliupur_90.__iter__(), po.Poliumadur_20.__iter__(),
#                po.Poliumadur_90.__iter__(), po.Poliurdicc_30.__iter__(), po.Epoxyrm_primer.__iter__(),
#                po.Epoxydur_primer.__iter__(),
#                po.Impremix.__iter__(), po.Impresol.__iter__()]
#
# mycursor.executemany("""INSERT INTO paints
#                     (id, name, capacity, value, first_base, second_base, type_of_paint)
#                      VALUES (%s, %s, %s, %s, %s, %s, %s)""", paints_list)
#
# db.commit()

