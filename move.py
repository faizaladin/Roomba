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

def spiral():
    lidar = RPLidar('/dev/ttyUSB0')
    #lidar.motor_speed(50)
    counter = 0.5
    lidar_stopped = False
    while True:
        info=lidar.get_info()
        print(info)
        health=lidar.get_health()
        lidar.clean_input()
        for scan in lidar.iter_scans(max_buf_meas=5000):
            for (_, angle, distance) in scan:
                print("Angle: {}, Distance: {}".format(angle, distance))
                if distance < 550 and (angle < 15 or angle > 345):
                    print("object detected")
                    lidar.stop()
                    lidar.stop_motor()
                    lidar.disconect()
                    return move()
            left(0.5)
            set_forward(counter)
            counter += 0.5
            time.sleep(1)
            lidar.clean_input()
            print("cleaning input")
            lidar.reset()
            print("resetting lidar")
            time.sleep(1)
            lidar.start()
            print("starting scan process")
            break


def move():
    lidar = RPLidar('/dev/ttyUSB0')
    while True:  # Loop indefinitely for continuous scanning
        forward()
        lidar.clean_input()
        print("hit")
        info=lidar.get_info()
        print(info)
        health=lidar.get_health()
        print(health)
        lidar_stopped = False
        if lidar_stopped:
            lidar.start_motor()
            lidar.start()
        for scan in lidar.iter_scans(max_buf_meas=5000):
            obstacle_detected = False
            for (_, angle, distance) in scan:
                if distance < 450 and (angle < 15 or angle > 345):
                    obstacle_detected = True
                    break
                print("Angle: {}, Distance: {}".format(angle, distance))
            if obstacle_detected:
                print("Obstacle detected! Avoiding...")
                stop(2)
                set_backward(4)
                left(randint(1, 4))
                print("Continuing movement...")
                forward()
                lidar.clean_input()  # Clear lidar input buffer
                lidar.stop()
                lidar.stop_motor()
                lidar_stopped = True
                time.sleep(1)  # Wait for lidar to reset
                break  # Exit the loop to restart scanning
                
while True:
    try:
        spiral()
    except KeyboardInterrupt:
        stop(2)
        GPIO.cleanup()
        lidar.clean_input()

