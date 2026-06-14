from datetime import date
import shutil
import sys
import os

base_dir = None

def get_in_file():
    global base_dir
    try:
        os.mkdir("safe_environment")
    except FileExistsError:
        pass
    os.chdir("safe_environment")
    base_dir = os.getcwd()

get_in_file()

cur_dir = os.getcwd()
return_item = None
print_return = False


manual = {
    "": f"Hello and welcome to Flumph terminal, running on python! here are some  specific manuals: \ncommands\nkeyboard shortcuts\nabout this terminal",
    "commands": f"here are some commands: \nexit\ncls\nmkdir\ncd\ncwd\ndel_dir\nfullpath\nman\n type man before the commands to get information on the command",
    "keyboard shortcuts": f"the keyboard shortcuts are: \nup arrow: previous command\ndown arrow: next command\nctrl+l: clear the screen\nctrl+d: exit the terminal",
    "about this terminal": "placeholder",
        "exit": "exit the terminal.",
        "cls": "clears the screen.",
        "mkdir": "makes a new directory with that name.",
        "cd": "changes the directory to the directory with that name.\nif no qualifiers are given, revert to the parent directory",
        "cwd": "gives you the current working directory",
        "del_dir": "delete the current directory and all attached file and directories, then moves you to the \n parent directory.",
        "fullpath": "gives you the full path of the current working directory",
        "man": "gives the manual of a command.",
        "whoami": "prints the name of the current user",
        "date": "prints the current date",
        "ls": "lists files in the current directory"

}

def exit_terminal(terminal, qualifiers):
    sys.exit()

def cls(terminal, qualifiers):
    global print_return
    terminal.configure(state="normal")
    terminal.delete(0.0, "end")
    terminal.configure(state="disabled")
    print_return = False

def mkdir(terminal, qualifiers):
    global cur_dir, print_return
    os.mkdir(qualifiers)
    os.chdir(qualifiers)
    cur_dir = os.getcwd()

def cd(terminal, qualifiers):
    global cur_dir, print_return
    if qualifiers == "":
        if base_dir != cur_dir:
            os.chdir("..")
    else:
        os.chdir(qualifiers)
    cur_dir = os.getcwd()
    print_return = False

def cwd(terminal, qualifiers):
    global return_item, print_return
    return_item = os.getcwd()
    return_item = return_item[len(base_dir) + 1:]
    print_return = True

def del_cur_dir(terminal, qualifiers):
    global cur_dir, print_return
    print_return = False
    if base_dir != cur_dir:
        directory = os.getcwd()
        os.chdir("..")
        shutil.rmtree(directory)
        cur_dir = os.getcwd()

def full_path(terminal, qualifiers):
    global return_item, print_return
    return_item = os.getcwd()
    print_return = True

def man(terminal, qualifiers):
    global print_return, return_item
    if qualifiers in manual:
        print_return = True
        return_item = manual[qualifiers]
    else:
        print_return = True
        return_item = f"unknown manual {qualifiers}"

def whoami(terminal, qualifiers):
    global print_return, return_item
    print_return = True
    return_item = os.getlogin()

def what_is_the_date(terminal, qualifiers):
    global print_return, return_item
    print_return = True
    return_item = date.today()

def ls(terminal, qualifiers):
    global print_return, return_item
    print_return = True
    return_item = os.listdir()