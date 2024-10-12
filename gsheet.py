import gspread

class Gsheet:
    def __init__(self, cred_dir, gsheet_url):
        self.cred_dir = cred_dir
        self.gsheet_url = gsheet_url
        self.gc = gspread.service_account(filename=self.cred_dir)
        self.sh = self.gc.open_by_url(self.gsheet_url)
        self.ws = self.sh.worksheet("raw")

    def get_row_count(self):
        records = self.ws.get_all_values()
        return len(records)

    def get_row_values(self, counter):
        return self.ws.row_values(counter)

    def update_row(self, y, x, val):
        self.ws.update_cell(y, x, val)
