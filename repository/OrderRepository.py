from core.database.Database import Database
from model.Order import Order


class OrderRepository:

    def create(self, order: Order, storage: list):
        query1 = """INSERT INTO orders VALUES(null,%s,%s,NOW())"""
        query2 = """INSERT INTO order_dishes VALUES(null,%s,%s,%s)"""
        query3 = """UPDATE ingredients SET count=%s WHERE id=%s"""

        dishes = []

        with Database() as con:
            con.autocommit = False
            cursor = con.cursor()
            cursor.execute(query1, (order.name, order.sum,))
            idx = cursor.lastrowid
            for dish in order.dishes:
                dishes.append((idx, dish.idx, dish.count))
            cursor.executemany(query2, dishes)

            cursor.executemany(query3, storage)

            con.commit()

        return idx
