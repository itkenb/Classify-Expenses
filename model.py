import os
import sqlite3

class Model:
    def __init__(self):
        self.conn = sqlite3.connect('Expenses.db')
        self.c = self.conn.cursor()
        self.check_tables()

        # self.category = [
        #     "502 TAXES",
        #     "503 FIDUCIARY FEES & SERVICES",
        #     "504 CONTRIBUTIONS 505 ACCOUNTING & TAX PREPARATION",
        #     "506 LEGAL SERVICES 31 CHART OF ACCOUNTS EXPENSES - OTHER"
        # ]

    def check_tables(self):
        self.c.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
        if len(self.c.fetchall()) == 0:
            self.create_classes_tbl()
            self.create_subclasses_tbl()
            self.create_bnk_accts_tbl()
            self.create_keywords_tbl()
            self.insert_classes()
            self.insert_subclasses()
            self.create_expenses_tbl()
            self.conn.commit()

    def insert_classes(self):
        sql = """INSERT OR REPLACE INTO classes (
        class_id, class_name) VALUES (1, 'PERSONAL'),
        (2, 'TRUST')"""
        self.c.execute(sql)

    def insert_subclasses(self):
        sql = """INSERT OR REPLACE INTO subclasses (
        subclass_id, subclass_name) VALUES (?, ?)"""

        with open("subclasses.txt", "r", encoding="utf-8") as f:
            for idx, subclass in enumerate(f):
                self.c.execute(sql, (idx + 1, subclass.strip()))
    
    def create_keywords_tbl(self):
        sql = """CREATE TABLE IF NOT EXISTS keywords (
        keyword_id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword_name TEXT,
        class_id INTEGER,
        subclass_id INTEGER,
        FOREIGN KEY(class_id) REFERENCES classes(class_id),
        FOREIGN KEY(subclass_id) REFERENCES subclasses(subclass_id))"""
        self.c.execute(sql)

    def create_expenses_tbl(self):
        sql = """CREATE TABLE IF NOT EXISTS expenses (
        expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
        expense_date TEXT,
        expense_description TEXT,
        expense_amount REAL,
        bnk_acct_id INTEGER,
        keyword_id INTEGER,
        FOREIGN KEY(bnk_acct_id) REFERENCES bnk_accts(bnk_acct_id),
        FOREIGN KEY(keyword_id) REFERENCES keywords(keyword_id))
        """
        self.c.execute(sql)

    def create_bnk_accts_tbl(self):
        sql = """CREATE TABLE IF NOT EXISTS bnk_accts (
        bnk_acct_id INTEGER PRIMARY KEY AUTOINCREMENT,
        bnk_acct_name TEXT)"""
        self.c.execute(sql)

    def create_subclasses_tbl(self):
        sql = """CREATE TABLE IF NOT EXISTS subclasses (
        subclass_id INTEGER PRIMARY KEY,
        subclass_name TEXT)"""
        self.c.execute(sql)

    def create_classes_tbl(self):
        sql = """CREATE TABLE IF NOT EXISTS classes (
        class_id INTEGER PRIMARY KEY,
        class_name TEXT)"""
        self.c.execute(sql)

    def add_bnk_acct(self, bnk_acct_name):
        check_rowid = self.get_bnk_acct_by_name(bnk_acct_name)

        if  check_rowid is None:
            sql = """INSERT OR REPLACE INTO bnk_accts (bnk_acct_name)
            VALUES (?)"""
            self.c.execute(sql, (bnk_acct_name, ))
            check_rowid = self.c.lastrowid
            self.conn.commit()
            return check_rowid
        else:
            return check_rowid[0]

    def get_bnk_acct_by_name(self, bnk_acct_name):
        sql = """SELECT bnk_acct_id FROM bnk_accts WHERE bnk_acct_name = ?"""
        self.c.execute(sql, (bnk_acct_name, ))
        return self.c.fetchone()

    def add_expense(self, expense):
        sql = """INSERT INTO expenses (
        expense_date, expense_description,
        expense_amount, bnk_acct_id)
        VALUES (?, ?, ?, ?)"""
        self.c.execute(sql, (expense[0], expense[1], float(expense[2]), expense[3]))
        self.conn.commit()

    def get_unsorted_epxenses(self):
        sql = """SELECT * FROM expenses WHERE
        keyword_id IS NULL AND expense_amount > 0"""
        self.c.execute(sql)
        unsorted_expenses = self.c.fetchall()
        
        return unsorted_expenses
    
    def get_keywords(self):
        sql = """SELECT *, length(keyword_name) as key_len FROM keywords
        ORDER BY key_len DESC"""
        self.c.execute(sql)
        keywords = self.c.fetchall()
        
        return keywords
    
    def sort_expense(self, expense):
        sql = """UPDATE expenses SET keyword_id = ?
        WHERE expense_id = ?"""
        self.c.execute(sql, expense)
        self.conn.commit()

    def add_keyword(self, keyword):
        sql = """INSERT OR REPLACE INTO keywords (keyword_name, class_id, subclass_id)
        VALUES (?, ?, ?)"""
        self.c.execute(sql, keyword)
        self.conn.commit()

        return self.c.lastrowid