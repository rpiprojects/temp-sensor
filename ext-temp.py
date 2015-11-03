import json
import mysql.connector
import time
import urllib2

# mysql db setup
cnx = mysql.connector.connect(user='pi', database='temperatures')
cursor = cnx.cursor()

add_temperature = (
    "INSERT INTO exterior "
    "(taken, temp_f, hum_pct) "
    "VALUES (%s, %s, %s);")

response = urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?zip=60625,us&units=imperial&appid=c2d731ec10b41675520dea9427b1fec3')
data = json.load(response)
response_code = data['cod']
if response_code == 200:
    temp = data['main']['temp'] 
    hum = data['main']['humidity']
    taken = time.strftime('%Y-%m-%d %H:%M:%S')
    temp_info = (taken, temp, hum)
    cursor.execute(add_temperature, temp_info)

cnx.commit()

cursor.close()
cnx.close()
