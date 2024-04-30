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

def left(num):
    p.start(25)
    s.start(25)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    time.sleep(num)
    stop()

def stop():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.HIGH)

def check_for_objects(scan):
    for measurement in scan:
        angle, quality, distance = measurement
        print(angle, quality, distance)
        if distance < 700:
            return True
    return False

lidar = RPLidar('/dev/ttyUSB0')

info = lidar.get_info()
print(info)

health=lidar.get_health()
print(health)

lidar.start_motor()

scan_data = [0] * 360

while True:
    try:
        forward()
        for scan in lidar.iter_scans(max_buf_meas=5000):
            for (_, angle, distance) in scan:
                scan_data.append(distance)
                non_zero_scan_data = [value for value in scan_data if value!= 0]
                lidar.clean_input()
            if min(non_zero_scan_data) < 100:
                stop()
                break
    except KeyboardInterrupt:
        stop()
        GPIO.cleanup()
        lidar.clean_input()

    except RPLidarException as e:
        lidar.clean_input()
        continue

lidar.stop()

#lidar.disconnect()