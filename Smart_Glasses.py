import cv2
import pyttsx3
import RPi.GPIO as GPIO
import serial
import time
from time import sleep
import telepot
import pytesseract
from pytesseract import Output
 
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

#thres = 0.45 # Threshold to detect object
Classes = "None"
classNames = []
classFile = "coco.names"#/home/pi/Desktop/Object_Detection_Files/
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"#/home/pi/Desktop/Object_Detection_Files/
weightsPath = "frozen_inference_graph.pb"#/home/pi/Desktop/Object_Detection_Files/

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

def press() :
    button_state = GPIO.input(16)
    if button_state == True:
        print('Button Pressed...')
        print(map_link)
        bot.sendMessage(receiver_id, map_link)
       # bot.sendMessage(receiver_id2, map_link)
        print('Sended')
        time.sleep(0.2)
def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box,className])
                global Classes
                Classes = className
                
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

    return img,objectInfo
if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)
    #cap.set(10,70)


    while True:
        switch_state = GPIO.input(12)

        if switch_state == True:
            success, ObjectDetection = cap.read()
            result, objectInfo = getObjects(ObjectDetection,0.45,0.2, objects=['person','bird'])
            cv2.imshow("ObjectDetection",ObjectDetection)
            print(Classes)
            press()
            engine.say(Classes)
            engine.runAndWait()
        else :
            press()
            ret, OCR = cap.read()
            text = pytesseract.image_to_string(OCR)
            cv2.imshow('OCR', OCR)
            print(text)
            engine.say(text)
            engine.runAndWait()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
cap.release()
cv2.destroyAllWindows()