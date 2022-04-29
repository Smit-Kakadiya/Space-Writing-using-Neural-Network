import numpy as np
import cv2
from collections import deque

# function of trackbar
def setValues(x):
   print("")


# Creating the trackbars that will be used to change the marker color
cv2.namedWindow("Color detectors")
cv2.createTrackbar("Upper Hue", "Color detectors", 153, 180,setValues)
cv2.createTrackbar("Upper Saturation", "Color detectors", 255, 255,setValues)
cv2.createTrackbar("Upper Value", "Color detectors", 255, 255,setValues)
cv2.createTrackbar("Lower Hue", "Color detectors", 64, 180,setValues)
cv2.createTrackbar("Lower Saturation", "Color detectors", 72, 255,setValues)
cv2.createTrackbar("Lower Value", "Color detectors", 49, 255,setValues)


# Using various arrays to manage color points of various colors
b_points = [deque(maxlen=1024)]
g_points = [deque(maxlen=1024)]
r_points = [deque(maxlen=1024)]
y_points = [deque(maxlen=1024)]

# These indexes will be used to identify the points in specific color arrays.
blue_index_color = 0
yellow_index_color = 0
green_index_color = 0
red_index_color = 0

#The kernel that will be used for dilatation.
kernel = np.ones((5,5),np.uint8)

in_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
color_Index = 0

# Here's how to set up Canvas.
paint_Window = np.zeros((471, 636, 3)) + 255
paint_Window = cv2.rectangle(paint_Window, (40, 1), (140, 65), (0, 0, 0), 2)
paint_Window = cv2.rectangle(paint_Window, (160, 1), (255, 65), in_colors[0], -1)
paint_Window = cv2.rectangle(paint_Window, (275, 1), (370, 65), in_colors[1], -1)
paint_Window = cv2.rectangle(paint_Window, (390, 1), (485, 65), in_colors[2], -1)
paint_Window = cv2.rectangle(paint_Window, (505, 1), (600, 65), in_colors[3], -1)

cv2.putText(paint_Window, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paint_Window, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paint_Window, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paint_Window, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paint_Window, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 2, cv2.LINE_AA)
cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)


# PC's default webcam is being loaded.
cap = cv2.VideoCapture(0)

# Keep looping
while True:
    # Taking a picture with the camera and reading the frame
    ret, frame_f = cap.read()
    #To see the same side of yours, flip the frame around.
    frame_f = cv2.flip(frame_f, 1)
    hsv = cv2.cvtColor(frame_f, cv2.COLOR_BGR2HSV)


    hue_u = cv2.getTrackbarPos("Upper Hue", "Color detectors")
    saturation_u = cv2.getTrackbarPos("Upper Saturation", "Color detectors")
    value_u = cv2.getTrackbarPos("Upper Value", "Color detectors")
    hue_l = cv2.getTrackbarPos("Lower Hue", "Color detectors")
    saturation_l = cv2.getTrackbarPos("Lower Saturation", "Color detectors")
    value_l = cv2.getTrackbarPos("Lower Value", "Color detectors")
    Upper_h = np.array([hue_u, saturation_u, value_u])
    Lower_h = np.array([hue_l, saturation_l, value_l])


    # The color buttons were added to the live frame for color access.
    frame_f = cv2.rectangle(frame_f, (40, 1), (140, 65), (122, 122, 122), -1)
    frame_f = cv2.rectangle(frame_f, (160, 1), (255, 65), in_colors[0], -1)
    frame_f = cv2.rectangle(frame_f, (275, 1), (370, 65), in_colors[1], -1)
    frame_f = cv2.rectangle(frame_f, (390, 1), (485, 65), in_colors[2], -1)
    frame_f = cv2.rectangle(frame_f, (505, 1), (600, 65), in_colors[3], -1)
    cv2.putText(frame_f, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame_f, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame_f, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame_f, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame_f, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 2, cv2.LINE_AA)


    # Making it mask to identify the pointer
    Mask_w = cv2.inRange(hsv, Lower_h, Upper_h)
    Mask_w = cv2.erode(Mask_w, kernel, iterations=1)
    Mask_w = cv2.morphologyEx(Mask_w, cv2.MORPH_OPEN, kernel)
    Mask_w = cv2.dilate(Mask_w, kernel, iterations=1)

    # After idetifying the pointer, find contours for it.
    cnts,_ = cv2.findContours(Mask_w.copy(), cv2.RETR_EXTERNAL,
                              cv2.CHAIN_APPROX_SIMPLE)
    center_w = None

    # contours are formed here
    if len(cnts) > 0:
    	# sorting contours to find the largest
        cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        # Calculate the radius of the enclosing circle that surrounds the discovered contour.
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        # Circumscribe the contour with a circle.
        cv2.circle(frame_f, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        # Calculating the detected contour's center
        M = cv2.moments(cnt)
        center_w = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

        # Now see whether the user wishes to press any of the buttons above the screen.
        if center_w[1] <= 65:
            if 40 <= center_w[0] <= 140: # Clear Button
                b_points = [deque(maxlen=512)]
                g_points = [deque(maxlen=512)]
                r_points = [deque(maxlen=512)]
                y_points = [deque(maxlen=512)]

                blue_index_color = 0
                green_index_color = 0
                red_index_color = 0
                yellow_index_color = 0

                paint_Window[67:, :, :] = 255
            elif 160 <= center_w[0] <= 255:
                    color_Index = 0 # Blue
            elif 275 <= center_w[0] <= 370:
                    color_Index = 1 # Green
            elif 390 <= center_w[0] <= 485:
                    color_Index = 2 # Red
            elif 505 <= center_w[0] <= 600:
                    color_Index = 3 # Yellow
        else :
            if color_Index == 0:
                b_points[blue_index_color].appendleft(center_w)
            elif color_Index == 1:
                g_points[green_index_color].appendleft(center_w)
            elif color_Index == 2:
                r_points[red_index_color].appendleft(center_w)
            elif color_Index == 3:
                y_points[yellow_index_color].appendleft(center_w)
    # When nothing is discovered, append the next deques to avoid any confusion.
    else:
        b_points.append(deque(maxlen=512))
        blue_index_color += 1
        g_points.append(deque(maxlen=512))
        green_index_color += 1
        r_points.append(deque(maxlen=512))
        red_index_color += 1
        y_points.append(deque(maxlen=512))
        yellow_index_color += 1

    # On the canvas, draw lines in all of the colors and frame them.
    points_p = [b_points, g_points, r_points, y_points]
    for a in range(len(points_p)):
        for b in range(len(points_p[a])):
            for c in range(1, len(points_p[a][b])):
                if points_p[a][b][c - 1] is None or points_p[a][b][c] is None:
                    continue
                cv2.line(frame_f, points_p[a][b][c - 1], points_p[a][b][c], in_colors[a], 2)
                cv2.line(paint_Window, points_p[a][b][c - 1], points_p[a][b][c], in_colors[a], 2)

    # Show windows here
    cv2.imshow("Tracking", frame_f)
    cv2.imshow("Paint", paint_Window)
    cv2.imshow("mask", Mask_w)

	# If the 'q' key is pushed, the application will be terminated.
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Allow the camera and all resources to be released.
cap.release()
cv2.destroyAllWindows()