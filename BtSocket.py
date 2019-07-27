from bluetooth import *

class BtSocket():
    port = 1

    def __init__(self, mac_addr):
        self.addr = mac_addr
        self.sock = None

    def connect(self):
        self.sock = BluetoothSocket(RFCOMM)
        self.sock.connect((self.addr, self.port))

    def close(self):
        sel.sock.close()

    def send(self, data):
        datalen = len(data)
        len_lsb = datalen & 0xFF
        len_msb = (datalen >> 8) & 0xFF
        dat_arr = [len_lsb, len_msb]
        for dbyte in data:
            dat_arr.append(dbyte)
        dat_arr = bytes(dat_arr)
        self.sock.send(dat_arr)

    def recv(self):
        lenbytes = self.sock.recv(2)
        datalen = lenbytes[0] + (lenbytes[1] << 8)
        data = self.sock.recv(datalen)
        return data
