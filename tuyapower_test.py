import tuyapower

PLUGIP = '10.0.0.31'
# PLUGID = 'bf764d5b886fe012d19b9p'
# PLUGKEY = 'sqrf2g1amfutn4co'    # CLOUD KEY
DEVICEID = 'bf764d5b886fe012d19b9p'
PLUGID = 'sqrf2g1amfutn4co'
PLUGKEY = '172720aeeda39452'    # LOCAL KEY
PLUGVERS = '3.4'

(on, w, mA, V, err) = tuyapower.deviceInfo(PLUGID, PLUGIP, PLUGKEY, PLUGVERS)
print(on, w, mA, V, err)
(on, w, mA, V, err) = tuyapower.deviceInfo(DEVICEID, PLUGIP, PLUGKEY, PLUGVERS)
print(on, w, mA, V, err)

rawData = tuyapower.deviceRaw(PLUGID, PLUGIP, PLUGKEY, PLUGVERS)
print(rawData)

dev = tuyapower.devicePrint(PLUGID, PLUGIP, PLUGKEY, PLUGVERS)
print(dev)

dataJSON = tuyapower.deviceJSON(PLUGID, PLUGIP, PLUGKEY, PLUGVERS)
print(dataJSON)

print(*dir(tuyapower), sep=', ')