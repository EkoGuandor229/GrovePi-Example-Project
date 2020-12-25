import time
import datetime
import csv
from grovepi import *
from grove_rgb_lcd import *

# Python functions help to organize the code into separate packets.
# They must be declared before use.

# Blink specified LED in 0.25s interval for 2 seconds.
def blink_ligth(led):
    for _ in range(8):
        digitalWrite(led,1)
        time.sleep(0.25)
        digitalWrite(led, 0)
        time.sleep(0.25)


# Handles the printing and saving to file
def handle_sensordata(temperature, humidity, light_intensity, sound_level):
    text = "Temperature:\n" + temperature + " C"
    print(text)
    print_to_display(text)
    
    text =  "Humidity:\n" + humidity + "%"
    print(text)
    print_to_display(text)
    
    text = "Light Intensity:\n" + light_intensity
    print(text)
    print_to_display(text)
    
    text = "Sound Level:\n" + sound_level
    print(text)
    print_to_display(text)
    
    print_to_csv(temperature, humidity, light_intensity, sound_level)
    
    
# Prints text to display and then fades display color from green to red
def print_to_display(text):
    setText(text)
    setRGB(0, 128, 64)
    for c in range(0, 128):
        setRGB(c, 128-c, 0)
        time.sleep(0.01)
        
    time.sleep(2)
    setRGB(0, 0, 0)
    

# Saves the data to a csv-file specified.
def print_to_csv(temperature, humidity, light_intensity, sound_level):
    # Gets the time in the YYYY-MM-DD HH-MM-SS.MS Format
    timestamp = datetime.datetime.now()
    # Add the actual sensordata a list.
    row = [timestamp, temperature, humidity, light_intensity, sound_level]
    # Specify the file, where the data gets saved.
    # In this case sensor_data.csv which is in the folder CSV-Files
    file_path = "CSV-Files/sensor_data.csv"
    # Open the file in the append mode (a+)
    with open(file_path, "a+") as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write sensor data
        csv_writer.writerow(row)
    print("Data sucessfully saved to the csv")
    print_to_display("Save sucessful")
    
    
# connect red led with port D0 and set the Pin to Output
led_red = 2
pinMode(led_red, "OUTPUT")

# connect green led with port D1 and set the Pin to Output
led_green = 3
pinMode(led_green, "OUTPUT")

# connect red led with port D0 and set the Pin to Output
led_blue = 4
pinMode(led_blue, "OUTPUT")

# connect button with port D2 and set the Pin to Input
button = 8
pinMode(button,"INPUT")

# connect LCD-Display with port IC2-1. The Pin does not have to be set.

# connect temperature/humidity sensor to port A0.
temp_hum_sensor = 7

# connect light sensor to port A1.
light_sensor = 1

# connect sound sensor to port A2.
sound_sensor = 2

# Main loop, where the program logic is executed
while True:
    # Try-except-block for error catching and handling
    try:
        #Read button status
        button_status = digitalRead(button)
        # Run the program if the button status is HIGH (True)
        if button_status:
            # Turn off blue LED
            digitalWrite(led_blue,0)
            
            # Get value from temperature/humidity sensor
            [temp, hum] = dht(temp_hum_sensor, 0)
            temperature = str(temp)
            humidity = str(hum)
            
            # Get value from light sensor
            light_intensity = str(analogRead(light_sensor))
            
            # Get value from sound sensor. Only use, if level is above 0
            sound = analogRead(sound_sensor)
            if sound > 0:
                sound_level = str(sound)
                
            # Turn on green LED to signal that measurements are ok.
            digitalWrite(led_green, 1)
            
            # Print sensor values to console and display. \t inserts a tab and \n inserts a newline
            handle_sensordata(temperature, humidity, light_intensity, sound_level)
            
            # Turn off green LED.
            digitalWrite(led_green, 0)
            time.sleep(1)
        # Code execution, if the button status is LOW (False)
        else:
            digitalWrite(led_blue,1)
            time.sleep(1)
                
    # Stop code execution, if ctrl + c is pressed
    except KeyboardInterrupt:
        blink_ligth(led_red)
        print("Shutdown")
        break
    
    except IOError:
        blink_ligth(led_red)
        print("Error with the connection between sensors/actors and the GrovePi")
        break
        
    except Exception as e: 
        blink_ligth(led_red)
        print("An unknown Error occured.\n", e)
        break
    
    finally:
        # Turn off display and leds
        digitalWrite(led_blue,0)
        digitalWrite(led_red, 0)
        digitalWrite(led_green, 0)
        setText("")
        setRGB(0, 0, 0)
        
        

