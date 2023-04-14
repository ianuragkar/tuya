import logging
from tuya_iot import TuyaOpenAPI as tuya
from tuya_iot import TUYA_LOGGER as tl, TuyaOpenMQ

# Cloud project authorization info	
ACCESS_ID = 'um9pr9ecantnpfgee9wn'	
ACCESS_KEY = 'ea2afe7758484023b101d08e6b33adc4'
# Select an endpoint base on your project availability zone	
# For more info, refer to: https://developer.tuya.com/en/docs/iot/api-request?id=Ka4a8uuo1j4t4	
ENDPOINT = "https://openapi.tuyaeu.com"	
# Enable debug log
tl.setLevel(logging.DEBUG)
	
# Project configuration	
USERNAME = 'camrymontero@yahoo.in'	
PASSWORD = 'anuragcd.1'

DEVICE_ID = 'bf764d5b886fe012d19b9p'
APP_SCHEMA = 'tuyaSmart'

# Initialization of tuya openapi	
openapi = tuya(ENDPOINT, ACCESS_ID, ACCESS_KEY)	
# openapi.connect()
openapi.connect(USERNAME, PASSWORD, 'eu', APP_SCHEMA)

openapi.get(f"/v1.0/iot-03/devices/{DEVICE_ID}")
# openapi.get(f"/v1.0/iot-03/devices/{DEVICE_ID}")
# openapi.get(f"/v1.0/iot-03/devices/{DEVICE_ID}/status") 
# openapi.get(f"/v1.0/iot-03/devices/{DEVICE_ID}/functions") 

commands = {'commands': [{'code': 'switch_1', 'value': True}]}
# request = openapi.post(f'/v1.0/iot-03/devices/{DEVICE_ID}/commands', commands)
# print(response)

# def getDeviceProperties(DEVICE_ID):
#     return tuya.get(f'/v1.0/iot-03/devices/{DEVICE_ID}/specification')

# print(getDeviceProperties(DEVICE_ID))
# print(*dir(TuyaOpenAPI), sep='\n')

def on_message(msg):
    print("on_message: %s" % msg)

# openapi.token_info.expire_time = 0

# openmq = TuyaOpenMQ(openapi)
# openmq.start()
# openmq.add_message_listener(on_message)