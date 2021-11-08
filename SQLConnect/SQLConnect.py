import mysql.connector
import dotenv
import os

dotenv.load_dotenv()

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

conn = mysql.connector.connect(username=username, password=password, host='localhost')
cursor = conn.cursor()
