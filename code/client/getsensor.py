#!/usr/bin/python
import sys
import Adafruit_DHT
import json

def getSensor(verbose=False):
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)

    str_data =  '{0:0.1f} -- {1:0.1f}'.format(temperature, humidity)

    temp = float(str_data.split(' -- ')[0])
    hum = float(str_data.split(' -- ')[1])

    if verbose:
        print(temp, hum)

    data = {'humidity': hum, 'temperature': temp}
    #result = json.dumps(data)
    if verbose:
        print(result)
    #return result
    return data


#getSensor()
