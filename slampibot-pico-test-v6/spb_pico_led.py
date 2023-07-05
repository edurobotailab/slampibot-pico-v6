from machine import Pin
import utime

led_R1 = Pin(20, Pin.OUT)
led_G1 = Pin(19, Pin.OUT)
led_B1 = Pin(18, Pin.OUT)

led_R2 = Pin(28, Pin.OUT)
led_G2 = Pin(27, Pin.OUT)
led_B2 = Pin(26, Pin.OUT)

try:   
    while True:
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
    utime.sleep_ms(1000)
    
    led_R2.value(0)
    led_G2.value(0)
    led_B2.value(0)
    utime.sleep_ms(1000)
   
