from helpers import file, gui_functions
import dearpygui.dearpygui as dpg
import subprocess


def initialize_dwgfile():
    file_number = get_file_number()
    try:
        dwg_file = file.DWGFiles(file_number)
    except ValueError:
        raise ValueError
    return dwg_file


def get_file_number():
    return dpg.get_value('file_number').strip()


def open_dwg_with_powershell(file_path, file_name):
    # Start a new PowerShell process
    powershell = subprocess.Popen(
        ["powershell.exe", "-Command", "-"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True, shell=True)

    # Run multiple PowerShell commands
    powershell.stdin.write(f"cd {file_path}\n")
    powershell.stdin.write(f'.\\"{file_name}"\n')
    powershell.stdin.write("Exit\n")

    # Get the output of the PowerShell commands
    output, errors = powershell.communicate()

    # Print the output and errors
    print(output)
    print(errors)


def open_file():
    selected_file = dpg.get_value('file_list').strip()
    if not selected_file:
        gui_functions.display_error(get_file_number())
        return
    dwg_file = initialize_dwgfile()
    file_name = selected_file.split(' | ')[0]
    file_path = dwg_file.get_file_path(file_name)

    open_dwg_with_powershell(file_path, file_name)
