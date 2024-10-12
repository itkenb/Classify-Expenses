import os
from model import Model
from gsheet import Gsheet

class Expense:
    def __init__(self):
        if not os.path.isfile("settings.file"):
            self.cred_dir, self.gsheet_url = self.create_settings_file()
        else:
            with open("settings.file", "r", encoding="utf-8") as f:
                self.details = f.readlines()

        self.gs = Gsheet(self.details[0].strip(), self.details[1].strip())
        self.md = Model()
        self.controller()

    def create_settings_file(self):
        """Creates a file that stores the path to google sheet credential JSON
        and Google Sheet URL"""
        cred_dir = input("Credential directory\n>> ")
        gsheet_url = input("Google Sheet URL:\n>> ")

        with open("settings.file", "a", encoding="utf-8") as f:
            f.write(cred_dir + "\n")
            f.write(gsheet_url + "\n")

        return cred_dir, gsheet_url

    def controller(self):
        row_count = self.gs.get_row_count()
        counter = 2

        while counter < row_count + 1:
            row_values = self.gs.get_row_values(counter)
            col_count = len(row_values)
            if col_count == 5:
                if float(row_values[2]) > 0:
                    ismatch = self.match_keyword(row_values[1])
                    if ismatch is None:
                        kw = input(f"Keyword for {row_values[1]}: ")
                        cls = int(input("Class: "))
                        scls = int(input("Subclass: "))
                        self.md.add_keyword(kw, cls, scls)
                        class_name = self.md.get_class_name(cls)
                        subclass_name = self.md.get_subclass_name(scls)
                        self.gs.update_row(counter, col_count + 1, class_name[0])
                        self.gs.update_row(counter, col_count + 2, subclass_name[0])
                    else:
                        self.gs.update_row(counter, col_count + 1, ismatch[0])
                        self.gs.update_row(counter, col_count + 2, ismatch[1])

            counter += 1

    def match_keyword(self, description):
        keywords = self.md.get_all_keywords()

        for keyword in keywords:
            if keyword[0] in description.lower():
                return keyword[1], keyword[2]

if __name__ == "__main__":
    Expense()
