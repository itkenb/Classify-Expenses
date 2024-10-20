import os

class Clear:
    '''Clears screen'''
    def __init__(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
