import cv2
import numpy as np
import cv_processing

cap = cv2.VideoCapture(0)


while (1):
    #read image from camera to object 'frame'
    _, frame = cap.read()

    #determine dimensions of frame. Its checked to be 480 x 640 x 3 (because of RGB 3 channels)
    #print(frame.shape)

    #convert 'frame' from RGB to HSV and store new image in 'hsv'
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    #set range of red color to filter
    lower_red = np.array([150, 100, 0])
    upper_red = np.array([180, 255, 255])

    #set range of blue color to filer
    lower_blue = np.array([100,50,0])
    upper_blue = np.array([160,255,240])

    #set range of blue color to filer
    lower_yellow = np.array([10,100,0])
    upper_yellow = np.array([60,255,200])

    #set range of blue color to filer
    lower_green = np.array([50,50,0])
    upper_green = np.array([100,255,250])

    #create mask to determine which pixels are within range. Pixel value becomes 255 if its true, 0 if its not.
    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    #blur out the image_mask to minimise noise
    #red_mask = cv2.blur(red_mask, (10, 10))
    #blue_mask = cv2.blur(blue_mask, (10, 10))
    #yellow_mask = cv2.blur(yellow_mask, (10, 10))
    #green_mask = cv2.blur(green_mask, (10, 10))

    #_, red_mask = cv2.threshold(red_mask,245,255,cv2.THRESH_BINARY)
    #_, blue_mask = cv2.threshold(blue_mask, 245, 255, cv2.THRESH_BINARY)
    #_, yellow_mask = cv2.threshold(yellow_mask, 245, 255, cv2.THRESH_BINARY)
    #_, green_mask = cv2.threshold(green_mask, 245, 255, cv2.THRESH_BINARY)

    #overlay mask with original frame image to get the final filtered image
    red_res = cv2.bitwise_and(frame, frame, mask=red_mask)
    blue_res = cv2.bitwise_and(frame, frame, mask=blue_mask)
    yellow_res = cv2.bitwise_and(frame, frame, mask=yellow_mask)
    green_res = cv2.bitwise_and(frame, frame, mask=green_mask)

    """
    Start of KC code to determine the center point of the colored spot
    """

    #create empty list to store mask pixels' coordinates later
    red_mask_list = []
    blue_mask_list = []
    yellow_mask_list = []
    green_mask_list = []

    #res.shape[0] is number of row, res.shape[1] is number of columns
    #this block of code says, if pixel in mask is 255, then append the pixel coordinates into the list color_mask_list
    for i in range(0, red_mask.shape[0], 3):
        for j in range(0, red_mask.shape[1], 3):
            if red_mask[i][j] == 255:
                red_mask_list.append([j,i])

    for i in range(0, blue_mask.shape[0], 3):
        for j in range(0, blue_mask.shape[1], 3):
            if blue_mask[i][j] == 255:
                blue_mask_list.append([j,i])

    for i in range(0, yellow_mask.shape[0], 3):
        for j in range(0, yellow_mask.shape[1], 3):
            if yellow_mask[i][j] == 255:
                yellow_mask_list.append([j,i])

    for i in range(0, green_mask.shape[0], 3):
        for j in range(0, green_mask.shape[1], 3):
            if green_mask[i][j] == 255:
                green_mask_list.append([j,i])

    #call function to get average pos of colored spot
    red_coordinate = (cv_processing.Average_Pos(red_mask_list))
    blue_coordinate = (cv_processing.Average_Pos(blue_mask_list))
    yellow_coordinate = (cv_processing.Average_Pos(yellow_mask_list))
    green_coordinate = (cv_processing.Average_Pos(green_mask_list))

    #if there is an average coordinate for the color, draw a circle on it
    if red_coordinate != None:
        cv2.circle(frame, (red_coordinate[0], red_coordinate[1]), 10, (255,255,255), -1)

    if blue_coordinate != None:
        cv2.circle(frame, (blue_coordinate[0], blue_coordinate[1]), 10, (255,255,255), -1)

    if yellow_coordinate != None:
        cv2.circle(frame, (yellow_coordinate[0], yellow_coordinate[1]), 10, (255,255,255), -1)

    if green_coordinate != None:
        cv2.circle(frame, (green_coordinate[0], green_coordinate[1]), 10, (255,255,255), -1)

    #draw a line from red to blue
    if red_coordinate != None and blue_coordinate != None:
        cv2.line(frame, (red_coordinate[0], red_coordinate[1]), (blue_coordinate[0], blue_coordinate[1]), (255,255,255))

    #draw a line from red to blue
    if yellow_coordinate != None and green_coordinate != None:
        cv2.line(frame, (yellow_coordinate[0], yellow_coordinate[1]), (green_coordinate[0], green_coordinate[1]), (255,255,255))

    """
    End of KC code to determine the center point of the colored spot
    """



    """
    Start of Code to determine Theta Values
    """

    #joint1 be green to yellow, joint2 be blue to red
    #call self defined function in another python file to obtain theta1 and theta2
    theta1 = cv_processing.get_theta(yellow_coordinate, green_coordinate)
    link2_angle = cv_processing.get_theta(blue_coordinate, red_coordinate)

    if theta1 != None and link2_angle != None:
        theta2 = link2_angle - theta1

        theta1 = round(theta1, 2)
        theta2 = round(theta2, 2)
    else:
        theta2 = None

    theta_display_string = "Theta1: " + str(theta1) + "  Theta2: " + str(theta2)

    """
    End of Code to Determine Theta Value
    """

    """
    Start of Code to create overlay of Camera Feed
    """

    #place project text overlay
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, 'Project Jarvis', (30, 50), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, theta_display_string, (30, 450), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

    """
    End of Code to create overlay of Camera Feed
    """
    #display the frame, mask and final image(res)
    cv2.imshow('frame', frame)
    #cv2.imshow('mask', mask)
    #cv2.imshow('red_res', red_res)
    #cv2.imshow('blue_res', blue_res)
    #cv2.imshow('yellow_res', yellow_res)
    #cv2.imshow('green_res', green_res)
    #cv2.imshow('yellow_mask', yellow_mask)

    #exit program if exit button is pressed
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()