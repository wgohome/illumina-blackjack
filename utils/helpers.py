import os

def clear_screen():
    # For Windows
    if os.name == "nt":
        os.system("cls")
    # For mac and windows
    elif os.name == "posix":
        os.system("clear")
