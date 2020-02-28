import colorama

def write(string: str, status: bool):
    if status:
        success(string)
    else:
        error(string)

def error(string: str):
    set_color(True)
    print(f"Error: ", end="")
    restore_color()
    print(string)

def success(string: str):
    set_color(False)
    print(f"Success: ", end="")
    restore_color()
    print(string)

def set_color(status: bool = False):
    """
    Sets color to GREEN if status == False, else RED
    """
    print(colorama.Fore.LIGHTGREEN_EX if status else colorama.Fore.RED, end="")

def restore_color():
    print(colorama.Fore.WHITE, end="")