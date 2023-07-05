from machine import Pin
from encoder import Encoder
import utime

enc_r = Encoder(Pin(11), Pin(10)) # right wheel
enc_l = Encoder(Pin(12), Pin(13)) # left wheel

try:
    while True:
        print(enc_r.position())
        print(enc_l.position())
        utime.sleep_ms(5)
except KeyboardInterrupt:
    print("Keyboard Interrupt")
finally:
    print("Stop to print encoder")