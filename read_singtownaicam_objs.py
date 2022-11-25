# This Example is Connect With SingTown AI Cam,
# and get Object Detection results.

import struct
import time
from pyb import UART

uart = UART(3, 9600, timeout=10)

def check_crc(message):
    '''
    return 0 if no mistake
    '''
    crc = 0
    for m in message:
        crc ^= m
        for j in range(8):
            if crc & 1:
                crc ^= 0x91
            crc >>= 1
    return crc

def read_singtownaicam_objs(uart):
    '''
    return list of detected objects,
    object is list of 6 numbers: [score, idx, x1, y1, x2, y2]
    score max is 255
    x1,y1 is corner of left top
    x2,y2 is corner of right bottom
    x1,y1,x2,y2 is in pixel, max is 640,480
    
    example: [(140, 1, 322, 1, 616, 54)] means:
        found 1 object,
        score is 140,
        object index is 1,
        x1 is 322, y1 is 1, x2 is 616, y2 is 54
    '''
    while True:
        head = uart.readchar()
        if head != 0xeb:
            print("warning: head1", head)
            continue
        head = uart.readchar()
        if head != 0x90:
            print("warning: head2", head)
            continue
        num = uart.readchar()
        if num == -1:
            print("error: num timeout")
            continue
        payload = uart.read(num*10+1)
        if len(payload) != (num*10+1):
            print("error: payload length not match")
            continue
        if check_crc(bytes([num])+payload) != 0:
            print('error: crc')
            continue
        objs = []
        for i in range(num):
            objs.append(struct.unpack_from("<BBHHHH", payload, 10*i))
        return objs

while(True):
    if uart.any():
        print(read_singtownaicam_objs(uart)) 
        
