'''This module handles all the miscellaneous functions in the program.'''
import subprocess
import os.path
import dearpygui.dearpygui as dpg
from helpers import file, gui_functions


def initialize_dwgfile() -> file.DWGFiles:
    '''Initializes and returns a DWGFiles Object.'''
    file_number = get_file_number()
    try:
        dwg_file = file.DWGFiles(file_number)
    except ValueError as exc:
        raise exc
    return dwg_file


def get_file_number() -> str:
    '''Retuns the file number from the GUI.'''
    return dpg.get_value('file_number').strip()


def open_dwg_with_powershell(file_path: os.path, file_name: str) -> None:
    '''Runs the windows powershell commands to change directory, and
     open the given DWG file.'''

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


def open_file() -> None:
    '''Opens a DWG file using windows powershell,
     given the file number.'''
    selected_file = dpg.get_value('file_list').strip()
    if not selected_file:
        gui_functions.display_error(get_file_number())
        return
    dwg_file = initialize_dwgfile()
    file_name = selected_file.split(' | ')[0]
    file_path = dwg_file.get_file_path(file_name)

    open_dwg_with_powershell(file_path, file_name)
