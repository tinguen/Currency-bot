import mysql.connector

my_db = mysql.connector.connect(
  host="localhost",
  user="xxxxx",
  passwd="xxxxx"
)

my_cursor = my_db.cursor()


def get_currency(chat_id):
    my_cursor.execute("SELECT currency FROM `bot`.`base_currency` WHERE chat_id={}".format(chat_id))
    row = my_cursor.fetchone()
    if row is None:
        return row
    return row[0]


def set_currency(chat_id, currency):
    if get_currency(chat_id) is not None:
        my_cursor.execute("UPDATE `bot`.`base_currency` SET currency='{}' WHERE chat_id='{}'".format(currency, chat_id))
    else:
        sql = "INSERT INTO `bot`.`base_currency` (chat_id, currency) VALUES (%s, %s)"
        values = (chat_id, currency)
        my_cursor.execute(sql, values)
    my_db.commit()


def add_fav(chat_id, curr1, curr2):
    sql = "INSERT INTO `bot`.`favorite` (chat_id, curr1, curr2) VALUES (%s, %s, %s)"
    values = (chat_id, curr1, curr2)
    my_cursor.execute(sql, values)
    my_db.commit()


def get_fav(chat_id):
    my_cursor.execute("SELECT * FROM `bot`.`favorite` WHERE chat_id={}".format(chat_id))
    arr = []
    row = my_cursor.fetchone()
    while row is not None:
        arr.append(row)
        row = my_cursor.fetchone()
    return arr

