import time
import requests
import pandas as pd
import panel as pn
import hvplot.pandas

# create an empty dataframe with the columns latitude and longitude
df = pd.DataFrame(columns=['latitude', 'longitude'])

# define the fetch_data() function that returns the current coordinates of the ISS from the webserver
def fetch_data():
    # send a GET request to the webserver and get the response as a JSON object
    response = requests.get('https://api.wheretheiss.at/v1/satellites/25544').json()
    # get the latitude and longitude values from the response
    latitude = response['latitude']
    longitude = response['longitude']
    return latitude, longitude

# define the update() function that updates the plot
def update():
    # call the fetch_data() function and get the values
    latitude, longitude = fetch_data()
    # append the values as a new row to df
    df.loc[len(df)] = [latitude, longitude]
    # update the plot with the new data
    plot.stream(df)

# create a plot for the columns latitude and longitude using hvplot
plot = df.hvplot.scatter(x='longitude', y='latitude', title='ISS coordinates')

# create a panel layout with the plot
layout = pn.Column(plot)

# set an interval to call the update function every 1 second
pn.state.add_periodic_callback(update, period=1000)

# show the layout in a panel webserver
layout.show()

# create a loop that runs indefinitely
while True:
    # get the current time
    start = time.time()
    # call the fetch_data() function and get the values
    latitude, longitude = fetch_data()
    # append the values as a new row to df
    df.loc[len(df)] = [latitude, longitude]
    # wait for 0.1 second before fetching new data
    time.sleep(0.1)
