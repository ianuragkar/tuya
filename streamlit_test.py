import streamlit as st
import pandas as pd
import time

# Define a function to get data from some source
def get_data():
  # For simplicity, we use random values here
  # You can replace this with your own logic
  import random
  on = random.choice([True, False])
  w = random.random()
  mA = random.random()
  V = random.random()
  err = random.choice(["OK", "ERROR"])
  return on, w, mA, V, err

# Create an empty dataframe to store the data
df = pd.DataFrame(columns=["time", "on", "w", "mA", "V", "err"])

# Create a slider to control the refresh rate
refresh_rate = st.sidebar.slider("Refresh rate (s)", 0.1, 10.0, 1.0)

# Create placeholders for the plots and the labels
w_plot = st.empty()
mA_plot = st.empty()
V_plot = st.empty()
on_label = st.empty()
err_label = st.empty()

# Loop until the user stops the app
while True:
  # Get the current data
  on, w, mA, V, err = get_data()
  
  # Append the data to the dataframe with a timestamp
  df = df.append({"time": time.time(), "on": on, "w": w, "mA": mA, "V": V, "err": err}, ignore_index=True)
  
  # Plot the data using streamlit line charts
  w_plot.line_chart(df[["w", "time"]])
  mA_plot.line_chart(df[["mA", "time"]])
  V_plot.line_chart(df[["V", "time"]])
  
  # Show the values of on and err using streamlit text
  on_label.text(f"Switch: {on}")
  err_label.text(f"Status: {err}")
  
  # Wait for the refresh rate
  time.sleep(refresh_rate)