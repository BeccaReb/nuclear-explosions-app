import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_bar_page():
    @st.cache_data
    def load_data():
        return pd.read_csv('nuclear_explosions.csv')

    df = load_data()

    df['Year'] = df['Date.Year']


    st.title('Nuclear Explosions Data by Year')
    st.write('This page shows the number of nuclear explosions per country for a selected year between 1945 and 1998.')

    year = st.slider('Select a year:', 1945, 1998, 1962)

    year_data = df[df['Year'] == year]

    explosions_by_country = year_data['WEAPON SOURCE COUNTRY'].value_counts()

    fig, ax = plt.subplots(figsize=(10, 6))
    explosions_by_country.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title(f'Nuclear Explosions Data in {year}')
    ax.set_xlabel('Countries')
    ax.set_ylabel('Number of Explosions')
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    st.pyplot(fig)

    if st.checkbox('Display raw data for selected year'):
        st.write(year_data[['WEAPON SOURCE COUNTRY', 'Data.Name', 'Date.Day', 'Date.Month']])


    def show_table_page():
        st.title("Data Table View")

if __name__ == "__main__":
   show_table_page()