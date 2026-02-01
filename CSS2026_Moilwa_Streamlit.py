# -*- coding: utf-8 -*-
"""
Created on Sun Feb  1 22:57:43 2026

@author: Grego
"""

import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px

# --------------------------------------------------
# WATER-THEMED BACKGROUND
# 
st.markdown(
    """
    <style>
    /* Apply gradient to the main app container */
    .stApp {
        background: linear-gradient(to bottom, #e0f7fa, #b2ebf2);
    }

    /* Make Streamlit sections transparent */
    .main, .css-1d391kg, .css-ffhzg2 {
        background-color: transparent;
    }

    /* Header colors */
    h1, h2, h3, h4, h5, h6 {
        color: #004d40;
    }

    /* Text color */
    .stText, p, span {
        color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# APP TITLE & INTRO
# --------------------------------------------------
st.title("Securing the Future, One Authorisation at a Time")
st.write("A water bankruptcy is a future we cannot afford.")

name = "Mr. Gregory Moilwa"
field = "Environmental Sciences"
institution = "North-West University"

st.header("A Scientist and an Authorisation")
st.write(f"**Name:** {name}")
st.write(f"**Field of Research:** {field}")
st.write(f"**Institution:** {institution}")

# --------------------------------------------------
# STUDY AREA IMAGES
# --------------------------------------------------
st.title("The Vaal and its Tributary, Koekemoerspruit")

try:
    img1 = Image.open("Moilwa_Koekemoerspruit.jpg")
    img2 = Image.open("Moilwa_Vaal river_Vermaasdrift.jpg")
except FileNotFoundError:
    st.error("Images not found. Check file paths.")
    st.stop()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Koekemoerspruit tributary")
    st.image(img1, use_container_width=True)

with col2:
    st.subheader("Vermaasdrift sampling point")
    st.image(img2, use_container_width=True)

# --------------------------------------------------
# SECTION TITLE
# --------------------------------------------------
st.header("Water Quality Analysis")
st.write(
    "Select a variable and a year range to view water quality trends "
    "in the Vaal River and Koekemoerspruit tributary."
)

# --------------------------------------------------
# LOAD WATER QUALITY DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("KMS_Var.xlsx")

    # Ensure 'Year' column exists
    if "Year" not in df.columns:
        df = df.reset_index()
        df.rename(columns={df.columns[0]: "Year"}, inplace=True)

    df.columns = df.columns.astype(str).str.strip()
    df["Year"] = df["Year"].astype(int)

    # Remove rows where Year is 0
    df = df[df["Year"] != 0]

    return df

WQ_data = load_data()

# --------------------------------------------------
# VARIABLE SELECTION
# --------------------------------------------------
variable = st.selectbox(
    "Choose a water quality variable",
    ["Uranium", "Arsenic", "Manganese", "pH"]
)

# --------------------------------------------------
# WHO GUIDELINE VALUES
# --------------------------------------------------
WHO_GUIDELINES = {
    "Uranium": 0.03,      # mg/L
    "Arsenic": 0.01,      # mg/L
    "Manganese": 0.4,     # mg/L
    "pH": 8.5             # upper limit
}

# --------------------------------------------------
# YEAR FILTER
# --------------------------------------------------
min_year = int(WQ_data["Year"].min())
max_year = int(WQ_data["Year"].max())

Year_filter = st.slider(
    "Select Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Filter data based on the selected year range
filtered_data = WQ_data[
    (WQ_data["Year"] >= Year_filter[0]) &
    (WQ_data["Year"] <= Year_filter[1])
]

min_selected_year = Year_filter[0]
max_selected_year = Year_filter[1]

# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------
st.subheader(f"{variable} levels ({min_selected_year}–{max_selected_year})")
st.dataframe(filtered_data[["Year", variable]])

# --------------------------------------------------
# LINE CHART WITH WHO GUIDELINE
# --------------------------------------------------
df_plot = filtered_data[["Year", variable]]
fig = px.line(
    df_plot,
    x="Year",
    y=variable,
    title=f"{variable} levels ({min_selected_year}–{max_selected_year})",
    markers=True
)

# Add WHO guideline as horizontal line
who_value = WHO_GUIDELINES.get(variable, None)
if who_value is not None:
    fig.add_hline(
        y=who_value,
        line_dash="dash",
        line_color="red",
        annotation_text=f"WHO Guideline: {who_value}",
        annotation_position="top left"
    )

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# CONTACT INFO
# --------------------------------------------------
st.header("Contact Information")
email = "MoilwaG@dws.gov.za"
st.write(f"You can reach {name} at {email}.")
