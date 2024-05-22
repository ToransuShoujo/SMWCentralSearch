import dearpygui.dearpygui as dpg

import database
import defines
from datetime import datetime
from datetime_management import datetime_to_dict

listbox_difficulty_data = []
current_date = datetime.now().astimezone()
current_time_zone = f"{current_date.isoformat()[-6:]} UTC"
modified_items = []
dpg.create_context()


def listbox_difficulty_callback(sender, app_data):
    label = dpg.get_item_label(sender)
    if label not in listbox_difficulty_data:
        listbox_difficulty_data.append(label)
        dpg.bind_item_theme(sender, button_selected_theme)
    else:
        listbox_difficulty_data.remove(label)
        dpg.bind_item_theme(sender, button_normal_theme)
    item_modified_callback(sender)
    return


def btn_search_callback():
    search_dict = {}
    for tag in modified_items:
        search_dict[tag] = dpg.get_value(tag)
    print(search_dict)
    database.search_hack(search_dict)
    return

def btn_reset_callback():
    for tag in modified_items:
        if tag.startswith('txt') or tag.startswith('combo'):
            dpg.set_value(tag, "")
        elif tag.startswith('bool'):
            if "exact_match" in tag:
                dpg.set_value(tag, True)
            else:
                dpg.set_value(tag, False)
        elif tag.startswith('radio'):
            dpg.set_value(tag, "Accepted")
        elif tag.startswith('date'):
            dpg.set_value(tag, datetime_to_dict(current_date))
        elif tag.startswith('listbox'):
            listbox_label = dpg.get_item_label(tag)
            if listbox_label in listbox_difficulty_data:
                listbox_difficulty_data.remove(listbox_label)
                dpg.bind_item_theme(tag, button_normal_theme)
        else:
            raise Exception(f"Unknown default for {tag}")
    return


def item_modified_callback(sender):
    if sender not in modified_items:
        modified_items.append(sender)
    elif sender.startswith('listbox') or sender.startswith('bool') or sender.startswith('radio'):
        modified_items.remove(sender)
    if sender == "combo-difficulty" and "combo-category" not in modified_items:
        modified_items.append("combo-category")
    return


def set_item_callbacks():
    items = dpg.get_all_items()
    items.pop(0)  # Remove the first item because it is referencing the primary window.
    for item_id in items:
        item_tag = dpg.get_item_alias(item_id)
        if item_tag == '':
            continue
        if item_tag[0:3] == 'btn':
            continue
        if dpg.get_item_configuration(item_id)["callback"] is None:
            dpg.set_item_callback(item=item_tag, callback=item_modified_callback)


# Custom listbox code provided by bandit-masked on GitHub
with dpg.theme() as custom_listbox_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, 0)
        dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0, 0.5)

with dpg.theme() as button_selected_theme:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 119, 200, 153))

with dpg.theme() as button_normal_theme:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (51, 51, 55, 255))


def create_main_window():
    dpg.create_viewport(title="SMW Central Search", width=925, height=475, resizable=False)
    dpg.setup_dearpygui()

    with dpg.window(tag="Primary Window"):
        with dpg.group(horizontal=True, horizontal_spacing=20):
            dpg.add_text("Hack title:  ")
            dpg.add_input_text(tag="txt-title", width=400)
            dpg.add_checkbox(label="Exact match", tag="bool-title-exact_match", default_value=True)
            dpg.add_checkbox(label="Regex", tag="bool-title-regex")

        with dpg.group(horizontal=True, horizontal_spacing=20):
            dpg.add_text("Hack authors:")
            dpg.add_input_text(tag="txt-authors", width=400, hint="Comma separated list of authors")
            dpg.add_checkbox(label="Exact match", tag="bool-authors-exact_match", default_value=True)
            dpg.add_checkbox(label="Regex", tag="bool-authors-regex")
            dpg.add_checkbox(label="Search individually", tag="bool-authors-individually")

        with dpg.group(horizontal=True, horizontal_spacing=20):
            dpg.add_text("Difficulty:  ")
            with dpg.child_window(height=120, width=400, border=False) as custom_listbox:
                for difficulty in defines.hack_difficulties:
                    tag_difficulty = "listbox-" + difficulty.replace(" ", "_").replace(":", "").lower()
                    dpg.add_button(label=difficulty, tag=tag_difficulty, width=-1, callback=listbox_difficulty_callback)
                dpg.bind_item_theme(custom_listbox, custom_listbox_theme)
            dpg.add_checkbox(label="Search individually", tag="bool-difficulties-individually")

        with dpg.group(horizontal=True, horizontal_spacing=20):
            dpg.add_text("Extras:      ")
            dpg.add_checkbox(label="Demo?", tag="bool-demo")
            dpg.add_checkbox(label="Hall of fame?", tag="bool-hall_of_fame")

        with dpg.group(horizontal=True, horizontal_spacing=20):
            dpg.add_text("Date before: ")
            dpg.add_date_picker(tag="date-before", default_value=datetime_to_dict(current_date))
            dpg.add_text("Date after: ")
            dpg.add_date_picker(tag="date-after", default_value=datetime_to_dict(current_date))

        with dpg.group(horizontal=True, horizontal_spacing=20):
            dpg.add_text("Time before: ")
            dpg.add_input_text(tag="txt-time-before", width=200, hint="14:51:00", no_spaces=True)
            dpg.add_text(current_time_zone)
            dpg.add_radio_button(items=("Submitted", "Accepted"), horizontal=True, tag="radio-time-before",
                                     default_value="Accepted")

        with dpg.group(horizontal=True, horizontal_spacing=20):
            dpg.add_text("Time after:  ")
            dpg.add_input_text(tag="txt-time-after", width=200, hint="12:24:00", no_spaces=True)
            dpg.add_text(current_time_zone)
            dpg.add_radio_button(items=("Submitted", "Accepted"), horizontal=True, tag="radio-time-after",
                                 default_value="Accepted")

        with dpg.group(horizontal=True, horizontal_spacing=20):
            dpg.add_button(label="Search", callback=btn_search_callback)
            dpg.add_button(label="Reset", callback=btn_reset_callback)

    set_item_callbacks()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)


def create_prep_window():
    with dpg.window(tag="win_prep", width=800, height=300):
        with dpg.table(header_row=False):
            for i in range(0, 5):
                dpg.add_table_column()
            for i in range(0, 7):
                with dpg.table_row():
                    for j in range(0, 5):
                        if i == 3 and j == 2:
                            dpg.add_text("Preparing, please wait...")
                        else:
                            dpg.add_text("            ")


def create_results_window():
    return