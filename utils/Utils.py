""" Utility Classes """

class IP_UTILS(): 
    def __init__(self):
        pass

    def is_valid_IP_addr(self, sample_str):
        """ TEST CASES - valid ip address return True
        >>> a = IP_UTILS()
        >>> a.is_valid_IP_addr("1000.10.10.1")
        False
        >>> a.is_valid_IP_addr("10.10.10.1")
        True
        >>> a.is_valid_IP_addr("192.168.1.1")
        True
        >>> a.is_valid_IP_addr("a.1.1.1")
        False
        """            
        import re
        result = True
        match_obj = re.search( r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", sample_str)
        if  match_obj is None:
            result = False
        else:
            for value in match_obj.groups():
                if int(value) > 255:
                    result = False
                    break
        return result

    def get_host_name_ip(self):
        """ TEST CASES - valid ip address return True
        >>> a = IP_UTILS()
        >>> a.get_host_name_ip()
        ('DESKTOP-ORAV2LD', '192.168.0.193')
        """            
        import socket

        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        return (host_name, host_ip)


import doctest # enable doctest
doctest.testmod()
