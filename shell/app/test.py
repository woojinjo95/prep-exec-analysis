from adbutils import adb



output = adb.connect("192.168.219.110:5555")
print(output)
print(dir(adb))
print(adb.shell)

device = adb.device("192.168.219.110:5555")
# print(adb.device.shell("ls -alh"))
# print(device.shell("ls -alh"))
# client = adbutils.AdbClient(host="192.168.219.110", port=5555)
# for item in adb.forward_list():
#     print(item.serial, item.local, item.remote)

# print(client.shell2("ls -alh"))
print(dir(device))
print(device.shell2("ls -alh"))

