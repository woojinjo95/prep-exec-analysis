import socket
import struct
import threading
import time
# import pcap
from datetime import datetime
import os
from pypacker import ppcap

# Send/receive based on source/destination data
from pypacker import psocket
from pypacker.layer3 import ip
from pypacker.layer4 import udp
from pypacker.psocket import SocketHndl

# packet_ip = ip.IP(src_s="192.168.126.98", dst_s="239.192.69.11") + udp.UDP(dport=4999)
# psock = psocket.SocketHndl(mode=SocketHndl.MODE_LAYER_3, timeout=10)
# packets = psock.sr(packet_ip, max_packets_recv=1)

# for p in packets:
#     print("got layer 3 packet: %s" % p)
# psock.close()



def socket_igmp(ip: str, port: int, interval: float=0.5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(interval)

    sock.bind((ip, port))
    mreq = struct.pack("4sl", socket.inet_aton(ip), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    start_time = time.time()

    filename = f'network_{start_time}.pcap'
    with ppcap.Writer(filename=filename, linktype=ppcap.DLT_EN10MB) as pwriter:
       
        while time.time() < start_time + interval:
            ts = time.time()
            buffer, address = sock.recvfrom(4090)
            pwriter.write(b'\x01\x00^@E\x0bp]\xcc;6\xd9\x08\x00E\x80\x05LE]\x00\x00\x17\x11\xe4\xed\xc0\xa8~b\xef\xc0E\x0b\x13\x87\xc0D\x058\x00\x00' + buffer)
        sock.close()


if __name__ == '__main__':
    socket_igmp('233.18.158.251', 5000)



# class Socket_IGMP(threading.Thread):
#     def __init__(self, ip, port, duration=10):
#         super(Socket_IGMP, self).__init__()
#         self.duration = duration
#         self.ip = ip
#         self.port = port

#     def run(self):
#         time.sleep(4)
#         MCAST_GRP = self.ip
#         MCAST_PORT = self.port
#         IS_ALL_GROUPS = True
#         self.sock = socket.socket(
#             socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
#         self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         self.sock.settimeout(self.duration)
#         if IS_ALL_GROUPS:
#             self.sock.bind(('', MCAST_PORT))
#         else:
#             self.sock.bind((MCAST_GRP, MCAST_PORT))
#         self.mreq = struct.pack(
#             "4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
#         self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, self.mreq)

#         s = time.time()
#         try:
#             while time.time() < s + self.duration:
#                 self.sock.recv()
#                 pass
#         except socket.timeout:
#             pass
#         finally:
#             self.sock.close()
