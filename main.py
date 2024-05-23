import dearpygui.dearpygui as dpg
import database
import scrape
import gui


gui.create_main_window()
gui.create_prep_window()
for i in range(0, 6):
    dpg.render_dearpygui_frame()
database.insert_smw_hacks(scrape.scrape_hacks())
dpg.delete_item('win_prep')
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
dpg.destroy_context()
