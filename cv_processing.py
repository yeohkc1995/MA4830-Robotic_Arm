import math

#this function will take in a list of [x, y] coordinates and return [average_X, average_Y]. This is to estimate the center point of the colored spot
#e.g. [ [x1,y1], [x2,y2], [x3,y3] ]
def Average_Pos(a):

    if len(a) == 0:
        return

    total_X = 0
    total_Y = 0

    average_X = 0
    average_Y = 0

    for i in a:
        total_X += i[0]
        total_Y += i[1]

    average_X = int(total_X / len(a))
    average_Y = int(total_Y / len(a))

    return [average_X, average_Y]

#this function will take 2 point coordinates as input argument, then output the theta value between them
#input: [x1,y1], [x2,y2]
#output: theta
def get_theta(a,b):

    if (a == None or b == None):
        return

    if b[0] != a[0]:
        basic_angle = math.atan(abs(b[1] - a[1]) / abs(b[0] - a[0]))
        basic_angle = ( basic_angle / (2* 3.142) ) * 360
    else:
        basic_angle = 90

    if (b[0] >= a[0]) and (b[1] >= a[1]):
        return basic_angle

    elif (b[0] <= a[0]) and (b[1] >= a[1]):
        return 180 - basic_angle

    elif (b[0] <= a[0]) and (b[1] <= a[1]):
        return basic_angle + 180

    elif (b[0] >= a[0]) and (b[1] <= a[1]):
        return 360 - basic_angle


#print(Average_Pos([ [100,5], [200,10], [300,15], [400,20] ]))
print(get_theta([1,1], [2,-3]))