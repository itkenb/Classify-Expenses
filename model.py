import sqlite3

class Model:
    """- Initiates with creating database and inserting required data.
    - Handles storing keywords into the database"""
    def __init__(self):
        self.conn = sqlite3.connect('Expenses.db')
        self.c = self.conn.cursor()
        self.category = [
            "502 TAXES",
            "503 FIDUCIARY FEES & SERVICES",
            "504 CONTRIBUTIONS 505 ACCOUNTING & TAX PREPARATION",
            "506 LEGAL SERVICES 31 CHART OF ACCOUNTS EXPENSES - OTHER"
        ]

        # Create class table
        self.c.execute("""CREATE TABLE IF NOT EXISTS class (
                       class_id INTEGER PRIMARY KEY,
                       class_name TEXT)""")
        #Insert classes
        self.c.execute("""INSERT OR REPLACE INTO class (class_id, class_name)
                       VALUES (1, 'PERSONAL'), (2, 'TRUST')""")

        #Create subclass table
        self.c.execute("""CREATE TABLE IF NOT EXISTS subclass (
                       subclass_id INTEGER PRIMARY KEY,
                       subclass_name TEXT)""")

        #Insert Subclasses
        with open("subclasses.txt", "r", encoding="utf-8") as f:
            for idx, subclass in enumerate(f):
                sql = """INSERT OR REPLACE INTO subclass (
                subclass_id, subclass_name)
                VALUES(?, ?)"""
                self.c.execute(sql, (idx + 1, subclass.strip()))

        #Create keyword table
        self.c.execute("""CREATE TABLE IF NOT EXISTS keywords (
                       keyword_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       keyword_name TEXT,
                       category INTEGER,
                       class_id INTEGER,
                       subclass_id INTEGER,
                       FOREIGN KEY(class_id) REFERENCES class(class_id),
                       FOREIGN KEY(subclass_id) REFERENCES subclass(subclass_id))""")

        #Create expenses table
        self.c.execute("""CREATE TABLE IF NOT EXISTS expenses (
                       expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       date TEXT,
                       description TEXT,
                       amount REAL,
                       account TEXT,
                       transaction_type INTEGER,
                       class_id INTEGER,
                       subclass_id INTEGER,
                       FOREIGN KEY(class_id) REFERENCES class(class_id),
                       FOREIGN KEY(subclass_id) REFERENCES subclass(subclass_id))""")

        self.conn.commit()
