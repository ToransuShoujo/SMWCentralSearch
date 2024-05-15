import gui
import dearpygui.dearpygui as dpg

gui.create_main_window()

while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

dpg.destroy_context()
