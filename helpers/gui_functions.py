import dearpygui.dearpygui as dpg
from helpers import misc


def create_gui():
    dpg.create_context()
    dpg.create_viewport(title='Existing File Search', width=600, height=600)

    with dpg.font_registry():
        default_font = dpg.add_font("sans.ttf", 22)

    with dpg.window(label="main", no_title_bar=True,
                    no_resize=True, no_move=True, autosize=True):
        dpg.add_text('Enter The File Number')
        dpg.add_input_text(tag='file_number', default_value='FN', width=90)
        with dpg.group(tag='listbox', parent='main'):
            create_listbox()

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
    dpg.set_value('file_list', '')


def display_file_list():
    dwg_file = misc.initialize_dwgfile()
    dpg.delete_item('file_list')
    create_listbox(items=dwg_file.formatted_file_list)


def create_listbox(items=[]):
    dpg.add_listbox(tag='file_list', items=items, num_items=10,
                    width=500, parent='listbox')
