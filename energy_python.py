import tuyapower
import scan_devices
em = scan_devices.fetch_available_devices(verbose=False)[0]

import time
import random
import pandas as pd
import matplotlib.pyplot as plt

# create an empty dataframe with the columns
df = pd.DataFrame(columns=['on', 'w', 'mA', 'V', 'err'])

# define the fetch_data() function that returns random values for the variables
def fetch_data():
    (on, w, mA, V, err) = tuyapower.deviceInfo(em.id, em.ip, em.key, '3.4')
    return on, w, mA, V, err

# define the plot() function that plots the values in df columns w, mA and V
def plot():
    # create a figure with three subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
    # plot the w column as a line plot on ax1
    ax1.plot(df['w'], color='blue')
    ax1.set_ylabel('w')
    # plot the mA column as a line plot on ax2
    ax2.plot(df['mA'], color='green')
    ax2.set_ylabel('mA')
    # plot the V column as a line plot on ax3
    ax3.plot(df['V'], color='red')
    ax3.set_ylabel('V')
    # set the x-axis label as 'time'
    ax3.set_xlabel('time')
    # show the figure
    plt.show()

# create a loop that runs indefinitely
while True:
    # get the current time
    start = time.time()
    # call the fetch_data() function and get the values
    on, w, mA, V, err = fetch_data()
    # append the values as a new row to df
    df.loc[len(df)] = [on, w, mA, V, err]
    # check if one second has passed since the last plot update
    if time.time() - start >= 1:
        # call the plot() function and update the plots
        plot()
        # reset the start time
        start = time.time()
        # check if five seconds have passed since the last plot save
        if time.time() - start >= 5:
            # save the figure as a png file
            plt.savefig('energy.png')
            # reset the start time
            start = time.time()
    # wait for 0.1 second before fetching new data
    time.sleep(0.1)
