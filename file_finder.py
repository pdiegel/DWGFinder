'''This program finds and opens dwg files on a network server,
 given the file number.'''
import subprocess
import os
import dearpygui.dearpygui as dpg
import datetime
import time


def get_file_attributes():
    file_number = dpg.get_value('file_number')
    year = file_number[:2]
    month = file_number[2:4]
    if int(year) > 89:
        if int(month) < 10:
            month = file_number[3]
    short_file_number = f'{year}{month}{file_number[5:8]}'
    file_path = f'//server/dwg/{year}dwg/{month}/'
    return [file_path, file_number, short_file_number]


def get_file_list():
    file_attributes = get_file_attributes()
    file_path = file_attributes[0]
    file_list = find_dwg_file(
        file_path, file_attributes[1], file_attributes[2])
    new_file_list = []
    for i, file in enumerate(file_list):
        file_date = os.path.getctime(os.path.join(file_path, file))
        formatted_date = datetime.datetime.strptime(
            str(file_date), "%a %b %d %H:%M:%S %Y")
        new_file_list.append(f'{file} {formatted_date}')

    dpg.delete_item('file_list')
    dpg.add_listbox(items=new_file_list, tag='file_list', parent='listbox')


def get_newest_file(file_path, file_list):
    newest_creation_time = 0
    newest_file = ''
    for file in file_list:
        file_creation_time = os.path.getctime(os.path.join(file_path, file))
        if file_creation_time > newest_creation_time:
            newest_creation_time = file_creation_time
            newest_file = file

    return newest_file


def find_dwg_file(file_path, file_number, short_file_number):
    job_list = []
    for (_, _, files) in os.walk(file_path, topdown=True):
        for file in files:
            is_dwg_file = file.lower().endswith('.dwg')
            if not is_dwg_file:
                continue
            if file.startswith(file_number):
                job_list.append(file)
            elif file.startswith(short_file_number):
                job_list.append(file)

    if job_list:
        return job_list


def open_file():
    file_path = get_file_attributes()[0]
    file_name = dpg.get_value('file_list').split(' ')[0]
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


def clear():
    dpg.set_value('file_number', '')
    dpg.set_value('file_list', '')


def main():
    dpg.create_context()
    dpg.create_viewport(title='Existing File Search', width=500, height=500)

    with dpg.font_registry():
        # first argument ids the path to the .ttf or .otf file
        default_font = dpg.add_font("sans.ttf", 24)

    with dpg.window(label="main", no_title_bar=True,
                    no_resize=True, no_move=True, autosize=True):
        dpg.add_text('Enter The File Number')
        dpg.add_input_text(tag='file_number', default_value='FN', width=90)
        with dpg.group(tag='listbox'):
            dpg.add_listbox(tag='file_list', items=[])

        with dpg.group(horizontal=True):
            dpg.add_button(
                label="Search", callback=get_file_list, height=60, width=123)
            dpg.add_button(label="Open", callback=open_file,
                           height=60, width=123)
            dpg.add_button(label="Clear", callback=clear, height=60, width=123)

        dpg.bind_font(default_font)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


# file_name = find_dwg_file(file_path, file_number, short_file_number)

# if file_name:
#     open_file(file_path, file_name)

if __name__ == '__main__':
    main()
