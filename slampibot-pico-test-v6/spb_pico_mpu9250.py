from machine import I2C, Pin
from mpu9250 import MPU9250
from ak8963 import AK8963
from mpu6500 import MPU6500
import utime
from math import sqrt, atan2, pi, copysign, sin, cos
 
i2c = I2C(id=0, scl=Pin(1), sda=Pin(0), freq=400000) # 400kHz

print('Scanning I2C bus...')
devices = i2c.scan() # this returns a list of devices

device_count = len(devices)

if device_count == 0:
    print('No i2c device found.')
else:
    print(device_count, 'devices found.')

for device in devices:
    print('Decimal address:', device, ", Hex address: ", hex(device))

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

# mpu = MPU9250(i2c, ak8963=ak8963)
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

try:    
    while True:
        mpu9250_rpy() # degree
        mpu9250_gyro()    # rad/s
        utime.sleep_ms(1000)
except KeyboardInterrupt:
    print("Keyboard Interrupt")
finally:
    print("Stop to print mpu9250")
