import mysql.connector
from dotenv import load_dotenv
import os


def quotes(lst):
    for i in range(len(lst)):
        if isinstance(lst[i], float):
            lst[i] = lst[i].__round__(2)
        if not isinstance(lst[i], int) and not isinstance(lst[i], float):
            lst[i] = '"' + str(lst[i]) + '"'
        lst[i] = str(lst[i])
    return lst


class SQLConnect:
    def __init__(self):
        load_dotenv()
        username = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')
        self.conn = mysql.connector.connect(username=username, password=password, host='localhost')
        self.cursor = self.conn.cursor()

    def createDatabase(self, name):
        self.cursor.execute("Drop Database If Exists {}".format(name))
        self.cursor.execute("Create database {}".format(name))
        self.cursor.execute("Use {}".format(name))

    def useDatabase(self, name):
        self.cursor.execute('Use {}'.format(name))

    def createTable(self, name, attributes):
        self.cursor.execute("Create table {} ({})".format(name, ', '.join(attributes)))

    def query(self, query):
        self.cursor.execute(query)

    def fetchOne(self):
        return self.cursor.fetchone()

    def fetchAll(self):
        return self.cursor.fetchall()

    def insertIntoTable(self, name, values):
        self.cursor.execute("Insert into {} VALUES ({})".format(name, ', '.join(quotes(values))))

    def commit(self):
        self.conn.commit()
        self.conn.close()
        self.cursor.close()
