#code block
import time
import requests
import pandas as pd
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.http import HttpResponse

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

# define the plot() function that plots the values in df columns latitude and longitude
def plot():
    # create a figure with a single subplot
    fig, ax = plt.subplots()
    # plot the latitude and longitude columns as a scatter plot on ax
    ax.scatter(df['longitude'], df['latitude'], color='blue')
    ax.set_xlabel('longitude')
    ax.set_ylabel('latitude')
    ax.set_title('ISS coordinates')
    # save the figure as a png file
    fig.savefig('plot.png')

# define the index() function that renders the django template with the plot
def index(request):
    # call the plot() function and update the plot
    plot()
    # render the template with the context variable
    return render(request, 'plot.html', {'plot': 'plot.png'})

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