import streamlit as st
import pandas as pd
import time
import datetime
import scan_devices
import tuyapower
import asyncio
from dataclasses import dataclass, field

@dataclass
class Var():
  NAME: str
  LABEL: str
  UNIT: str
  VALUE: float = field(init=False, default=0)
  LONGLABEL: str = field(init=False)
  
  def __post_init__(self):
    self.LONGLABEL = self.LABEL if self.UNIT is None else f"{self.LABEL} ({self.UNIT})"

p = Var('p', 'Power', 'W')
i = Var('i', 'Current', 'mA')
v = Var('v', 'Voltage', 'V')
f = Var('f', 'Frequency', 'Hz')
pf = Var('pf', 'PowerFactor', None)
temp = Var('temp', 'Temperature', 'C')
e = Var('e', 'Energy', 'kWh')

class ExportData():
  def __init__(self, filename):
    self.file = filename

  def save(df):
    df.tail(1).to_csv(f, header=False, index=False)

# Define a function to get data from some source
em = scan_devices.fetch_available_devices(verbose=False)[0]
def get_data():
  try:
    rawdata = tuyapower.deviceRaw(em.ID,em.IP,em.LKEY, em.VER)
    (sw, status, w, mA, V, f, pf, temp, kwh) = scan_devices.format_data(em, rawdata)
  except:
    (sw, status, w, mA, V, f, pf, temp, kwh) = (0, '404', 0, 0, 0, 0, 0, 0, 0)
  return (sw, status, w, mA, V, f, pf, temp, kwh)

# Create an empty dataframe to store the data
df = pd.DataFrame(columns=[
  "ts",
  "time",
  "Switch",
  "Status",
  "Power (W)",
  "Current (mA)",
  "Voltage (V)",
  "PowerFactor",
  "Frequency (Hz)",
  "Temperature (C)",
  "Energy (kWh)",
])

# Create a slider to control the refresh rate
# refresh_rate = st.slider("Refresh rate", min_value=0.1, max_value=60.0, value=1.0, step=0.1)

st.header(':orange[Tuya Smart Energy Meter]')
# user_colour = st.color_picker(label='Choose a colour for your plot')

# Create streamlit containers for the plots
on_label = st.empty()
status_label = st.empty()

stats = st.empty()

# Create a list of values to choose from
values = [1, 5, 10, 30, 60]
# Create a selectbox with the values
refresh_rate = st.selectbox("Refresh interval (s)", values)

w_chart = st.line_chart() # Power chart
# mA_chart = st.line_chart() # Current chart
# V_chart = st.line_chart() # Voltage chart
pf_chart = st.line_chart() # Power factor chart
# f_chart = st.line_chart() # Frequency chart
# e_chart = st.line_chart() # Energy chart
# temp_chart = st.line_chart() # Temperature chart
csvfile = 'TuyaEnergyMeter.csv'
# Loop until the user stops the app
with open(csvfile, 'a') as f:
  df.to_csv(f, header=f.tell()==0, index=False)
  while True:
    # Get the current data
    (sw, status, w, mA, V, Hz, pfac, t, kwh) = get_data()
    
    # Append the data to the dataframe with a timestamp in excel date format
    now = datetime.datetime.now()
    df = pd.concat(
        [
          df, pd.DataFrame({
          "ts": now,
          "time": pd.to_datetime(now, format="%Y-%m-%d %H:%M:%S"),
          "Switch": sw, 
          "Status": status, 
          "Power (W)": w, 
          "Current (mA)": mA, 
          "Voltage (V)": V, 
          "PowerFactor": pfac,
          "Frequency (Hz)": Hz,
          "Temperature (C)": t,
          "Energy (kWh)": kwh,
          }, index=[0])
        ], axis=0, ignore_index=False
      )
    statsdf = pd.DataFrame(columns=[
        "Quantity",
        "Now",
        "Minimum",
        "Maximum",
        "Mean"
      ])  

    # Loop through the columns of df except time, Switch and Status
    for col in df.columns[4:-1]:
      # Get the last row value from df for the current column
      now = df[col].iloc[-1]
      # Get the minimum, maximum and mean values from df for the current column
      minimum = df[col].min()
      maximum = df[col].max()
      mean = round(df[col].mean(), 3)
      # Create a row in statsdf with the current column name as Quantity and the calculated values as Now, Minimum, Maximum and Mean
      statsdf = pd.concat([
        statsdf, pd.DataFrame({
        "Quantity": col, 
        "Now": now, 
        "Minimum": minimum, 
        "Maximum": maximum, 
        "Mean": mean}, index=[0])
        ], axis=0, ignore_index=True)
      
    if len(df) % int(1 / refresh_rate) == 0:
      stats.dataframe(statsdf.rename(columns={'Quantity':'index'}).set_index('index'), use_container_width=True)
      
      # Add the data to the charts as new rows
      w_chart.add_rows(df[["time", "Power (W)"]].rename(columns={'time':'index'}).set_index('index'))
      # mA_chart.add_rows(df[["time", "Current (mA)"]].rename(columns={'time':'index'}).set_index('index'))
      # V_chart.add_rows(df[["time", "Voltage (V)"]].rename(columns={'time':'index'}).set_index('index'))
      pf_chart.add_rows(df[["time", "PowerFactor"]].rename(columns={'time':'index'}).set_index('index'))
      # f_chart.add_rows(df[["time", "Frequency (Hz)"]].rename(columns={'time':'index'}).set_index('index'))
      # e_chart.add_rows(df[["time", "Energy (kWh)"]].rename(columns={'time':'index'}).set_index('index'))
      # temp_chart.add_rows(df[["time", "Temperature (C)"]].rename(columns={'time':'index'}).set_index('index'))

      # Adjust the x-axis labels according to the time span of the data
      time_span = (df["ts"].max() - df["ts"].min()).total_seconds()
    
    if time_span < 60:
      # Show seconds if the span is less than a minute
      date_format = "%S"
      date_unit = "s"
      
    elif time_span < 3600:
      # Show minutes if the span is less than an hour
      date_format = "%M"
      date_unit = "min"
      
    elif time_span < 86400:
      # Show hours if the span is less than a day
      date_format = "%H"
      date_unit = "h"
      
    else:
      # Show days otherwise
      date_format = "%d"
      date_unit = "d"
      
    
    # Format the x-axis ticks and labels using streamlit.date_input
    
    # for col in (col1, col2, col3):
    #   # Get the current chart element from the column
    #   chart = col.dg._get_delta_generator()._block_container._form_data[-1]
      
      
    #   # Set the locator to show ticks every n units of time (n=1 by default)
    #   chart.x_axis.set_major_locator(st.date_input(unit=date_unit))
      
    #   # Set the formatter to show the date format of the ticks
    #   chart.x_axis.set_major_formatter(st.date_input(date_format))
      
    #   # Rotate the labels for better readability
    #   plt.setp(chart.x_axis.get_majorticklabels(), rotation=45)
    
    
    # Show the values of on and status using streamlit text
    sw_label = "ON" if sw == 1 else "OFF"
    on_label.text(f"Switch: {sw_label}")
    status_label.text(f"Status: {status}")
    
    # Wait for the refresh rate
    time.sleep(0.1)