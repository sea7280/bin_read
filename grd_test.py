from netCDF4 import Dataset
import binascii
import numpy as np
import netCDF4
import open_grd 
import ctypes


lib = ctypes.CDLL("/Users/sakumasouya/Desktop/arakisan/open_grd.so")
lib.print_hello()


path = '/Users/sakumasouya/Desktop/arakisan/dwsw.2000.grd'

data = open_grd.read(path)

print(data)




"""

with netCDF4.Dataset(path,'r') as nc:
    
    key = nc.variable()
    
    print(key)



with open(path, "rb") as grd:

    data = grd.read()
    #print(data)
    #https://docs.python.org/ja/3/library/stdtypes.html#bytearray-objects
    #print(bytearray(data).decode("utf_8"))
    ascii_data = binascii.b2a_hex(data)
    print(ascii_data)

"""