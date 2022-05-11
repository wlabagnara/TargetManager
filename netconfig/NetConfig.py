"""
    Network Configuration
    Utilizing UDP/IP settings for ETH communications
"""

import pandas as pd

class NetConfig(): 
    """ inputs are properties with setters and getters."""
    def __init__(self, host_ip, host_udp, target_ip, target_udp):
        self.host_ip = host_ip
        self.host_udp = host_udp
        self.target_ip = target_ip
        self.target_udp = target_udp

    def _set_default_network_config(self):
        self.target_ip.set("localhost")
        self.target_udp.set("5005")
        self.host_ip.set("localhost")
        self.host_udp.set("5005")

        df = pd.DataFrame({
            'Host':[self.host_ip.get(), self.host_udp.get()],
            'Target':[self.target_ip.get(), self.target_udp.get()]
        })

        df.to_json("network_config.json")
        read_f = pd.read_json("network_config.json")
        return read_f

    def save_network_config(self):
        """ Save the network configuration to a file"""
        df = pd.DataFrame({
            'Host':[self.host_ip.get(), self.host_udp.get()],
            'Target':[self.target_ip.get(), self.target_udp.get()]
        })

        df.to_json("network_config.json")
        print(f'Saved network config file host: {self.host_ip.get()} {self.host_udp.get()} target: {self.target_ip.get()} {self.target_udp.get()}')

    def read_network_config(self):
        """ Read the network configuration from a file """
        
        try:
            read_f = pd.read_json("network_config.json")
        except:
            print(f"Network configuration does not exist, so create default settings file.")
            read_f = self._set_default_network_config()

        host_ip = read_f['Host'][0]
        host_udp = read_f['Host'][1]
        target_ip = read_f['Target'][0]
        target_udp = read_f['Target'][1]
        print(f'Read network config file -- host: {host_ip} {host_udp} target: {target_ip} {target_udp}')
        return (host_ip, host_udp, target_ip, target_udp)

