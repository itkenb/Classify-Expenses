import sys
from clear import Clear
# from model import Model
from sort_records import SortRecords
from export_records import ExportRecords
from import_records import ImportRecords

class Expense:
    '''
    Expense.py main controller
    '''
    def __init__(self):
        self._controller()

    def _help(self):
        '''
        Returns acceptable commands e.g expense.py command
        '''
        print("HELP!")

    def _controller(self):
        '''
        Takes second argv
        Runs specific method based on given command
        '''
        modes = {
            "sort" : self._sort_records,
            "export" : self._export_records,
            "import" : self._import_records
        }

        if len(sys.argv) != 1:
            if sys.argv[1] in modes:
                modes.get(sys.argv[1])()
            else:
                self._help()
        else:
            self._help()

    def _import_records(self):
        '''
        Takes csv directory and bank account ID
        Calls import_records.ImportRecords class
        '''
        csv_dir = input("CSV directory:\n>> ")
        account_id = input("Account ID:\n>> ")
        ImportRecords(csv_dir, account_id)

    def _sort_records(self):
        '''
        Calls sort_records.SortRecords class
        '''
        SortRecords()

    def _export_records(self):
        '''
        TO DO'''
        print("EXPORT RECORDS")

if __name__ == "__main__":
    Expense()
