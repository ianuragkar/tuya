import tinytuya
import tuyapower

PLUGID = 'bf764d5b886fe012d19b9p'
PLUGIP = '10.0.0.19'
PLUGKEY = '20yxxbixxscyqncs'
PLUGVERS = '3.3'

d = tinytuya.OutletDevice(PLUGID, PLUGIP, PLUGKEY)
d.set_version(3.3)
data = d.status()

print(data)






# (on, w, mA, V, err) = tuyapower.deviceInfo(PLUGID, PLUGIP, PLUGKEY, PLUGVERS)
# print(on)
# print(w)
# print(mA)
# print(V)
# print(err)

# rawData = tuyapower.deviceRaw(PLUGID, PLUGIP, PLUGKEY, PLUGVERS)
# print(rawData)

# tuyapower.devicePrint(PLUGID, PLUGIP, PLUGKEY, PLUGVERS)
