import sys
from clear import Clear
# from model import Model
from sort_records import SortRecords
from export_records import ExportRecords
from import_records import ImportRecords

class Expense:
    def __init__(self):
        self.controller()

    def help(self):
        print("HELP!")

    def controller(self):
        modes = {
            "sort" : self.sort_records,
            "export" : self.export_records,
            "import" : self.import_records
        }

        if len(sys.argv) != 1:
            if sys.argv[1] in modes:
                modes.get(sys.argv[1])()
            else:
                self.help()
        else:
            self.help()

    def check_argv(self):
        modes = {
            "sort" : self.sort_records,
            "export" : self.export_records,
            "import" : self.import_records
        }

        if len(sys.argv) == 1:
            self.help()
        if sys.argv[1] not in modes:
            self.help()
        return modes.get(sys.argv[1])()

    def import_records(self):
        csv_dir = input("CSV directory:\n>> ")
        account_id = input("Account ID:\n>> ")
        ImportRecords(csv_dir, account_id)

    def sort_records(self):
        SortRecords()

    def export_records(self):
        print("EXPORT RECORDS")

    # def show_numbers(self):
    #     nums = Model().show_nums()

if __name__ == "__main__":
    Expense()
