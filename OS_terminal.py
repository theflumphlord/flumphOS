import customtkinter as ctk
import os
import sys
import shutil
import socket
import platform
import terminal_commands

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


def print_to_terminal(text):
    if isinstance(text, list):
        terminal_output.configure(state="normal")
        for line in text:
            terminal_output.insert("end", f"\n{line}")
            terminal_output.see("end")
        terminal_output.configure(state="disabled")
    else:
        terminal_output.configure(state="normal")
        terminal_output.insert("end", f"\n{text}")
        terminal_output.see("end")
        terminal_output.configure(state="disabled")


def enforce_prefix(var_name, mode, index):
    text = prefix_var.get()
    if not text.startswith(PREFIX):
        prefix_var.set(PREFIX)
    elif len(text) < len(PREFIX):
        prefix_var.set(PREFIX)


terminal = ctk.CTk()
terminal.title("Terminal")
terminal.geometry("800x450")

PREFIX = "user@flumph_terminal:~$"

prefix_var = ctk.StringVar(value=PREFIX)
prefix_var.trace_add("write", enforce_prefix)

commands_existing = {
    "exit": terminal_commands.exit_terminal,
    "cls": terminal_commands.cls,
    "mkdir": terminal_commands.mkdir,
    "cd": terminal_commands.cd,
    "cwd": terminal_commands.cwd,
    "del_dir": terminal_commands.del_cur_dir,
    "fullpath": terminal_commands.full_path,
    "man": terminal_commands.man,
    "whoami": terminal_commands.whoami,
    "date": terminal_commands.what_is_the_date,
    "ls" : terminal_commands.ls,
}

def autocomplete_command():
    global command_index, used_commands
    all_commands = []
    for i in commands_existing:
        if i[:len(terminal_command.get())] == terminal_command.get():
            all_commands.append(i)
    for i in all_commands:
        print_to_terminal(i)
        command_index += 1
        used_commands.append(i)

def execute_command(event):
    global command_index, prefix_var
    full_command = terminal_command.get().strip()
    command = full_command.split(maxsplit=1)[0]
    qualifiers = full_command[len(command):].strip()
    full_input = f"{prefix_var.get()}{full_command}"
    print_to_terminal(full_input)
    terminal_command.delete(0, "end")
    if command in commands_existing:
        commands_existing[command](terminal_output, qualifiers)
        used_commands.append(full_command)
        if terminal_commands.print_return:
            print_to_terminal(terminal_commands.return_item)
    elif command == "boot":
        terminal_commands.cls(terminal_output, qualifiers)
        boot_terminal()
        used_commands.append(full_command)
    elif command != "":
        print_to_terminal(f"Unknown command: '{command}'")
    prefix_var.set(f"{terminal_commands.cur_dir}{PREFIX}")
    command_index = len(used_commands)


# basic variables
host_name = None
current_os = None
user = None
used_commands = []
command_index = 0
base_dir = None

terminal_output = ctk.CTkTextbox(
    terminal,
    fg_color="#000000",
    text_color="#00FF00",
    font=("Cascadia Code", 14),
    wrap="word",
    activate_scrollbars=True
)

terminal_output.pack(expand=True, fill="both", padx=10, pady=5)

input_frame = ctk.CTkFrame(terminal, fg_color="transparent")
input_frame.pack(side="bottom", fill="x", padx=10, pady=5)

prompt_label = ctk.CTkLabel(
    input_frame,
    text=prefix_var.get(),
    font=("Cascadia Code", 14),
    text_color="#00FF00",
)
prompt_label.pack(side="left")

terminal_command = ctk.CTkEntry(
    input_frame,
    fg_color="#000000",
    text_color="#00FF00",
    font=("Cascadia Code", 14),
    height=20,
    border_width=0
)
terminal_command.pack(side="left", expand=True, fill="x", padx=(5, 0))

def fill_command():
    if command_index >= len(used_commands):
        terminal_command.delete(0, "end")
        terminal_command.insert(0, "")
    else:
        terminal_command.delete(0, "end")
        terminal_command.insert(0, used_commands[command_index])


def prev_command(event):
    global command_index
    command_index -= 1
    command_index = max(0, command_index)
    fill_command()

def next_command(event):
    global command_index
    command_index += 1
    command_index = min(len(used_commands) +2, command_index)
    fill_command()


terminal_command.bind("<Return>", execute_command)
terminal_command.bind("<Up>", prev_command)
terminal_command.bind("<Down>", next_command)
terminal_command.bind("<Control-l>", lambda event: terminal_commands.cls(terminal_output, ""))
terminal_command.bind("<Control-d>", lambda event: terminal_commands.exit_terminal(terminal_output, ""))
terminal_command.bind("<Tab>", lambda event : autocomplete_command())

def boot_terminal():
    global host_name, current_os, user, PREFIX, prefix_var, base_dir
    print_to_terminal("Checking user...")
    try:
        user = os.getlogin()
    except:
        user = "user"
    print_to_terminal(f"User loaded: {user}")
    print_to_terminal(f"checking base directory...")
    base_dir = os.getcwd()
    print_to_terminal(f"base directory found")
    PREFIX = f"{user}@flumph_terminal:~$"
    prefix_var.set(f"{terminal_commands.cur_dir}{PREFIX}")
    prompt_label.configure(text=PREFIX)
    print_to_terminal("Checking host...")
    host_name = socket.gethostname()
    print_to_terminal(f"Host found: {host_name}")
    print_to_terminal("Checking OS...")
    current_os = platform.system()
    print_to_terminal(f"OS detected: {current_os}\n")
    print_to_terminal("System Ready. Type 'cls' to clear or 'exit' to quit.")


terminal.after(20, boot_terminal)
terminal.mainloop()
