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

forward(2)