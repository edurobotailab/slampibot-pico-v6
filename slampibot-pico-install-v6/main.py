# Copyright 2023 EduRobotAILab CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Leo Cho

from machine import I2C, Pin
from encoder import Encoder
from l298n import L298N
from buzzer_music import music
from mpu9250 import MPU9250
from ak8963 import AK8963
from mpu6500 import MPU6500
from math import sqrt, atan2, pi, copysign, sin, cos
import utime


i2c = I2C(id=0, scl=Pin(1), sda=Pin(0), freq=400000) # 400kHz

# calibration for Magnetometer and Gyro
dummy = MPU9250(i2c)

ak8963 = AK8963(
    i2c,
    offset=(33.39844, -0.1763678, -3.725391), 
    scale=(0.7810696, 0.8247207, 1.971716),
    )

mpu6500 = MPU6500(
    i2c,
    gyro_offset=(-0.03383452, 0.02282055, -0.008768291)
)

mpu = MPU9250(i2c, mpu6500=mpu6500, ak8963=ak8963)
print("")
print("MPU Decimal address:", mpu.whoami, ", MPU Hex address:", hex(mpu.whoami))

# bias offset
pitch_bias = 0.0
roll_bias = 0.0

# For low pass filtering
filtered_x_value = 0.0 
filtered_y_value = 0.0

def degrees_to_heading(degrees):
    heading = ""
    if (degrees > 337) or (degrees >= 0 and degrees <= 22):
            heading = 'N'
    if degrees >22 and degrees <= 67:
        heading = "NE"
    if degrees >67 and degrees <= 112:
        heading = "E"
    if degrees >112 and degrees <= 157:
        heading = "SE"
    if degrees > 157 and degrees <= 202:
        heading = "S"
    if degrees > 202 and degrees <= 247:
        heading = "SW"
    if degrees > 247 and degrees <= 292:
        heading = "W"
    if degrees > 292 and degrees <= 337:
        heading = "NW"
    return heading

def get_reading()->float:
    ''' Returns the readings from the sensor '''
    global filtered_y_value, filtered_x_value
    x = mpu.acceleration[0] 
    y = mpu.acceleration[1]
    z = mpu.acceleration[2] 

    # Pitch and Roll in Radians
    roll_rad = atan2(-x, sqrt((z*z)+(y*y)))
    pitch_rad = atan2(z, copysign(y,y)*sqrt((0.01*x*x)+(y*y)))

    # Pitch and Roll in Degrees
    pitch = pitch_rad*180/pi
    roll = roll_rad*180/pi

    # Get soft_iron adjusted values from the magnetometer
    mag_x, mag_y, mag_z = mpu.magnetic

    filtered_x_value = low_pass_filter(mag_x, filtered_x_value)
    filtered_y_value = low_pass_filter(mag_y, filtered_y_value)

    yaw =  90 - atan2(filtered_y_value, filtered_x_value) * 180 / pi

    # make sure the angle is always positive, and between 0 and 360 degrees
    if yaw < 0:
        yaw += 360
        
    # Adjust for original bias
    pitch -= pitch_bias
    roll -= roll_bias

    heading = degrees_to_heading(yaw)

    return x, y, z, pitch, roll, yaw, heading

def low_pass_filter(raw_value:float, remembered_value):
    ''' Only applied 20% of the raw value to the filtered value '''
    
    # global filtered_value
    alpha = 0.8
    filtered = 0
    filtered = (alpha * remembered_value) + (1.0 - alpha) * raw_value
    return filtered

# reset orientation to zero
x, y, z, pitch_bias, roll_bias, yaw, heading = get_reading()

def mpu9250_rpy():
    ''' Shows the Pitch, Roll and heading '''
    (x, y, z, pitch, roll, yaw, heading_value) = get_reading()    
    # print("Pitch", round(pitch,1), "Roll", round(roll, 1), "Yaw", yaw, "Heading", heading_value)
    # print(roll, pitch, yaw)
    print(round(roll,1), round(pitch,1), round(yaw,1))
    utime.sleep_ms(10)

def mpu9250_gyro():
    print(mpu.gyro) # rad/s
    utime.sleep_ms(10)

enc_r = Encoder(Pin(11), Pin(10)) # right wheel
enc_l = Encoder(Pin(12), Pin(13)) # left wheel

motor_r = L298N(Pin(2, Pin.OUT), Pin(3, Pin.OUT), Pin(4, Pin.OUT)) # right wheel
motor_l = L298N(Pin(7, Pin.OUT), Pin(6, Pin.OUT), Pin(5, Pin.OUT)) # left wheel
       
# pico buzzer
song = '0 E3 1 0;2 E4 1 0;4 E3 1 0;6 E4 1 0;8 E3 1 0;10 E4 1 0;12 E3 1 0;14 E4 1 0;16 A3 1 0;18 A4 1 0;20 A3 1 0;22 A4 1 0;24 A3 1 0;26 A4 1 0;28 A3 1 0;30 A4 1 0;32 G#3 1 0;34 G#4 1 0;36 G#3 1 0;38 G#4 1 0;40 E3 1 0;42 E4 1 0;44 E3 1 0;46 E4 1 0;48 A3 1 0;50 A4 1 0;52 A3 1 0;54 A4 1 0;56 A3 1 0;58 B3 1 0;60 C4 1 0;62 D4 1 0;64 D3 1 0;66 D4 1 0;68 D3 1 0;70 D4 1 0;72 D3 1 0;74 D4 1 0;76 D3 1 0;78 D4 1 0;80 C3 1 0;82 C4 1 0;84 C3 1 0;86 C4 1 0;88 C3 1 0;90 C4 1 0;92 C3 1 0;94 C4 1 0;96 G2 1 0;98 G3 1 0;100 G2 1 0;102 G3 1 0;104 E3 1 0;106 E4 1 0;108 E3 1 0;110 E4 1 0;114 A4 1 0;112 A3 1 0;116 A3 1 0;118 A4 1 0;120 A3 1 0;122 A4 1 0;124 A3 1 0;0 E6 1 1;4 B5 1 1;6 C6 1 1;8 D6 1 1;10 E6 1 1;11 D6 1 1;12 C6 1 1;14 B5 1 1;0 E5 1 6;4 B4 1 6;6 C5 1 6;8 D5 1 6;10 E5 1 6;11 D5 1 6;12 C5 1 6;14 B4 1 6;16 A5 1 1;20 A5 1 1;22 C6 1 1;24 E6 1 1;28 D6 1 1;30 C6 1 1;32 B5 1 1;36 B5 1 1;36 B5 1 1;37 B5 1 1;38 C6 1 1;40 D6 1 1;44 E6 1 1;48 C6 1 1;52 A5 1 1;56 A5 1 1;20 A4 1 6;16 A4 1 6;22 C5 1 6;24 E5 1 6;28 D5 1 6;30 C5 1 6;32 B4 1 6;36 B4 1 6;37 B4 1 6;38 C5 1 6;40 D5 1 6;44 E5 1 6;48 C5 1 6;52 A4 1 6;56 A4 1 6;64 D5 1 6;64 D6 1 1;68 D6 1 1;70 F6 1 1;72 A6 1 1;76 G6 1 1;78 F6 1 1;80 E6 1 1;84 E6 1 1;86 C6 1 1;88 E6 1 1;92 D6 1 1;94 C6 1 1;96 B5 1 1;100 B5 1 1;101 B5 1 1;102 C6 1 1;104 D6 1 1;108 E6 1 1;112 C6 1 1;116 A5 1 1;120 A5 1 1;72 A5 1 6;80 E5 1 6;68 D5 1 7;70 F5 1 7;76 G5 1 7;84 E5 1 7;78 F5 1 7;86 C5 1 7;88 E5 1 6;96 B4 1 6;104 D5 1 6;112 C5 1 6;120 A4 1 6;92 D5 1 7;94 C5 1 7;100 B4 1 7;101 B4 1 7;102 C5 1 7;108 E5 1 7;116 A4 1 7'    
mySong = music(song, pins=[Pin(15)])   

duration=0
try:
    while (duration<380) :
        print(mySong.tick())        
        utime.sleep_ms(40)
        duration +=1
except KeyboardInterrupt:
    print("keyboard interrupt")
finally:
    mySong.stop()

# pico led
led_R1 = Pin(20, Pin.OUT)
led_G1 = Pin(19, Pin.OUT)
led_B1 = Pin(18, Pin.OUT)

led_R2 = Pin(28, Pin.OUT)
led_G2 = Pin(27, Pin.OUT)
led_B2 = Pin(26, Pin.OUT)

try:   
    for i in range(0,2):
        led_R1.value(1)
        led_G1.value(0)
        led_B1.value(0)
        utime.sleep_ms(1000)
        
        led_R1.value(0)
        led_G1.value(1)
        led_B1.value(0)
        utime.sleep_ms(1000)

        led_R1.value(0)
        led_G1.value(0)
        led_B1.value(1)        
        utime.sleep_ms(1000)
        
        led_R2.value(1)
        led_G2.value(0)
        led_B2.value(0)
        utime.sleep_ms(1000)
        
        led_R2.value(0)
        led_G2.value(1)
        led_B2.value(0)
        utime.sleep_ms(1000)

        led_R2.value(0)
        led_G2.value(0)
        led_B2.value(1)        
        utime.sleep_ms(1000)       
except KeyboardInterrupt:
    print("Keyboard Interrupt")
finally:
    led_R1.value(0)
    led_G1.value(0)
    led_B1.value(0)
    
    led_R2.value(0)
    led_G2.value(0)
    led_B2.value(0)
    
    utime.sleep_ms(1000)
