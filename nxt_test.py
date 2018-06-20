import serial, traceback, wmi, re, bluetooth

def get_device_info(s):
    s.write(b'\x02\x00\x01\x9b')
    return s.read(35)

def search():
    devices = bluetooth.discover_devices(duration=3, lookup_names = True)
    return devices

def serial_port_mac_addr_map():
    c = wmi.WMI()
    map = []
    for sp in c.Win32_SerialPort():
        for b in sp.references(wmi_class='Win32_PnPDevice'):
            e = b.SameElement
            mac = re.match('BTHENUM\\\{.*?\}_LOCALMFG&.*?\\\\.*?([A-F\d]{12})', e.PNPDeviceID).group(1)
            mac = ':'.join([mac[i:i+2] for i in range(0, len(mac), 2)])
            map.append({'port': e.DeviceID, 'addr': mac})
    return map

def bt_mac_addr_map():
    results = search()
    ret_list = []
    if results != None:
        for addr, name in results:
            ret_list.append({'name': name, 'addr': addr})
    return ret_list

def serial_test():
    #print(serial_port_mac_addr_map())
    s = serial.Serial(port='COM5', baudrate=9600, bytesize=8, timeout=3.0, write_timeout=3.0)
    try:
        print(get_device_info(s))
    except:
        traceback.print_exc()
    s.close()

def bt_test():
    serial_ports = serial_port_mac_addr_map()
    bt_devices = bt_mac_addr_map()
    nxts = []
    for port in serial_ports:
        for device in bt_devices:
            if port['addr']==device['addr']:
                nxts.append({'name': device['name'], 'port': port['port']})
    print(nxts)
    for nxt in nxts:
        s = serial.Serial(port=nxt['port'], baudrate=9600, bytesize=8, timeout=3.0, write_timeout=3.0)
        try:
            print('DEVICE INFO FOR', nxt['name'])
            print(get_device_info(s))
        except:
            traceback.print_exc()
        s.close()

if __name__ == '__main__':
    serial_test()
    #bt_test()
