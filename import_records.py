import csv
from model import Model
from clear import Clear

class ImportRecords:
    '''
    Takes csv directory and bank account ID
    Imports csv records to Expense.expenses table
    CSV Format
    Date - Description - Amount
    '''
    def __init__(self, csv_dir, account_id):
        self.csv_dir = csv_dir
        self.account_id = account_id
        self.md = Model()
        self._controller()

    def _controller(self):
        '''
        Checks if bank account exists,
        if not, adds new bank account ID and
        takes newly added
        Expenses.bnk_accts.bnk_acct_id.
        Reads csv file and appends
        Expenses.bnk_accts.bnk_acct_id for
        every line in the csv file
        '''
        print("Importing CSV to database... Please wait...")
        expenses = []
        bnk_acct_id = self.md.add_bnk_acct(self.account_id)

        with open(self.csv_dir, 'r', encoding="utf-8") as cf:
            csv_raw = csv.reader(cf)
            for c in csv_raw:
                c.append(bnk_acct_id)
                expenses.append(c)  
        self._import_expenses(expenses)
        Clear()
        print("CSV Imported...")

    def _import_expenses(self, expenses):
        '''
        Calls add_expense from Model class and pass
        date, description, amount, and bnk_acct_id
        '''
        for expense in expenses:
            self.md.add_expense(expense)
