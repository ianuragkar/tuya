import tuyapower
import scan_devices

# Importing the required modules
import pandas as pd
import streamlit as st
import time

# Defining the function to fetch data
def fetch_data():
  # Simulating some random data for demonstration purposes
  # You can replace this with your own logic to get the actual data
  import random
  on = random.choice([True, False])
  w = random.randint(1, 10)
  mA = random.uniform(0.1, 1.0)
  V = random.uniform(0.5, 5.0)
  err = random.choice([None, "Low voltage", "High current", "Overload"])
  return on, w, mA, V, err

# Creating an empty dataframe to store the data
df = pd.DataFrame(columns=["on", "w", "mA", "V", "err"])

# Creating a streamlit app
st.title("Data Visualization App")
st.write("This app plots the values of w, mA and V from the fetch_data() function and displays the last values of on and err.")

# Creating placeholders for the plots and the text
plot1 = st.empty()
plot2 = st.empty()
plot3 = st.empty()
text1 = st.empty()
text2 = st.empty()

# Looping indefinitely to update the app
while True:
  # Fetching the data and appending it to the dataframe
  on, w, mA, V, err = fetch_data()
  df.loc[len(df)] = [on, w, mA, V, err]

  # Plotting the values of w, mA and V using line charts
  plot1.line_chart(df["w"])
  plot2.line_chart(df["mA"])
  plot3.line_chart(df["V"])

  # Displaying the last values of on and err using text
  text1.text(f"on: {df['on'].iloc[-1]}")
  text2.text(f"err: {df['err'].iloc[-1]}")

  # Sleeping for one second before updating the app
  time.sleep(1)

