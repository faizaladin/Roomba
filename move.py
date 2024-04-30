from random import randint
import RPi.GPIO as GPIO
import time
from math import floor
from rplidar import RPLidar, RPLidarException 

GPIO.setmode(GPIO.BCM)

ena = 12
enb = 13
in1 = 17
in2 = 27
in3 = 22
in4 = 5

GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(ena, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(enb, GPIO.OUT)

p = GPIO.PWM(ena, 1000)
s = GPIO.PWM(enb, 1000)

def forward():
    p.start(25)
    s.start(25)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)

def set_forward(num):
    p.start(25)
    s.start(25)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    time.sleep(num)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.HIGH)

def set_backward(num):
    p.start(25)
    s.start(25)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    time.sleep(num)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.HIGH)

def left(num):
    p.start(25)
    s.start(25)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    time.sleep(num)

def stop(num):
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.HIGH)
    time.sleep(num)

def check_for_objects(scan):
    for measurement in scan:
        angle, quality, distance = measurement
        print(angle, quality, distance)
        if distance < 700:
            return True
    return False

def move():
    print("restart")
    scans = []
    cooldown = False
    while True:  # Loop indefinitely for continuous scanning
        for scan in lidar.iter_scans(max_buf_meas=5000):
            scans.append(scan)
            if len(scans) == 10:
                print("hit")
                break
        for (_, angle, distance) in scan:
            forward()
            print("Angle: {}, Distance: {}".format(angle, distance))
            if distance < 520 and (angle < 15 or angle > 345):
                obstacle_detected = True
                break
                print("Angle: {}, Distance: {}".format(angle, distance))
        if obstacle_detected:
            print("Obstacle detected! Avoiding...")
            stop(2)
            set_backward(4)
            left(randint(1, 4))
            print("Continuing movement...")
            lidar.clean_input()  # Clear lidar input buffer
            lidar.reset()  # Reset lidar
            time.sleep(2)
            forward()
        else:
            forward()



            




lidar = RPLidar('/dev/ttyUSB0')

info = lidar.get_info()
print(info)

health=lidar.get_health()
print(health)

lidar.start_motor()

scan_data = [0] * 360

while True:
    try:
        move()
    except KeyboardInterrupt:
        stop(2)
        GPIO.cleanup()
        lidar.clean_input()

lidar.stop()

#lidar.disconnect()