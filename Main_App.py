"""
Names: Rebecca Magana, Frieda Nal, & Siri Dhayabaran
CS230: Section 8
Data: •	Nuclear Explosions 1945-1998 (2046 rows)
URL:
Description: This is an online, interactive plotting application that displays worldwide nuclear explosion data during the period 1945-1998. Users can access the historical database through various pages, each giving a different type of perspective. The first page establishes the dataset, the second provides a bar chart of nuclear activity by time, the third is a sortable table of top explosions, and the fourth is a map that identifies nuclear test sites around the world. Users can further customize their view using filters like country, year range, and yield and gain a deeper understanding of nuclear test patterns.
"""

import streamlit as st
from Table_Page import show_table_page
from Bar_Page import show_bar_page
from Map_Page import show_map_page

st.set_page_config(
    page_title="Nuclear Explosion Data (1945-1998)",
    layout="wide",
    page_icon="💥"
)

st.title("🌍 Worldwide Nuclear Explosion Data (1945-1998)")
st.markdown("""
- This interactive application visualizes nuclear explosion data from 1945-1998.
- Please use the side bar to adjust the Table and Map Settings. 
""")

tab1, tab2, tab3 = st.tabs(["📈 Activity Timeline", "🧮 Explosion Table", "🗺️ Test Site Map"])

with tab1:
    show_bar_page()

with tab2:
    show_table_page()

with tab3:
    show_map_page()