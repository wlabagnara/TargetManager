'''
UDP Client Keep Alive - The client interface used to 'ping' the target device (UDP server).
'''

import socket
import time as t
import threading as th
from collections import deque

class KeepAlive:
    def __init__(self, udp_ip, udp_port, msg_str):
        self.udp_ip =  udp_ip     # UDP_IP = "localhost" (loopback IP address for testing)
        self.udp_port = udp_port  # UDP_PORT = 5005
        self.msg_str = msg_str    # "Hello, World!"

        self.thread = th.Thread(target=self.hello)
        self.time_ticks = 0.050
        self.run_time_tot = 0 # total number of time ticks
        self.running = False

        self.rx_queue = deque()

        self.msg_count_rx_curr = 0 # Message counts
        self.msg_count_rx_prev = 0
        self.msg_count_tx_curr = 0   

        # print (f"UDP target IP: {udp_ip}")
        # print (f"UDP target port: {udp_port}")
        # print (f"message: {msg_str}")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # IPv4 and UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow address/port reuse immediately 

    def hello(self): # this method is invoked as a thread
        while self.running: 
            self.sock.sendto(bytes(self.msg_str, 'utf-8'), (self.udp_ip, self.udp_port))
            self.msg_count_tx_curr = self.msg_count_tx_curr + 1

            data, addr = self.sock.recvfrom(1024)
            msg_rx = f"Client received message: {data.decode()}"
            # print(f"{msg_rx}")
            self.rx_queue.append(msg_rx)
            self.msg_count_rx_curr = self.msg_count_rx_curr + 1
            self.run_time_tot = self.run_time_tot + self.time_ticks
            t.sleep(self.time_ticks)

    def get_rx_counts(self):
        """ get receive message counts"""
        return self.msg_count_rx_curr 

    def is_running(self):
        return self.running

    def rx_data_avail(self):
        """ thread is running and has data in it's receive queue"""
        return  (self.running and self.rx_queue)

    def get_rx_data(self):
        """ get data from queue when available"""
        if self.rx_data_avail():
            return  self.rx_queue.popleft()

    def get_tx_counts(self):
        """ get transmit message counts"""
        return self.msg_count_tx_curr

    def get_rx_sync(self):
        """ determines if the application (client) is actively receiving messages """    
        if (self.running == True) and (self.msg_count_rx_curr > self.msg_count_rx_prev):
            self.msg_count_rx_prev = self.msg_count_rx_curr
            return True
        else:
             return False
    
    def get_rx_msg_rate(self):
        if round(self.run_time_tot) > 0:            
            return round(self.msg_count_rx_curr/self.run_time_tot, 2)
        else:
            return 0

    def get_tx_msg_rate(self):
        if round(self.run_time_tot) > 0:            
            return round(self.msg_count_tx_curr/self.run_time_tot, 2)
        else:
            return 0

    def start(self):
        print(f'Starting Keep Alive (Client) Thread!')
        self.running = True
        self.thread.start()

    def stop(self):
        print(f'Stopping Keep Alive (Client) Thread!')
        self.running = False