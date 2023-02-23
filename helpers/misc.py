from helpers import file
import dearpygui.dearpygui as dpg
import subprocess


def initialize_dwgfile():
    file_number = dpg.get_value('file_number')
    dwg_file = file.DWGFiles(file_number)
    return dwg_file


def open_dwg_with_powershell(file_path, file_name):
    # Start a new PowerShell process
    powershell = subprocess.Popen(
        ["powershell.exe", "-Command", "-"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True)

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
    dwg_file = initialize_dwgfile()
    selected_file = dpg.get_value('file_list')
    file_name = selected_file.split(' | ')[0]
    file_path = dwg_file.get_specific_file_path(file_name)

    open_dwg_with_powershell(file_path, file_name)
