import os
import time
import mysql.connector

os.system('modprobe w1-gpio')
os.system('modprobe w1_therm')

temp_sensor = '/sys/bus/w1/devices/28-0000055ab81d/w1_slave'

# mysql db setup
cnx = mysql.connector.connect(user='pi', database='temperatures')
cursor = cnx.cursor()

add_temperature = (	"INSERT INTO bedroom "
			"(taken, temp_f) "
			"VALUES (%s, %s);")
			

def temp_raw():
    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = temp_raw()

    temp_output = lines[1].find('t=')

    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return round(temp_f, 1)

temp_info = (time.strftime('%Y-%m-%d %H:%M:%S'), read_temp())
cursor.execute(add_temperature, temp_info)

cnx.commit()

cursor.close()
cnx.close()
