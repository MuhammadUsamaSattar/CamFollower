import math
import matplotlib.pyplot as plt
from turtle import Turtle, Screen


################################################################################################################################################
#To use the program, modify the Data.txt file in the same folder as CamFollower.py. The name and location of the file must not be changed.
#To define the case. You must first have a line with character '#'. This indicates the start of a new case.
#In the next line you have to define Rb and Rf. You have to put character "|" after each value. The values must be in a particular order.
#From this line you can start defining the segment motions.The format is as below for each case:

#   #
#   Rb|Rf|
#   angle_start|angle_end|segment_type|curve_type|displacement|
#   angle_start|angle_end|segment_type|curve_type|displacement|
#   .
#   .
#   .
#   angle_start|angle_end|segment_type|curve_type|displacement|

#Make sure that the lines are in ascending order. angle_end of one line must be equal to angle_start of the next one. The sum of rise displacements must be equal
#to sum of return displacements. Otherwise, the cam profile wont be a closed curve.
#Although not necessary, but it is advisable to have rise motions at the start, a dwell after the rise and finally return motions.
#Also try to not have large displacements in small angle ranges. As, this can result in impossible meshes, that go inside the cam profile.
#You can modify WIDTH and HEIGHT in CamFollower.py to change the width and height of turtle window

#You have to wait until the drawing for once case is confirmed after which you have to press "Enter" with command line in focus to move onto the next case.
################################################################################################################################################


WIDTH, HEIGHT = 1920, 1080  # coordinate system size


################################################################################################################################################


#type is the type of motion curve from 'Constant Accelaration', 'Simple Harmonic' or 'Cyclodial Motion'
#segment_type is the displacement type from rise, dwell and return
#angle_current is the angle since start of the current motion type. segment_start_angle and segment_end_angles are the angle values at start of end of motion
#total_displacement is the max displacement that the follower achieves during the segment.
#prev_displacement is the total displacement at the end of last segment
def calcDisplacement(angle_current, segment_start_angle, segment_end_angle, segment_type, curve_type, total_displacement, prev_displacement):
    angle_current -= segment_start_angle
    angle_total = segment_end_angle - segment_start_angle
    angle_total *= math.pi/180
    angle_current *= math.pi/180

    if curve_type == 'Constant Accelaration':
        if segment_type == 'rise':
            if angle_current < (angle_total/2):
                y = 2 * total_displacement * ((angle_current/angle_total) ** 2)
            else:
                y = total_displacement * (1 - 2 * ((1 - (angle_current/angle_total)) ** 2))
            y += prev_displacement
        elif segment_type == 'return':
            if angle_current < (angle_total/2):
                y = total_displacement * (1 - 2 * (angle_current/angle_total) ** 2)
            else:
                y = 2 * total_displacement * (1 - (angle_current/angle_total)) ** 2
            y = prev_displacement - total_displacement + y
    
    elif curve_type == 'Simple Harmonic Motion':
        if segment_type == 'rise':
            y = total_displacement * (1 - math.cos((math.pi * angle_current) / angle_total)) / 2
            y += prev_displacement
        elif segment_type == 'return':
            y = total_displacement * (1 + math.cos((math.pi * angle_current) / angle_total)) / 2
            y = prev_displacement - total_displacement + y
    
    elif curve_type == 'Cyclodial Motion':
        if segment_type == 'rise':
            y = total_displacement * ((angle_current/angle_total) - math.sin(2 * math.pi * angle_current / angle_total) / (2 * math.pi))
            y += prev_displacement
        elif segment_type == 'return':
            y = total_displacement * (1 - (angle_current/angle_total) + math.sin(2 * math.pi * angle_current / angle_total) / (2 * math.pi))
            y = prev_displacement - total_displacement + y

    return y

#Calculates the pitch curve radius value
def calcPitchCurve(radius_basecircle, radius_follower, angle_current, displacement):
    angle_current *= math.pi/180
    r = radius_basecircle + radius_follower + displacement

    return r

#Calculates the x portion of the follower motion tangent
def calcXdash(angle_current, angle_next, R_current, R_next):
    angle_current *= math.pi/180
    angle_next *= math.pi/180

    return ((math.cos(angle_current)*(R_next - R_current)/(angle_next - angle_current)) - R_current*math.sin(angle_current))

#Calculates the y portion of the follower motion tangent
def calcYdash(angle_current, angle_next, R_current, R_next):
    angle_current *= math.pi/180
    angle_next *= math.pi/180

    return (math.sin(angle_current)*(R_next - R_current)/(angle_next - angle_current) + R_current*math.cos(angle_current))

#Calculates the x value of the follower location
def calcXFollower(angle_current, displacement):
    angle_current *= math.pi/180
    return (displacement*math.cos(angle_current))

#Calculates the y value of the follower location
def calcYFollower(angle_current, displacement):
    angle_current *= math.pi/180
    return (displacement*math.sin(angle_current))

#Calculates the x and y portions of the cam profile location
def calcCamProfile(follower_x, follower_y, x_dash, y_dash, radius_follower):
    m = math.sqrt(((x_dash) ** 2 + (-y_dash) ** 2))

    P_x = follower_x - radius_follower * (y_dash/m)
    P_y = follower_y + radius_follower * (x_dash/m)

    return (P_x, P_y)

#Puts the various data points in different array from the input file
def generateDataSet(file):
    dataset = []
    read = False

    for line in file:
        if line[0] == '#':
            read = True
            dataset.append([])
        elif read:
            dataset[-1].append(line)

    return dataset

#Converts the read dataset into useable data. Separates the different line in different arrays and then put each of the data info in these individual arrays
def convertDataSet(dataset):
    dataset_new = []
    for i in range(len(dataset)):
        dataset_new.append([])
        for j in range(len(dataset[i])):
            dataset_new[i].append([])

            word = ''
            for char in dataset[i][j]:
                if char != '|':
                    word += char
                else:
                    dataset_new[i][j].append(word)
                    word = ''
    
    parameters = []
    for i in range(len(dataset_new)):
        parameters.append(dataset_new[i][0])
        dataset_new[i].pop(0)

    for i in dataset_new:
        for j in i:
            for k in range(len(j)):
                if k == 0:
                    j[k] = float(j[k])
                elif k == 1:
                    j[k] = float(j[k])
                elif k == 2:
                    j[k] = str(j[k])
                elif k == 3:
                    j[k] = str(j[k])
                elif k == 4:
                    j[k] = float(j[k])

    return dataset_new, parameters

#Determines which segment the motion is in depending upon the current angle
def getSegment(angle, dataset, data_number):
    for i in range(len(dataset[data_number])):
        if (dataset[data_number][i][0] <= angle) and (dataset[data_number][i][1] > angle):
            return i

#Maps distance coordinates to screen pixel locations        
def map(x, x1, x2, y1, y2):
    return (((y2-y1)*(x-x1)/(x2-x1)) + y1)

#Draws the axis lines
def axis(turtle, distance, n):
    position = turtle.position()
    turtle.pendown()

    tick = int(distance/n)
    for _ in range(n):
        turtle.forward(tick)
        turtle.dot()

    turtle.setposition(position)

#Labels the axis with value points
def labelAxis(ivy, distance, min_value, max_value):
    tick_value = (max_value - min_value)/10
    tick_distance = distance/10

    for i in range(10):
        ivy.forward(tick_distance)
        ivy.write(round((tick_value*(i+1) + min_value), 3), font = ('Arial', int(WIDTH/240),'normal'))

#Sets up the axis and all information such as value marking and axis markings
def setupAxis(ivy, max_dis, max_P_x, max_P_y, min_dim):
    if max_P_x > max_P_y:
        max_P = max_P_x
    else:
        max_P = max_P_y

    ivy.penup()
    ivy.goto(WIDTH/12, HEIGHT/12)
    axis(ivy, min_dim, 10)
    
    ivy.penup()
    ivy.goto(WIDTH/12, 0.75*HEIGHT/12)
    labelAxis(ivy, min_dim, 0, 360)

    ivy.penup()
    ivy.goto(3.5*WIDTH/12, 0.5*HEIGHT/12)
    ivy.write("Angle", font = ('Arial', int(WIDTH/192),'bold'))
    

    ivy.penup()
    ivy.goto(WIDTH/12, HEIGHT/12)
    ivy.setheading(90)
    axis(ivy, 10*HEIGHT/12, 10)
    
    ivy.penup()
    ivy.goto(0.85*WIDTH/12, HEIGHT/12)
    ivy.setheading(90)
    labelAxis(ivy, 10*HEIGHT/12, 0, max_dis)

    ivy.penup()
    ivy.goto(0.1*WIDTH/12, HEIGHT/2)
    ivy.write("Displacement", font = ('Arial', int(WIDTH/192),'bold'))
    

    ivy.penup()
    ivy.goto(9*WIDTH/12, HEIGHT/2)
    ivy.setheading(0)
    axis(ivy, min_dim/2, 10)
    ivy.penup()
    ivy.goto(9*WIDTH/12, HEIGHT/2)
    ivy.setheading(180)
    axis(ivy, min_dim/2, 10)
    
    ivy.penup()
    ivy.goto(9*WIDTH/12, 6.1*HEIGHT/12)
    ivy.setheading(0)
    labelAxis(ivy, min_dim/2, 0, max_P+(2*Rf))
    ivy.penup()
    ivy.goto(9*WIDTH/12, 6.1*HEIGHT/12)
    ivy.setheading(180)
    labelAxis(ivy, min_dim/2, 0, max_P+(2*Rf))

    ivy.penup()
    ivy.goto(11.65*WIDTH/12, HEIGHT/2)
    ivy.write("P_x", font = ('Arial', int(WIDTH/192),'bold'))
    

    ivy.penup()
    ivy.goto(9*WIDTH/12, HEIGHT/2)
    ivy.setheading(90)
    axis(ivy, min_dim/2, 10)
    ivy.penup()
    ivy.goto(9*WIDTH/12, HEIGHT/2)
    ivy.setheading(270)
    axis(ivy, min_dim/2, 10)

    ivy.penup()
    ivy.goto(9.05*WIDTH/12, HEIGHT/2)
    ivy.setheading(90)
    labelAxis(ivy, min_dim/2, 0, max_P+(2*Rf))
    ivy.penup()
    ivy.goto(9.05*WIDTH/12, HEIGHT/2)
    ivy.setheading(270)
    labelAxis(ivy, min_dim/2, 0, max_P+(2*Rf))

    ivy.penup()
    ivy.goto(9*WIDTH/12, ((6 + 0.25)*HEIGHT/12 + (min_dim/2)))
    ivy.write("P_y", font = ('Arial', int(WIDTH/192),'bold'))

    ivy.penup()
    ivy.goto(0.05*WIDTH/12, 0.4*HEIGHT/12)
    ivy.pendown()
    ivy.setheading(0)
    ivy.forward(6.25*WIDTH/12)
    ivy.setheading(90)
    ivy.forward(11*HEIGHT/12)
    ivy.setheading(180)
    ivy.forward(6.25*WIDTH/12)
    ivy.setheading(270)
    ivy.forward(11*HEIGHT/12)

    ivy.penup()
    ivy.goto(6.4*WIDTH/12, 0.4*HEIGHT/12)
    ivy.pendown()
    ivy.setheading(0)
    ivy.forward(5.5*WIDTH/12)
    ivy.setheading(90)
    ivy.forward(11*HEIGHT/12)
    ivy.setheading(180)
    ivy.forward(5.5*WIDTH/12)
    ivy.setheading(270)
    ivy.forward(11*HEIGHT/12)

#Plots the displacement curve
def plotDis(ivy, x, y, max_dis):
    ivy.pendown()
    for i in range(len(x)):
        a = map(x[i], 0, 360, WIDTH/12, 6*WIDTH/12)
        b = map(y[i], 0, max_dis, HEIGHT/12, 11*HEIGHT/12)
        ivy.goto(int(a), int(b))

#Plots the cam profile and follower profile
def plotCamProfile(ivy, x, y, max_P_x, max_P_y, Rf, min_dim, R, angles):
    if max_P_x > max_P_y:
        max_P = max_P_x
    else:
        max_P = max_P_y

    x_scaling = (min_dim/2) / (max_P_x + 2*Rf)
    y_scaling = (min_dim/2) / (max_P_y)

    if x_scaling < y_scaling:
        scaling = x_scaling
    else:
        scaling = y_scaling

    ivy.width(1.5)
    for i in range(len(x)):
        a = (scaling * x[i]) + 9*WIDTH/12
        b = (scaling * y[i]) + HEIGHT/2

        if i == 0:
            ivy.goto(int(a), int(b))

        ivy.pendown()
        ivy.goto(int(a), int(b))

    ivy.penup()
    angles.append(angles[0])
    R.append(R[0])
    ivy.color("green")
    for i in range(len(x)):
        a = (scaling * R[i] * math.cos(math.pi * angles[i]/180)) + 9*WIDTH/12
        b = (scaling * R[i] * math.sin(math.pi * angles[i]/180)) + HEIGHT/2

        if i == 0:
            ivy.goto(int(a), int(b))

        ivy.pendown()
        ivy.goto(int(a), int(b))

    ivy.color("black")
    angles.pop(-1)
    R.pop(-1)

    ivy.penup()

    a = (scaling * x[0]) + 9*WIDTH/12
    b = (HEIGHT/2)
    r = scaling*Rf

    ivy.goto(int(a), int(b))

    ivy.pendown()
    ivy.circle(r)

#Main plotting function. Handles all the plotting.
def plotGraphs(max_dis, angles, y, max_P_x, max_P_y, Rf, R):

    if (5*WIDTH/12) < (10*HEIGHT/12):
        min_dim = 5*WIDTH/12
    else:
        min_dim = 10*HEIGHT/12

    setupAxis(ivy, max_dis, max_P_x, max_P_y, min_dim)

    ivy.penup()
    ivy.goto(WIDTH/12, HEIGHT/12)
    plotDis(ivy, angles, y, max_dis)

    ivy.penup()
    plotCamProfile(ivy, P_x, P_y, max_P_x, max_P_y, Rf, min_dim, R, angles)


################################################################################################################################################


f = open('Data.txt', 'r')

dataset = generateDataSet(f)
dataset, parameters = convertDataSet(dataset)

n = 180 #Number of divisions. More divisions will cause the program to run slower but will give more accurate results

#Main loop that iterates through each case
for data_number in range(len(dataset)):
    screen = Screen()
    screen.setup(WIDTH,HEIGHT)
    screen.setworldcoordinates(0, 0, WIDTH, HEIGHT)
    ivy = Turtle(visible=False)
    ivy.speed('fastest')

    y = []
    R = []
    angles = []
    segment_check = 0
    prev_displacement = 0
    Rb = float(parameters[data_number][0])
    Rf = float(parameters[data_number][1])

    #Loop that calculates the R values for each angle value
    for i in range(n):
        angle = i * (360/n)
        angles.append(angle)
    
        segment_number = getSegment(angle, dataset, data_number)
        if segment_number != segment_check:
            prev_displacement = y[-1]
            segment_check = segment_number
        data = dataset[data_number][segment_number]
    
        if data[2] != 'dwell':
            y.append(calcDisplacement(angle,data[0], data[1], data[2], data[3], data[4], prev_displacement))
        elif data[2] == 'dwell':
            dis = 0
            for j in range(segment_number):
                dis += dataset[data_number][j][4]
            y.append(dis)
    
        R.append(calcPitchCurve(Rb, Rf, angle, y[-1]))

    P = []
    angles.append(angles[0])
    R.append(R[0])

    #Loop that calculates the P values
    for i in range(n):
        a,b = (calcCamProfile(calcXFollower(angles[i], R[i]), calcYFollower(angles[i], R[i]), calcXdash(angles[i], angles[i+1], R[i], R[i+1]), calcYdash(angles[i], angles[i+1], R[i], R[i+1]), Rf))
        P.append([a,b])

    angles.pop(-1)
    R.pop(-1)
    P.append(P[0])

    max_dis = -1
    max_P_x = -1
    max_P_y = -1
    
    P_x = [val[0] for val in P]
    P_y = [val[1] for val in P]

    for x in y:
        if abs(x) > max_dis:
            max_dis = x
    
    for x in P_x:
        if abs(x) > max_P_x:
            max_P_x = abs(x)
    
    for x in P_y:
        if abs(x) > max_P_y:
            max_P_y = abs(x)
    
    #Call to graph plotting function
    plotGraphs(max_dis, angles, y, max_P_x, max_P_y, Rf, R)

    input("Press Enter to continue...")
    ivy.reset()