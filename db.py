import sqlite3
from sys import environ
from os import path

__dbpath = environ["DB_PATH"]

__conn = sqlite3.connect(path.abspath(__dbpath))

cursor = __conn.cursor()