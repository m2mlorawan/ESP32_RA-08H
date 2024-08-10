import struct
import time
import bme280
import ubinascii
from LoRaWAN import lora
from cayennelpp import CayenneLPP
from machine import Pin, SoftI2C

lora = lora()

APP_EUI = "0000000000000000"                   # Substitute Your APP_EUI here
DEV_EUI = "1200000000000002"                   # Substitute Your DEV_EUI here
APP_KEY = "20000000000000000000000000000001l"   # Substitute Your APP_KEY here

lora.configure(DEV_EUI, APP_EUI, APP_KEY)

lora.startJoin()
print("Start Join.....")
while not lora.checkJoinStatus():
  print("Joining....")
  time.sleep(1)
print("Join success!")

stop = False
motion = 0
led = Pin(2, Pin.OUT)
temp = 0
pa = 0
hum = 0
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000) 
bme = bme280.BME280(i2c=i2c)

cnt = 1
relay1 = Pin(12, Pin.OUT)
button = Pin(4, Pin.IN)
button.value()
while True:
    print("----------Wait 10 Second---------")
    time.sleep(2.0)
    print("\r\n\r\nPacket No #{}".format(cnt))
    temp, pa, hum = bme.values 
    print("-----------------------------------")
    print("BME280/BMP280 values:")
    temp, pa, hum = bme.values
    print('temp:', temp, ' Hum:', hum , 'PA:', pa)
    print("-----------------------------------")
    
    c = CayenneLPP()
    c.addTemperature(1, float(temp)) 
    c.addBarometricPressure(2, float(pa))
    c.addRelativeHumidity(3, float(hum)) 
    c.addDigitalOutput(4, button.value() )    
    #c.addAnalogOutput(9, 120.0)

    b = (ubinascii.hexlify(c.getBuffer()))
    led.value(1)
    print('')
    print('************    Sending Data Status   **************')
    lora.sendMsg(b.decode('utf-8'))
    print("Sent message:", b.decode('utf-8'))
    time.sleep(2.0)
    led.value(0)
    cnt = cnt + 1
    response = lora.receiveMsg()
    if (response != ""):
       print("Received: ", end=": ")
       print(response)
       



