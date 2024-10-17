import csv
from model import Model
from clear import Clear

class ImportRecords:
    def __init__(self, csv_dir, account_id):
        self.csv_dir = csv_dir
        self.account_id = account_id
        self.md = Model()
        self.controller()

    def controller(self):
        print("Importing CSV to database... Please wait...")
        expenses = []
        bnk_acct_id = self.md.add_bnk_acct(self.account_id)

        with open(self.csv_dir, 'r', encoding="utf-8") as cf:
            csv_raw = csv.reader(cf)
            for c in csv_raw:
                c.append(bnk_acct_id)
                expenses.append(c)  
        self.import_expenses(expenses)
        Clear()
        print("CSV Imported...")

    def import_expenses(self, expenses):
        for expense in expenses:
            self.md.add_expense(expense)
