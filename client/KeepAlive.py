"""
    UDP Client Keep Alive - The client interface used to 'ping' the target device (UDP server).
"""

import socket
import time as t
import threading as th
from collections import deque

import datasim.DataSim as ds

class KeepAlive:
    """ Keep alive class for implementation of the host (client-side) UDP/IP connection"""
    def __init__(self, udp_ip, udp_port, msg_str):
        self.udp_ip =  udp_ip     # UDP_IP = "localhost" (loopback IP address for testing)
        self.udp_port = udp_port  # UDP_PORT = 5005
        self.msg_str = msg_str    # "Hello, World!"

        self.thread = th.Thread(target=self.hello)
        self.time_ticks = 1 # seconds per tick
        self.run_time_tot = 0 # total number of time ticks
        self.running = False

        self.rx_queue = deque() # receive data from target hardware
        self.tx_msg = "IDLE"
        self.tx_queue = deque() # send data to target hardware

        self.msg_count_rx_curr = 0 # Message counts
        self.msg_count_rx_prev = 0
        self.msg_count_tx_curr = 0   

        # print (f"UDP target IP: {udp_ip}")
        # print (f"UDP target port: {udp_port}")
        # print (f"message: {msg_str}")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # IPv4 and UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow address/port reuse immediately 

        # data simulate init
        self.data_sim = ds.DataSim()



    def hello(self):
        """ Method is invoked as the client-side thread. """
        while self.running: 
            if self.tx_queue:
                msg_tx = self.tx_queue.popleft()
            else:
                msg_tx = self.tx_msg # keep transmitting last value

            send_msg = self.msg_str + " count: " + str(self.msg_count_tx_curr) + " model in: " + msg_tx
            self.sock.sendto(bytes(send_msg, 'utf-8'), (self.udp_ip, self.udp_port))
            self.msg_count_tx_curr = self.msg_count_tx_curr + 1

            data, addr = self.sock.recvfrom(1024)
            msg_rx = f"Client received message: {data.decode()}"
            # print(f"{msg_rx}")
            self.rx_queue.append(msg_rx)
            self.msg_count_rx_curr = self.msg_count_rx_curr + 1
            self.run_time_tot = self.run_time_tot + self.time_ticks
            self.data_sim.datasim() # simulate data (for GUI plotting) as if received from remote target
            t.sleep(self.time_ticks)

    def get_rx_counts(self):
        """ Get the total number of messages received by the client."""
        return self.msg_count_rx_curr 

    def is_running(self):
        """ Check if the thread is running."""
        return self.running

    def rx_data_avail(self):
        """ Check if thread is running and has data to process in it's receive queue"""
        return  (self.running and self.rx_queue)

    def get_rx_data(self):
        """ Get data from queue when available"""
        if self.rx_data_avail():
            return  self.rx_queue.popleft()

    def tx_data(self, msg_data):
        """ Send data to target hardware when thread is running"""
        if (self.running == True):
            msg_data_str = str(msg_data)
            self.tx_queue.append(msg_data_str)
            self.tx_msg = msg_data_str # hold on to last queue entry

    def get_tx_counts(self):
        """ Get the total number of messages transmitted by the client."""
        return self.msg_count_tx_curr

    def get_rx_sync(self):
        """ Determines if the application (client) is actively receiving messages """    
        if (self.running == True) and (self.msg_count_rx_curr > self.msg_count_rx_prev):
            self.msg_count_rx_prev = self.msg_count_rx_curr
            return True
        else:
             return False
    
    def get_rx_msg_rate(self):
        """ Returns the recieve message rate as calculated by this class."""
        if round(self.run_time_tot) > 0:            
            return round(self.msg_count_rx_curr/self.run_time_tot, 2)
        else:
            return 0

    def get_tx_msg_rate(self):
        """ Returns the transmission message rate as calculated by this class."""
        if round(self.run_time_tot) > 0:            
            return round(self.msg_count_tx_curr/self.run_time_tot, 2)
        else:
            return 0

    def start(self):
        """ Gracefully starts the client-side thread."""
        print(f'Starting Keep Alive (Client) Thread!')
        self.running = True
        self.thread.start()

    def stop(self):
        """ Gracefully stops the client-side thread."""
        print(f'Stopping Keep Alive (Client) Thread!')
        self.running = False