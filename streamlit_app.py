import streamlit as st
import pandas as pd
import requests as r
import snowflake.connector

st.title("Welcome to Chandra gopal's Streamlit App")
st.text("How can I help you?  🥑")

st.header('🍞Breakfast Menu')
st.text('Omega 3 & Blueberry Oatmeal')
st.text('Kale, Spinach & Rocket Smoothie')
st.text('Hard-Boiled Free-Range Egg')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Apple'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.

st.dataframe(fruits_to_show)

#st.line_chart(my_fruit_list)
st.header("Fruityvice Advice!!!")

fruityvice_response = r.get("https://www.fruityvice.com/api/fruit/watermelon")
# st.text(fruityvice_response.json())
# st.dataframe(fruityvice_response.json())
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
st.dataframe(fruityvice_normalized)

fruit_choice = st.text_input("What fruit information you would like to show?", "kiwi")
st.write("User Entered", fruit_choice)

ft_response = r.get("https://www.fruityvice.com/api/fruit/"+fruit_choice)
ft_normalized = pd.json_normalize(ft_response.json())
st.dataframe(ft_normalized)
