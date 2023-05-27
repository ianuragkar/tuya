import os
import sys
import json
import logging
import datetime
import tuyapower
import tinytuya
from dataclasses import dataclass
from typing import List, Dict, Tuple

try:
    import tinytuya
    api = "tinytuya"
    api_ver = tinytuya.__version__
except ImportError:
    import pytuya
    api = "pytuya"
    try:
        api_ver = pytuya.__version__
    except:
        api_ver = "unknown"

name = "tuyapower"
version_tuple = (0, 1, 0)
version = version_string = __version__ = "%d.%d.%d" % version_tuple
__author__ = "jasonacox"

log = logging.getLogger(__name__)

log.info("%s version %s", __name__, version)
log.info("Python %s on %s", sys.version, sys.platform)
log.info("Using %s version %r", api, api_ver)

@dataclass
class Device():
    ID: str
    IP: str
    LKEY: str
    MAC: str
    NAME: str
    PKEY: str
    VER: float

@dataclass
class EnergyMeter(Device):
    SWITCH: bool
    VOLTAGE: float #V
    CURRENT: float #A
    POWER: float #W
    FREQUENCY: float #Hz
    PF: float
    TEMP: float #degC
   
    

def local_devices() -> dict:
    if not os.path.exists(os.path.join(os.getcwd(), 'snapshot.json')):
        tinytuya.scan(maxretry=10, color=True)
    with open('snapshot.json') as json_file:
        return json.load(json_file)['devices']

def fetch_available_devices(verbose: bool = True) -> List[Device]:
    valid_devs = []
    devices = local_devices()
    for d in devices:
        if d['name'] != '':
            dev = Device(
                d['id'],
                d['ip'],
                d['key'],
                d['mac'],
                d['name'],
                d['productKey'],
                3.4
            )
            if verbose is True:
                for k, v in d.items():
                    print(f"{k:<10}: {v}")
            valid_devs.append(dev)
            return valid_devs

def format_data(device: Device, data: dict):
    now = datetime.datetime.now()
    iso_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    if data:
        dps = data["dps"]
        sw = dps["9"]
        # Check to see if this is a multiswitch Tuya device
        # assuming DP 2 (switch-2) and 10 (countdown-2) = multiswitch
        if "10" in dps.keys() and "2" in dps.keys():
            # return a dictionary with all switch states
            swDict = {}
            for e in ["1","2","3","4","5","6","7"]:
                if e in dps.keys():
                    swDict[e] = dps[e]
            sw = swDict
        # Check for power data - DP 19 on some 3.1/3.3 devices
        if "19" in dps.keys():
            w = float(dps["19"]) / 100.0
            mA = float(dps["18"])
            V = float(dps["20"]) / 100.0
            f = float(dps["133"]) / 100.0
            pf = float(dps["134"])
            temp = float(dps["135"])
            kwh = float(dps["123"]) / 1000.0 #kWh
            ovp = float(dps["104"]) / 10.0 #V
            ocp = float(dps["105"]) / 100.0 #A
            opp = float(dps["106"]) #W
            lang = str(dps["107"])
            brightness = int(dps["108"])
            standby_brightness = int(dps["109"])
            sleep_time = int(dps["110"])
            switch_mode = str(dps["112"])
            standby_screen = str(dps["117"])
            ovp_recovery_delay = int(dps["137"])
            dev_power_on_switch_state = str(dps["138"])
            key_beep = bool(dps["111"])
            enter_standby_time = dps["110"]
            some_mode = dps["136"] #TODO: identify this
            key = "OK"
        # Check for power data - DP 5 for some 3.1 devices
        elif "5" in dps.keys():
            w = float(dps["5"]) / 100.0
            mA = float(dps["4"])
            V = float(dps["6"]) / 100.0
            key = "OK"
        else:
            key = "Power data unavailable"
        info = dict(
            datetime=iso_time, switch=sw, power=w, current=mA, voltage=V
        )
        log.info(str(info))
    else:
        log.info("Incomplete response from plug %s [%s]." % (device.ID, device.IP))
        key = "Incomplete response"
    return (sw, key, w, mA, V, f, pf, temp, kwh)

def main():
    em = fetch_available_devices(verbose=False)[0]
    rawdata = tuyapower.deviceRaw(em.ID,em.IP,em.LKEY, em.VER)
    (sw, status, w, mA, V, f, pf, temp, kwh) = format_data(em, rawdata)
    print((sw, status, w, mA, V, f, pf, temp, kwh))
    
    # tinytuya.set_debug(True, False)
    
    # a = tinytuya.OutletDevice(em.ID,em.IP,em.LKEY)
    # a.set_version(em.ver)
    # data = a.status()
    # print(data)
    
    # tuyapower.deviceScan(True)
    # tuyapower.devicePrint(em.ID,em.IP,em.LKEY, em.VER)
    
    # for dps, dpsdata in rawdata.items():
    #     for k, v in dpsdata.items():
    #         print(f"{k:<5}: {v}")
    
    # (on, w, mA, V, err) = tuyapower.deviceInfo(em.ID,em.IP,em.LKEY, em.VER)
    # print((on, w, mA, V, err))

if __name__ == '__main__':
    main()