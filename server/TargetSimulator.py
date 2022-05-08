"""
    Target Simulator - Simulates a target system (Server) that the Target Manager Client is managing.
"""
# from lib2to3.pgen2.token import EQUAL
import socket
import time as t
import threading as th

# datagen simulator
import csv
import random


class TargetSimulator:
    """ Target simulator class for implementation of the target (server-side) UDP/IP connection"""
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

        # datagen simulate init
        self.datagen_init()

    def get_rx_counts(self):
        """ Get the total number of messages received by the simulated target (server-side)"""
        return self.msg_count_rx_curr

    def get_tx_counts(self):
        """ Get the total number of messages transmitted by the simulated target (server-side)."""
        return self.msg_count_tx_curr

    def get_rx_sync(self):
        """ Determines if the target simulator is actively receiving messages."""
        if (self.running == True) and (self.msg_count_rx_curr > self.msg_count__rx_prev):
            self.msg_count_rx_prev = self.msg_count_rx_curr
            return True
        else:
             return False

    def receiver(self):  # this method is invoked as a thread 
        """ Method is invoked as the server-side thread."""
        while self.running:
                data, addr = self.sock.recvfrom(1024)
                self.msg_count_rx_curr = self.msg_count_rx_curr + 1
                # print (f"Server: message {self.msg_count_rx_curr} received from client")
                
                self.datagen() # generate a simulated data for every receive sample
                
                msg = f' {data.decode()} - {self.msg_count_rx_curr}'  
                self.sock.sendto(msg.encode(), addr)
                self.msg_count_tx_curr = self.msg_count_tx_curr + 1

                # test code to remap localhost string text
                # if self.udp_ip == "localhost": # make loopback address socket compliant
                #     self.udp_ip = "127.0.0.1"
                # self.sock.sendto(str(self.msg_count).encode(), (self.udp_ip, self.udp_port))

    def start(self):
        """ Gracefully starts the server-side thread."""
        print(f'Starting Target Simulator (Server) Thread!')
        self.running = True
        self.thread.start()

    def stop(self):
        """ Gracefully stops the server-side thread."""
        print(f'Stopping Target Simulator (Server) Thread!')
        self.running = False

    def datagen_init(self):
        self.x_value = 0
        self.total_1 = 1000
        self.total_2 = 1000
        self.fieldnames = ["x_value", "total_1", "total_2"]
        self.datagen_file = 'sim_data.csv'
    
        with open(self.datagen_file, 'w') as csv_file:
            self.csv_writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            self.csv_writer.writeheader()

    def datagen(self):
            with open(self.datagen_file, 'a') as csv_file:
                self.csv_writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
                info = {
                    "x_value": self.x_value,
                    "total_1": self.total_1,
                    "total_2": self.total_2
                }
                self.csv_writer.writerow(info)
                # print(self.x_value, self.total_1, self.total_2)
                self.x_value += 1
                self.total_1 = self.total_1 + random.randint(-10, 8)
                self.total_2 = self.total_2 + random.randint(-8, 10)
        

