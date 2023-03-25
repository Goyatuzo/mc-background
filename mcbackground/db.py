import sqlite3
from .servernet import mounting_dir
from os import path

conn = sqlite3.connect(path.join(mounting_dir, "data", "instance.db"))