#from gpiozero import Motor
from time import sleep
from RPi._GPIO import *
import RPi.GPIO as GPIO

#motor = Motor(forward=20, backward=21)

#while True:
#	print('forward')
#	motor.forward()
#	time.sleep(5)

#	print('backward')
#	motor.backward()
#	time.sleep(5)

FORWARD	=1
BACKWARD =-1 
STOP=0.0

CH1=0
CH2=0
CH3=0
CH4=0

ENA1 = 26
IN11 = 19
IN21 = 20

ENA2 = 16
IN12 = 13
IN22 = 6

ENA3 = 25
IN13 = 12
IN23 = 24

ENA4 = 17
IN14 = 18
IN24 = 27


def setPinConfig(EN,INA,INB):
	GPIO.setup(EN,GPIO.OUT)
	GPIO.setup(INA,GPIO.OUT)
	GPIO.setup(INB,GPIO.OUT)
	pwm=GPIO.PWM(EN,2000)
	pwm.start(100)
	return pwm

def setMotorControl(pwm,INA,INB,speed,stat):
	pwm.ChangeDutyCycle(100)
	if stat == FORWARD:
		GPIO.output(INA,GPIO.HIGH)
		GPIO.output(INB,GPIO.LOW)

	elif stat == STOP:
		GPIO.output(INA,GPIO.LOW)
		GPIO.output(INB,GPIO.LOW)

	elif stat == BACKWARD:
		GPIO.output(INA,GPIO.LOW)
		GPIO.output(INB,GPIO.HIGH)

GPIO.setmode(GPIO.BCM)
pwmA=setPinConfig(ENA1,IN11,IN21)
pwmB=setPinConfig(ENA2,IN12,IN22)
pwmC=setPinConfig(ENA3,IN13,IN23)
pwmD=setPinConfig(ENA4,IN14,IN24)

def car_forward(speed):
	setMotorControl(pwmA,IN11,IN21,speed,FORWARD)
	setMotorControl(pwmB,IN12,IN22,speed,BACKWARD)
	setMotorControl(pwmC,IN13,IN23,speed,FORWARD)
	setMotorControl(pwmD,IN14,IN24,speed,BACKWARD)
	print("f",speed)

def car_backward(speed):
	setMotorControl(pwmA,IN11,IN21,speed,BACKWARD)
	setMotorControl(pwmB,IN12,IN22,speed,FORWARD)
	setMotorControl(pwmC,IN13,IN23,speed,BACKWARD)
	setMotorControl(pwmD,IN14,IN24,speed,FORWARD)
	print('b',speed)

def car_stop(speed):
	setMotorControl(pwmA,IN11,IN21,speed,STOP)
	setMotorControl(pwmB,IN12,IN22,speed,STOP)
	setMotorControl(pwmC,IN13,IN23,speed,STOP)
	setMotorControl(pwmD,IN14,IN24,speed,STOP)
	print('s',speed)

def car_left(speed):
	setMotorControl(pwmA,IN11,IN21,speed,FORWARD)
	setMotorControl(pwmB,IN12,IN22,0,BACKWARD)
	setMotorControl(pwmC,IN13,IN23,speed,FORWARD)
	setMotorControl(pwmD,IN14,IN24,speed,BACKWARD)
	print('l',speed)

def car_right(speed):
	setMotorControl(pwmA,IN11,IN21,0,FORWARD)
	setMotorControl(pwmB,IN12,IN22,speed,BACKWARD)
	setMotorControl(pwmC,IN13,IN23,speed,FORWARD)
	setMotorControl(pwmD,IN14,IN24,speed,BACKWARD)
	print('r',speed)


#car_forward(100)
#sleep(10)

#car_stop(0)
#sleep(3)

#car_backward(100)
#sleep(10)

car_left(100)
sleep(10)


car_right(100)
sleep(10)

car_forward(100)
sleep(30)

GPIO.cleanup()
