"""This module creates the main GUI for the DWG File Finder, and handles
 all the functions that relate to the GUI."""
import dearpygui.dearpygui as dpg
from helpers import misc


def create_gui() -> None:
    """Creates the main GUI of the program."""
    dpg.create_context()
    dpg.create_viewport(title="Existing File Search", width=600, height=500)

    with dpg.handler_registry():
        dpg.add_key_press_handler(
            key=dpg.mvKey_Return, callback=display_file_list
        )

    with dpg.font_registry():
        default_font = dpg.add_font("sans.ttf", 22)

    with dpg.window(
        label="main",
        no_title_bar=True,
        no_resize=True,
        no_move=True,
        width=600,
        height=600,
    ):
        dpg.add_text("Enter The File Number")
        dpg.add_input_text(tag="file_number", default_value="", width=90)
        dpg.add_text("", tag="status")
        with dpg.group(tag="listbox"):
            create_file_listbox()

        dpg.add_spacer(height=10)

        with dpg.group(horizontal=True):
            dpg.add_button(
                label="Search",
                callback=display_file_list,
                height=60,
                width=250,
            )
            dpg.add_button(
                label="Open", callback=misc.open_file, height=60, width=150
            )
            dpg.add_button(label="Clear", callback=clear, height=60, width=150)

    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(
                dpg.mvStyleVar_FrameRounding, 3, category=dpg.mvThemeCat_Core
            )

    dpg.bind_theme(global_theme)
    dpg.bind_font(default_font)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


def clear() -> None:
    """Clears all values in the GUI."""
    dpg.set_value("file_number", "")
    dpg.set_value("status", "")
    clear_file_listbox()


def display_file_list() -> None:
    """Displays the file list to the GUI, with the given file number."""
    try:
        dwg_file = misc.initialize_dwgfile()
    except ValueError:
        display_error(misc.get_file_number())
        return

    dpg.delete_item("file_list")
    print(dwg_file.file_dict)
    file_list = [
        f"{key} | {value[0]}" for key, value in dwg_file.file_dict.items()
    ]
    create_file_listbox(items=file_list)


def clear_file_listbox() -> None:
    """Clears the file_list listbox in the GUI."""
    dpg.delete_item("file_list")
    create_file_listbox()


def create_file_listbox(items: list = None) -> None:
    """Creates the file_list listbox."""
    if not items:
        items = []
    dpg.add_listbox(
        tag="file_list", items=items, num_items=10, width=570, parent="listbox"
    )


def display_error(file_number: str) -> None:
    """Displays an error message on the GUI."""
    dpg.set_value("status", f"Error - File Number {file_number} not found.")
