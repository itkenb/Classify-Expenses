import os
import sqlite3

class Model:
    """- Initiates with creating database and inserting required data.
    - Handles storing keywords into the database"""
    def __init__(self):
        self.conn = sqlite3.connect('Expenses.db')
        self.c = self.conn.cursor()
        self.c.execute("""SELECT name FROM sqlite_master WHERE type='table';""")

        if len(self.c.fetchall()) == 0:
            self.create_class_tbl()
            self.create_subclass_tbl()
            self.create_keywords_tbl()
            self.conn.commit()

        # self.category = [
        #     "502 TAXES",
        #     "503 FIDUCIARY FEES & SERVICES",
        #     "504 CONTRIBUTIONS 505 ACCOUNTING & TAX PREPARATION",
        #     "506 LEGAL SERVICES 31 CHART OF ACCOUNTS EXPENSES - OTHER"
        # ]

    def create_class_tbl(self):
        """Creates class table and inserts default values"""
        self.c.execute("""CREATE TABLE IF NOT EXISTS class (
                        class_id INTEGER PRIMARY KEY,
                        class_name TEXT)""")

        self.c.execute("""INSERT OR REPLACE INTO class (class_id, class_name)
                        VALUES (1, 'PERSONAL'), (2, 'TRUST')""")


    def create_subclass_tbl(self):
        """Creates subclass table and inserts default values"""
        self.c.execute("""CREATE TABLE IF NOT EXISTS subclass (
                        subclass_id INTEGER PRIMARY KEY,
                        subclass_name TEXT)""")

        with open("subclasses.txt", "r", encoding="utf-8") as f:
            for idx, subclass in enumerate(f):
                sql = """INSERT OR REPLACE INTO subclass (
                subclass_id, subclass_name)
                VALUES(?, ?)"""
                self.c.execute(sql, (idx + 1, subclass.strip()))

    def create_keywords_tbl(self):
        """Creates keywords table"""
        self.c.execute("""CREATE TABLE IF NOT EXISTS keywords (
                        keyword_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        keyword_name TEXT,
                        class_id INTEGER,
                        subclass_id INTEGER,
                        FOREIGN KEY(class_id) REFERENCES class(class_id),
                        FOREIGN KEY(subclass_id) REFERENCES subclass(subclass_id))""")

    def get_all_keywords(self):
        sql = """SELECT keyword_name, class_name, subclass_name,
        LENGTH(keyword_name) as lngt FROM keywords
        INNER JOIN class ON keywords.class_id = class.class_id
        INNER JOIN subclass ON keywords.subclass_id = subclass.subclass_id
        ORDER BY lngt DESC"""

        self.c.execute(sql)

        return self.c.fetchall()

    def get_class_name(self, class_id):
        sql = """SELECT class_name FROM class WHERE class_id=? """
        self.c.execute(sql, (class_id, ))
        return self.c.fetchone()

    def get_subclass_name(self, subclass_id):
        sql = """SELECT subclass_name FROM subclass WHERE subclass_id=? """
        self.c.execute(sql, (subclass_id, ))
        return self.c.fetchone()

    def add_keyword(self, keyword_name, class_id, subclass_id):
        sql = """INSERT INTO keywords (
        keyword_name, class_id, subclass_id)
        VALUES (?, ?, ?)"""

        self.c.execute(sql, (keyword_name, class_id, subclass_id))
        self.conn.commit()
