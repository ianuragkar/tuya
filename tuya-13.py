import tuyapower
import tinytuya

PLUGIP = '10.0.0.31'
# PLUGID = 'bf764d5b886fe012d19b9p'
# PLUGKEY = 'sqrf2g1amfutn4co'    # CLOUD KEY
DEVICEID = 'bf764d5b886fe012d19b9p'
PLUGID = 'sqrf2g1amfutn4co'
PLUGKEY = '172720aeeda39452'    # LOCAL KEY
PLUGVERS = '3.4'

# tinytuya.set_debug(True) # Turn on Debug - for non-ANSI color use tinytuya.set_debug(True, False)
# a = tinytuya.OutletDevice(DEVICEID, PLUGIP, PLUGKEY)
# a.set_version(3.4)
# # a.set_dpsUsed({"1": None})  # This needs to be a valid datapoint on the device - 1 usually safe
# data =  a.status()
# print(data)

# (on, w, mA, V, err) = tuyapower.deviceInfo(PLUGID, PLUGIP, PLUGKEY, PLUGVERS)
# print(on, w, mA, V, err)
# (on, w, mA, V, err) = tuyapower.deviceInfo(DEVICEID, PLUGIP, PLUGKEY, PLUGVERS)
# print(on, w, mA, V, err)

# Connect to Device
d = tinytuya.OutletDevice(
    dev_id=DEVICEID,
    address=PLUGIP,
    local_key=PLUGKEY, 
    version=3.4)

# Get Status
data = d.status() 
# print('set_status() result %r' % data)

# Turn On
# d.turn_on()

# Turn Off
# d.turn_off()
# print(d.address)
# print(d.cid)
# print(d.port)
# print(d.product)
# print(d.real_local_key)
# print(d.receive)
# print(d.socket)
print(d.status)
# print(d.version)
# print(d.updatedps)
print(d.set_status(not data['dps']['1']))


# print(*dir(d), sep=', ')