import time
import random
import pandas as pd
import panel as pn
import hvplot.pandas
import tuyapower
import scan_devices

em = scan_devices.fetch_available_devices(verbose=False)[0]
df = pd.DataFrame(columns=['on', 'w', 'mA', 'V', 'err'])

def fetch_data():
    (on, w, mA, V, err) = tuyapower.deviceInfo(em.id, em.ip, em.key, '3.4')
    return on, w, mA, V, err

# define the update() function that updates the plots and the text
def update():
    # call the fetch_data() function and get the values
    on, w, mA, V, err = fetch_data()
    # append the values as a new row to df
    df.loc[len(df)] = [on, w, mA, V, err]
    # update the plots with the new data
    plot_w.stream(df)
    plot_mA.stream(df)
    plot_V.stream(df)
    # update the text with the last values in columns on and err
    text_on.value = f'On: {on}'
    text_err.value = f'Err: {err}'

# create plots for the columns w, mA and V using hvplot
plot_w = df.hvplot.line(x='index', y='w', color='blue', title='w')
plot_mA = df.hvplot.line(x='index', y='mA', color='green', title='mA')
plot_V = df.hvplot.line(x='index', y='V', color='red', title='V')

# create text widgets for the columns on and err using panel
text_on = pn.widgets.StaticText(name='On')
text_err = pn.widgets.StaticText(name='Err')

# create a panel layout with the plots and the text
layout = pn.Column(pn.Row(plot_w, plot_mA, plot_V), pn.Row(text_on, text_err))

# set an interval to call the update function every 1 second
pn.state.add_periodic_callback(update, period=1000)

# show the layout in a panel webserver
layout.show()
