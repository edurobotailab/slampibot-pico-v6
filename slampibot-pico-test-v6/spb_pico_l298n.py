from machine import Pin
from l298n import L298N
import utime

motor_r = L298N(Pin(2, Pin.OUT), Pin(3, Pin.OUT), Pin(4, Pin.OUT)) # right wheel
motor_l = L298N(Pin(7, Pin.OUT), Pin(6, Pin.OUT), Pin(5, Pin.OUT)) # left wheel

lin_vel_x = 0.5
ang_vel_z = -0.1
delay = 3000 # ms

vml = lin_vel_x - ang_vel_z
vmr = lin_vel_x + ang_vel_z

try:
    while True:
        motor_r.forward(vmr)    
        motor_l.forward(vml)    
        utime.sleep_ms(delay)
        motor_r.backward(vmr)    
        motor_l.backward(vml)    
        utime.sleep_ms(delay)
        motor_r.stop(vmr)
        motor_l.stop(vml)
        utime.sleep_ms(delay)
except KeyboardInterrupt:
    print("Keyboard Interrupt")
finally:
    motor_r.stop(vmr)
    motor_l.stop(vml)
    utime.sleep_ms(delay) 
