# this application will display the actual power usage
# the power will be retrieved from the MQTT broker and dislayed
# on the OLED display, and the NEOPüixel ring will change colors and will flash

import time
import network
import json
from neopixel import NeoPixel
from machine import Pin, I2C
import ssd1306 
import secrets
from umqtt.simple import MQTTClient

led = Pin("LED",Pin.OUT)
i2c = I2C(0,sda=Pin(4), scl=Pin(5))
display = ssd1306.SSD1306_I2C(128, 64, i2c)


display.text('PowerMax', 0, 0, 1)
display.show()


numpix = 12 # number of led's
neopin = Pin(0, Pin.OUT)  # GPIO0
pixels = NeoPixel(neopin, numpix)
 

#pixels.set_pixel_line_gradient(3, 13, green, blue)
#pixels.set_pixel_line(14, 16, red)
#pixels.set_pixel(20, (255, 255, 255))
 
# mqtt settings : Topic : smartyreader_enovos/act_pwr_imported_p_plus
# {"act_pwr_imported_p_plus_value":2.48,"act_pwr_imported_p_plus_unit":"kW"}
MQTT_TOPIC_POWER = 'smartyreader_enovos/act_pwr_imported_p_plus'
# MQTT Parameters
MQTT_SERVER = secrets.mqtt_server
MQTT_PORT = 0
MQTT_USER = secrets.mqtt_username
MQTT_PASSWORD = secrets.mqtt_password
MQTT_CLIENT_ID = b'raspberrypi_picow6453'
MQTT_KEEPALIVE = 7200

powerImport = 0.0
# initialize wifi function
def initialize_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # Connect to the network
    wlan.connect(ssid, password)

    # Wait for Wi-Fi connection
    connection_timeout = 10
    while connection_timeout > 0:
        if wlan.status() >= 3:
            break
        connection_timeout -= 1
        display.fill(0)
        display.show()
        display.text('Waiting for WIFI', 00, 20, 1)
        display.show()
        time.sleep(1)

    # Check if connection is successful
    if wlan.status() != 3:
        return False
    else:
        network_info = wlan.ifconfig()
        display.fill(0)
        display.show()
        display.text('Wifi IP', 40, 0, 1)
        display.text(str(network_info[0]), 0, 40, 1)
        display.show()
        return True
#Initialize mqtt connection function
def connect_mqtt():
    try:
        client = MQTTClient(client_id=MQTT_CLIENT_ID,
                            server=MQTT_SERVER,
                            port=MQTT_PORT,
                            user=MQTT_USER,
                            password=MQTT_PASSWORD,
                            keepalive=MQTT_KEEPALIVE)
        client.connect()
        display.fill(0)
        display.show()
        display.text('MQTT', 40, 0, 1)
        display.text("Connection OK", 0, 40, 1)
        display.show()
        return client
    except Exception as e:
        print('Error connecting to MQTT:', e)
        raise  # Re-raise the exception to see the full traceback

# Subcribe to MQTT topics
def subscribe(client, topic):
    client.subscribe(topic)
    display.fill(0)
    display.show()
    display.text('Subscribing to topic', 40, 0, 1)
    display.text(topic, 0, 40, 1)
    display.show()
    
# Callback function that runs when you receive a message on subscribed topic
def my_callback(topic, message):
    global powerImport
    # Perform desired actions based on the subscribed topic and respons
    m_decode=str(message.decode("utf-8","ignore"))  # first decode
    m_in=json.loads(m_decode) # second convert to json data
    powerImport = m_in["act_pwr_imported_p_plus_value"] # third extract data from json Object
    # Check the content of the received message
    led.toggle()
# define the neopixel colors based on value
def set_neopixel_color(np,val):
    n = np.n
    value = val
    
    rgb = [0, 0, 0]
    
    if value <= 0:
        rgb[0] = 0
        rgb[1] = 255
        rgb[2] = 0
    else:
        if value <= 1:
            rgb[0] = 153
            rgb[1] = 204
            rgb[2] = 0 
        else:
            if value <= 2:
                rgb[0] = 255
                rgb[1] = 255
                rgb[2] = 153
            else:
                if value <= 3:
                    rgb[0] = 153
                    rgb[1] = 204
                    rgb[2] = 0
                else:
                    if value <= 4:
                        rgb[0] = 255
                        rgb[1] = 204
                        rgb[2] = 0
                    else:
                        if value <= 5:
                            rgb[0] = 255
                            rgb[1] = 153
                            rgb[2] = 0
                        else:
                            if value <= 6:
                                rgb[0] = 255
                                rgb[1] = 102
                                rgb[2] = 0
                            else:
                                if value <= 7:
                                    rgb[0] = 255
                                    rgb[1] = 0
                                    rgb[2] = 0
                                else:
                                    if value > 7:
                                        rgb[0] = 255
                                        rgb[1] = 0
                                        rgb[2] = 255
    # Set all LEDs to the same color
    for i in range(n):
        np[i] = (int(rgb[0]), int(rgb[1]), int(rgb[2]))
    np.write()
    #np.brightness(42)  # not supported
# main loop
try:
    # Initialize Wi-Fi
    if not initialize_wifi(secrets.wifi_ssid, secrets.wifi_password):
        print('Error connecting to the network... exiting program')
    else:
        # Connect to MQTT broker, start MQTT client
        client = connect_mqtt()
        client.set_callback(my_callback)
        subscribe(client, MQTT_TOPIC_POWER)
        
        # Continuously checking for messages and displaying the value and adapt the led ring
        while True:
            time.sleep(5)
            client.check_msg()
            set_neopixel_color(pixels,powerImport)
            display.fill(0)
            display.show()
            display.text('Power Usage', 20, 0, 1)
            display.text(str(powerImport), 20, 30, 1)
            display.show()
except Exception as e:
    print('Error:', e)
