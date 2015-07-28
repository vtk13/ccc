import mysql.connector
import psycopg2
import datetime


con_my = mysql.connector.connect(user='root', database='cc')
cc = con_my.cursor(buffered=True)

con_pg = psycopg2.connect("dbname=ccc user=postgres")
ccc = con_pg.cursor()

ccc.execute('DELETE FROM goods_unit')
cc.execute('SELECT * FROM units')
max = 0
for (id, title) in cc:
    ccc.execute('INSERT INTO goods_unit (id, title) VALUES(%s, %s)', (id, title))
    if id > max:
        max = id
ccc.execute('ALTER SEQUENCE goods_unit_id_seq RESTART WITH %s', (max + 1,))

ccc.execute('DELETE FROM goods_good')
cc.execute('SELECT id, bar_code, title, unit, packed, pack_volume FROM goods')
max = 0
for (id, bar_code, title, unit, packed, pack_volume) in cc:
    if unit == 0:
        unit = 1
    packed = (packed == 1)
    ccc.execute('INSERT INTO goods_good (id, bar_code, title, unit_id, packed, pack_volume) VALUES(%s, %s, %s, %s, %s, %s)', (id, bar_code, title, unit, packed, pack_volume))
    if id > max:
        max = id
ccc.execute('ALTER SEQUENCE goods_good_id_seq RESTART WITH %s', (max + 1,))


ccc.execute('DELETE FROM goods_shop')
cc.execute('SELECT id, address_id, title FROM shops')
max = 0
for (id, address_id, title) in cc:
    ccc.execute('INSERT INTO goods_shop (id, address, title) VALUES(%s, %s, %s)', (id, address_id, title))
    if id > max:
        max = id
ccc.execute('ALTER SEQUENCE goods_shop_id_seq RESTART WITH %s', (max + 1,))


ccc.execute('DELETE FROM goods_cost')
cc.execute('SELECT id, good_id, shop_id, user_id, timestamp, cost, amount FROM sales')
max = 0
for (id, good_id, shop_id, user_id, timestamp, cost, amount) in cc:
    timestamp = datetime.datetime.fromtimestamp(timestamp)
    ccc.execute('INSERT INTO goods_cost (id, good_id, shop_id, user_id, timestamp, cost, amount, discount) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)', (id, good_id, shop_id, user_id, timestamp, cost, amount, False))
    if id > max:
        max = id
ccc.execute('ALTER SEQUENCE goods_cost_id_seq RESTART WITH %s', (max + 1,))

con_pg.commit()

con_my.close()
con_pg.close()
