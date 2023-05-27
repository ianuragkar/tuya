import tuyapower
import scan_devices
em = scan_devices.fetch_available_devices(verbose=False)[0]

import datetime
import time
import pandas as pd

def export_csv(df, filename):
    df.to_csv(filename)


stop_time = 10
sampling_freq = 0.1
autosave_freq = 2
df = pd.DataFrame(columns=['time', 'on', 'w', 'mA', 'V', 'err'])
start_time = time.perf_counter()
while True:
    start = time.time()
    on, w, mA, V, err = tuyapower.deviceInfo(em.id, em.ip, em.key, '3.4')
    df.loc[len(df)] = [datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), on, round(w/10, 8), mA, round(V/10, 8), err]
    time.sleep(sampling_freq)
    if time.time() - start >= autosave_freq:
        df.to_csv('energy.csv', index=False, mode='w')
        start = time.time()
    if time.perf_counter() - start_time > stop_time:
        break