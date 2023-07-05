# Author: Olivier Lenoir - <olivier.len02@gmail.com>
# Created: 2020-06-14 21:05:12
# Project: L298 Dual H-bridge, MicroPython
# Description:

from machine import PWM


class L298N(object):

    def __init__(self, ena, in1, in2):
        self.p_ena = PWM(ena)        
        self.p_in1 = in1
        self.p_in2 = in2        
        self.p_ena.freq(1000)        

    def forward(self, speed):
        self.speed = min(1, max(-1, speed))
        self.p_ena.duty_u16(int(65535*self.speed))
        self.p_in1.low()
        self.p_in2.high()
        
    def backward(self, speed):
        self.speed = min(1, max(-1, speed))        
        self.p_ena.duty_u16(int(65535*abs(self.speed)))
        self.p_in1.high()
        self.p_in2.low()
    
    def stop(self, speed):
        self.speed = min(1, max(-1, speed))        
        self.p_ena.duty_u16(int(65535*self.speed))
        self.p_in1.low()
        self.p_in2.low()  
