import sys
import dearpygui.dearpygui as dpg
import api
import gui
from yaspin import yaspin

skip_update = False

for arg in sys.argv[1:]:
    if arg in ('-s', '--skip-update'):
        skip_update = True

if not skip_update:
    with yaspin(text="Updating database...").white.bold.shark.on_blue:
        api.update_database()

gui.create_main_window()
for i in range(0, 6):
    dpg.render_dearpygui_frame()
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
dpg.destroy_context()
