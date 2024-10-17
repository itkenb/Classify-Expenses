from model import Model
from clear import Clear
import sys

class SortRecords:
    def __init__(self):
        self.md = Model()
        self.controller()

    def controller(self):
        unsorted_expenses = self.md.get_unsorted_epxenses()
        # keywords = self.md.get_keywords()

        if len(unsorted_expenses) == 0:
            print("YOU DON'T HAVE EXPENSES THAT NEEDS TO BE SORTED")
        else:
            for unsorted_expense in unsorted_expenses:
                expense_sorted = False
                keywords = self.md.get_keywords()
                for keyword in keywords:
                    if keyword[1] in unsorted_expense[2].lower():
                        expense_sorted = self.sort_expense((keyword[0], unsorted_expense[0]))
                        break
                if not expense_sorted:
                    expense_sorted = self.sort_expense((False, unsorted_expense))

    def sort_expense(self, unsorted_expense):
        if not unsorted_expense[0]:
            Clear()
            print(f"NO KEYWORD FOR {unsorted_expense[1][2]}")
            key = input(f"Add Keyword (--save to STOP and SAVE):\n>> ")
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
