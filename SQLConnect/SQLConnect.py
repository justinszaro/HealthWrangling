import mysql.connector
from dotenv import load_dotenv
import os


class SQLConnect:
    def __init__(self):
        load_dotenv()
        username = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')
        self.conn = mysql.connector.connect(username=username, password=password, host='localhost')
        self.cursor = self.conn.cursor()

    def createDatabase(self):
        self.cursor.execute('DROP DATABASE IF EXISTS Justin\'s Health')
        self.cursor.execute('CREATE DATABASE Justin\'s Health')
        self.cursor.execute('USE Justin\'s Health')

    def createTables(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS appleWatch')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS fitIndex (dates date, bodyMassIndex varchar(255), bodyMass '
                            'varchar(255), bodyFatPercentage varchar(255), leanBodyMass varchar(255), '
                            'basalEnergyBurned varchar(255)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS hidrate')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS iPhone')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS myFitnessPal')

    def appleWatchColumns(self):
        self.cursor.execute('')

    def fitIndexColumns(self):
        pass

    def hidrateColumns(self):
        pass

    def iPhoneColumns(self):
        pass

    def myFitnessPalColumns(self):
        pass


