import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    df = pd.read_csv("nuclear_explosions.csv")
    df['Average Yield'] = (df['Data.Yeild.Lower'] + df['Data.Yeild.Upper']) / 2
    df['WEAPON SOURCE COUNTRY'] = df['WEAPON SOURCE COUNTRY'].str.strip()
    return df

def show_table_page():
    st.title("Nuclear Explosions Data Explorer")
    st.write("Explore nuclear test data from 1945-1998")

    df = load_data()

    st.sidebar.header("Table Settings")

    all_countries = sorted(df['WEAPON SOURCE COUNTRY'].unique().tolist())
    selected_countries = st.sidebar.multiselect(
        "Select Countries",
        all_countries,
        default=["USA", "USSR"]
    )

    sort_options = {
        "Highest Yield": "Average Yield",
        "Lowest Yield": "Average Yield",
        "Deepest": "Location.Cordinates.Depth",
        "Shallowest": "Location.Cordinates.Depth",
        "Newest": "Date.Year",
        "Oldest": "Date.Year"
    }
    selected_sort = st.sidebar.selectbox("Sort By", list(sort_options.keys()))

    num_results = st.sidebar.slider("Number of Results", 10, 100, 20)

    if len(selected_countries) > 0:
        filtered_df = df[df['WEAPON SOURCE COUNTRY'].isin(selected_countries)]
    else:
        st.warning("Please select at least one country")
        st.stop()

    sort_column = sort_options[selected_sort]
    ascending = True if "Lowest" in selected_sort or "Shallowest" in selected_sort or "Oldest" in selected_sort else False
    sorted_df = filtered_df.sort_values(by=sort_column, ascending=ascending).head(num_results)

    st.subheader(f"Top {num_results} Nuclear Tests")
    st.dataframe(sorted_df[['WEAPON SOURCE COUNTRY', 'Data.Name', 'Date.Year',
                          'Average Yield', 'Location.Cordinates.Depth',
                          'Data.Magnitude.Body']])

    st.subheader("Tests by Country")
    if len(selected_countries) > 1:
        country_counts = sorted_df['WEAPON SOURCE COUNTRY'].value_counts()
        fig, ax = plt.subplots()
        ax.pie(country_counts,
               labels=country_counts.index,
               autopct='%1.1f%%',
               colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
        ax.set_title('Nuclear Tests by Selected Countries')
        st.pyplot(fig)
    else:
        st.write(f"Showing data for {selected_countries[0]} only - select multiple countries to see pie chart")

if __name__ == "__main__":
    show_table_page()