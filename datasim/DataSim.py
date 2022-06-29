"""
    Data Simulator - Simulates a data stream of values in a CSV file.  Useful for showing/demoing data plots on a GUI.
"""

# data simulator
import csv
import random

class DataSim(): 
    def __init__(self):
        self.datasim_init()

    def datasim_init(self):
        self.x_value = 0
        self.total_1 = 1000
        self.total_2 = 1000
        self.fieldnames = ["x_value", "total_1", "total_2"]
        self.datagen_file = 'data_sim_out.csv'
    
        with open(self.datagen_file, 'w') as csv_file:
            print (f"Opening file {self.datagen_file} to store simulation data.")
            self.csv_writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            self.csv_writer.writeheader()

    def datasim(self):
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
