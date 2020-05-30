from cv2 import cv2
import time, pandas, os
from datetime import datetime
 

first_frame = None
status_list = [None, None]
times = []
df = pandas.DataFrame(columns = ["Start", "End"])
video = cv2.VideoCapture(0)
file_output = 'output.avi'
width = video.get(cv2.CAP_PROP_FRAME_WIDTH)  
height = video.get(cv2.CAP_PROP_FRAME_HEIGHT) 
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(file_output,fourcc, 50.0, (int(width),int(height)))


while True:
    check, frame = video.read()
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "Motion Detector App " + str(datetime.now()),(50,50),font, 0.5, (255,255,255),2, cv2.LINE_AA)
 
    status = 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(21,21),0)
 
    if first_frame is None: 
        first_frame = gray
        continue  
 
    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue 
        status = 1 

    status_list.append(status)
    if status_list[-1] == 1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2]==1:
        times.append(datetime.now())

    cv2.imshow("Motion Detector",gray)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame, frame", frame)
    out.write(frame)
    key = cv2.waitKey(1)
    if key == ord('q'): 
        if status == 1: 
            times.append(datetime.now())
        break

for i in range(0, len(times), 2):
    df = df.append({"Start":times[i], "End":times[i+1]}, ignore_index=True)


df.to_csv("Times.csv")
video.release()
out.release()
cv2.destroyAllWindows