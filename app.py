import streamlit as st

home_page = st.Page("Home.py", title="Home", icon=":material/home:")
folders_page = st.Page("Folders.py", title="Folders", icon=":material/drag_indicator:")
settings_page = st.Page("Settings.py", title="Settings", icon=":material/settings:")
#pg = st.navigation({"Menu": [home_page, folders_page, settings_page ]})
pg = st.navigation({"Menu": [home_page, settings_page ]})
st.set_page_config(page_title="DocSort", page_icon="🗃️")
pg.run()










