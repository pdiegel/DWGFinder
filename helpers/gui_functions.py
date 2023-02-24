import dearpygui.dearpygui as dpg
from helpers import misc


def create_gui():
    dpg.create_context()
    dpg.create_viewport(title='Existing File Search', width=600, height=500)

    with dpg.font_registry():
        default_font = dpg.add_font("sans.ttf", 22)

    with dpg.window(label="main", no_title_bar=True,
                    no_resize=True, no_move=True, width=600, height=600):
        dpg.add_text('Enter The File Number')
        dpg.add_input_text(tag='file_number',
                           default_value='', width=90)
        dpg.add_text('', tag='status')
        with dpg.group(tag='listbox'):
            create_file_listbox()

        with dpg.group(horizontal=True):
            dpg.add_button(
                label="Search", callback=display_file_list, height=60,
                width=123)
            dpg.add_button(label="Open", callback=misc.open_file,
                           height=60, width=123)
            dpg.add_button(label="Clear", callback=clear, height=60, width=123)

        dpg.bind_font(default_font)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


def clear():
    dpg.set_value('file_number', '')
    dpg.set_value('status', '')
    clear_file_listbox()


def display_file_list():
    try:
        dwg_file = misc.initialize_dwgfile()
    except ValueError:
        display_error(misc.get_file_number())
        return

    dpg.delete_item('file_list')
    print(dwg_file.file_dict)
    file_list = [
        f'{key} | {dwg_file.file_dict[key][0]}' for key in dwg_file.file_dict]
    create_file_listbox(items=file_list)


def clear_file_listbox():
    dpg.delete_item('file_list')
    create_file_listbox()


def create_file_listbox(items: list = []):
    dpg.add_listbox(tag='file_list', items=items, num_items=10,
                    width=570, parent='listbox')


def display_error(file_number):
    dpg.set_value('status', f'Error - File Number {file_number} not found.')
