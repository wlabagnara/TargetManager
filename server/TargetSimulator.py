'''
Target Simulator - Simulates a target system (Server) that the Target Manager Client is 'talking' to.
'''
from lib2to3.pgen2.token import EQUAL
import socket
import time as t
import threading as th


class TargetSimulator:

    def __init__(self, udp_ip, udp_port):
        self.udp_ip =  udp_ip     # UDP_IP = "localhost" (loopback IP address for testing)
        self.udp_port = udp_port  # UDP_PORT = 5005

        self.thread = th.Thread(target=self.receiver)
        self.running = False

        self.msg_count_rx_curr = 0 # Message counts
        self.msg_count_rx_prev = 0
        self.msg_count_tx_curr = 0   

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # IPv4 and UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow address/port reuse immediately 
        # self.sock.setblocking(0)   # play with receiver blocking enable/disable
        # self.sock.settimeout(0.3)                       
        self.sock.bind((udp_ip, udp_port))

    def get_rx_counts(self):
        return self.msg_count_rx_curr

    def get_tx_counts(self):
        return self.msg_count_tx_curr

    def get_rx_sync(self):
        """ determines if the simulator (server) is actively receiving messages """
        if (self.running == True) and (self.msg_count_rx_curr > self.msg_count__rx_prev):
            self.msg_count_rx_prev = self.msg_count_rx_curr
            return True
        else:
             return False

    def receiver(self):  # this method is invoked as a thread 
        while self.running:
                data, addr = self.sock.recvfrom(1024)
                self.msg_count_rx_curr = self.msg_count_rx_curr + 1
                print (f"Server: message {self.msg_count_rx_curr} received from client")
                self.sock.sendto(str.encode(str(self.msg_count_rx_curr)), addr)
                self.msg_count_tx_curr = self.msg_count_tx_curr + 1

                # test code for send only
                # if self.udp_ip == "localhost": # make loopback address socket compliant
                #     self.udp_ip = "127.0.0.1"
                # self.sock.sendto(str(self.msg_count).encode(), (self.udp_ip, self.udp_port))

    def start(self):
        print(f'Starting Target Simulator (Server) Thread!')
        self.running = True
        self.thread.start()

    def stop(self):
        print(f'Stopping Target Simulator (Server) Thread!')
        self.running = False
