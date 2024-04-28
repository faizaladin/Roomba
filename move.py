import RPi.GPIO
import time
from rplidar import RPLidar

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

p = GPIO.PWM(ena, 500)
s = GPIO.PWM(enb, 500)

def forward(num):
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    time.sleep(num)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.HIGH)

def stop():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.HIGH)

lidar = RPLidar('/dev/ttyUSB0')  # Adjust port accordingly

try:
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            if distance < 200:  # Adjust the threshold according to your needs
                # Obstacle detected, stop and avoid
                stop()
            else:
                # No obstacle, continue forward
                forward(1)

except KeyboardInterrupt:
    pass

# Clean up GPIO
GPIO.cleanup()

# Stop RPLIDAR
lidar.stop()
lidar.disconnect()
