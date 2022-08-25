import streamlit as st
import pandas as pd
import requests as r
import snowflake.connector
from urllib.error import URLError

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = r.get("https://www.fruityvice.com/api/fruit/"+this_fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

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

# fruit_choice = st.text_input("What fruit information you would like to show?", "kiwi")
# st.write("User Entered", fruit_choice)

# ft_response = r.get("https://www.fruityvice.com/api/fruit/"+fruit_choice)
# ft_normalized = pd.json_normalize(ft_response.json())
# st.dataframe(ft_normalized)
try:
  fruit_choice = st.text_input("What fruit information you would like to show?")
  if not fruit_choice:
    st.error("Please select a fruit to get unformation.")
  else:
    #ft_response = r.get("https://www.fruityvice.com/api/fruit/"+fruit_choice)
    #ft_normalized = pd.json_normalize(ft_response.json())
    #st.dataframe(ft_normalized)
    back_from_function = get_fruityvice_data(fruit_choice)
    st.dataframe(back_from_function)

except URLError as a:
  st.error()

# st.stop()

st.header('The fruit load list contains:')

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
    return my_cur.fetchall()
  
if st.button("Get Fruit Load List"):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  st.dataframe(my_data_rows)
  
# st.stop()
# fruit_choice2 = st.text_input("What fruit would you like to add?", "jackfruit")
# st.write("Thanks for adding", fruit_choice2)
# st.text('Thanks for adding jackfruit')
# my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit')")

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit')")
    return "Thanks for adding " + new_fruit
  
add_my_fruit = st.text_input("What fruit would you like to add?")
if st.button("Add a fruit to the list"):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  st.text(back_from_function)
