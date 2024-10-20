from model import Model
from clear import Clear
import sys

class SortRecords:
    '''
    Handles all sorting of records to
    corresponding keyword, class, and subclass
    '''
    def __init__(self):
        self.md = Model()
        self._controller()

    def _controller(self):
        '''
        Checks if there are unsorted expenses from Expenses.expenses
        '''
        unsorted_expenses = self.md.get_unsorted_epxenses()

        if len(unsorted_expenses) == 0:
            print("YOU DON'T HAVE EXPENSES THAT NEEDS TO BE SORTED")
        else:
            for unsorted_expense in unsorted_expenses:
                expense_sorted = False
                keywords = self.md.get_keywords()
                for keyword in keywords:
                    if keyword[1] in unsorted_expense[2].lower():
                        expense_sorted = self._sort_expense((keyword[0], unsorted_expense[0]))
                        break
                if not expense_sorted:
                    expense_sorted = self._sort_expense((False, unsorted_expense))

    def _sort_expense(self, unsorted_expense):
        '''
        Takes unsorted_expenses and checks if keyword_name
        is in expense_name.
        If not, takes new keyword_name, class_id, and
        subclass_id then added to Expenses.keywords then sorts the record.
        Else, sorts record with the corresponding keyword.
        Returns true if successfully sorted
        '''
        if not unsorted_expense[0]:
            Clear()
            print(f"NO KEYWORD FOR {unsorted_expense[1][2]}")
            key = input("Add Keyword (--save to STOP and SAVE):\n>> ")
            if key == "--save":
                Clear()
                print("Changes saved...")
                sys.exit()
            class_id = int(input("Class ID:\n>>"))
            subclass_id = int(input("Subclass ID:\n>>"))
            keyword_id = self.md.add_keyword((key, class_id, subclass_id))
            self.md.sort_expense((keyword_id, unsorted_expense[1][0]))
        else:
            self.md.sort_expense(unsorted_expense)

        return True
