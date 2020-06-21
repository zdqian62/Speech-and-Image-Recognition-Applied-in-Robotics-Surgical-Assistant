from pymata_aio.pymata3 import PyMata3
from math import *

# COM Port
board = PyMata3(com_port="COM4")

# Pin Port
Extension_Servo = 9
Height_Servo = 10
Base_Servo = 11

# Servo Configuration
board.servo_config(Extension_Servo)
board.servo_config(Height_Servo)
board.servo_config(Base_Servo)

# Declarations
Py = 3
L1 = 3.6
L2 = 8.1
L3 = 11.8
a = 7.0
b = 5.0

# Calculation
aa = L1 - L3
bb = L2
Px = sqrt(a**2+b**2)
theta3 = int(atan2(b,a)*180/pi)
alpha = acos((Px**2+Py**2-aa**2-bb**2)/(2*aa*bb))
A = aa**2+bb**2+2*aa*bb*cos(alpha)
B = -2*Px*(aa+bb*cos(alpha))
C = Px**2-bb**2*sin(alpha)**2
theta2 = int(acos((-B-sqrt(B**2-4*A*C))/(2*A))*180/pi)
theta1 = int(theta2 - alpha*180/pi)
cal_Px = aa*cos(theta2*pi/180)+bb*cos(theta1*pi/180)
cal_Py = aa*sin(theta2*pi/180)+bb*sin(theta1*pi/180)
# Swap
if theta2 > theta1:
    i = theta1
    j = theta2
    theta1 = j
    theta2 = i
    cal_Px = aa*cos(theta1*pi/180)+bb*cos(theta2*pi/180)
    cal_Py = aa*sin(theta1*pi/180)+bb*sin(theta2*pi/180)
print('theta1 is %d degrees' % theta1)
print('theta2 is %d degrees' % theta2)
print('theta3 is %d degrees' % theta3)
cal_a = cal_Px*cos(theta3*pi/180)
cal_b = cal_Px*sin(theta3*pi/180)
print("a is %.3f and the calculated a is %.3f" % (a, cal_a))
print("b is %.3f and the calculated b is %.3f" % (b, cal_b))
print("Py is %.3f and the calculated Py is %.3f" % (Py, cal_Py))
    
# Home Position
def setup():
    board.analog_write(Extension_Servo, 90)
    board.analog_write(Height_Servo, 120)
    board.analog_write(Base_Servo, 40)
    board.sleep(3.0) # Time Delay 3s
    
if __name__ == "__main__":
    setup()
    while True:
        board.analog_write(Extension_Servo, (theta1+5))
        board.analog_write(Height_Servo, (-theta2+153))
        board.analog_write(Base_Servo, (theta3+55))
        board.shutdown()
