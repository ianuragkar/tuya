import os
import json
import tuyapower
import tinytuya
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class Device():
    id: str
    ip: str
    key: str
    mac: str
    name: str
    prodkey: str

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
                d['productKey']
            )
            if verbose is True:
                for k, v in d.items():
                    print(f"{k:<10}: {v}")
            valid_devs.append(dev)
            return valid_devs

def main():
    em = fetch_available_devices(verbose=False)[0]
    (on, w, mA, V, err) = tuyapower.deviceInfo(em.id, em.ip, em.key, '3.4')
    print((on, w, mA, V, err))

if __name__ == '__main__':
    main()