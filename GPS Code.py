import RPi.GPIO as GPIO
import serial
import time
from time import sleep
import telepot

 
global map_link
map_link = "None"
token = '7195603262:AAFfru3L66ZXMehvSKsmYl6iVHaHBxLr-G0' 
receiver_id = 811872391
# receiver_id2 = 1243468909
bot = telepot.Bot(token)

 
 ser = serial.Serial ("/dev/ttyAMA0")
 gpgga_info = "$GPGGA,"
 GPGGA_buffer = 0
 NMEA_buff = 0
 GPGGA_data_available = ""
 
 
  def convert_to_degrees(raw_value):
     decimal_value = raw_value/100.00
     degrees = int(decimal_value)
     mm_mmmm = (decimal_value - int(decimal_value))/0.6
     position = degrees + mm_mmmm
     position = "%.4f" %(position)
     return position
    
    
 received_data = (str)(ser.read(200)) #read NMEA string received
 GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string
 if (GPGGA_data_available>0):
     GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after “$GPGGA,” string
     NMEA_buff = (GPGGA_buffer.split(','))
     nmea_time = []
     nmea_latitude = []
     nmea_longitude = []
     nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
     nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
     nmea_longitude = NMEA_buff[3]
      print("NMEA Time: ", nmea_time,'\n')
     lat = (float)(nmea_latitude)
     lat = convert_to_degrees(lat)
     longi = (float)(nmea_longitude)
     longi = convert_to_degrees(longi)
      print ("NMEA Latitude:", lat,"NMEA Longitude:", longi,'\n')
     map_link = 'http://maps.google.com/?q=' + lat + ',' + longi
     
     GPIO.setmode(GPIO.BCM)

GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

engine = pyttsx3.init()



def press() :
    button_state = GPIO.input(16)
    if button_state == True:
        print('Button Pressed...')
        print(map_link)
        bot.sendMessage(receiver_id, map_link)
       # bot.sendMessage(receiver_id2, map_link)
        print('Sended')
        time.sleep(0.2)
