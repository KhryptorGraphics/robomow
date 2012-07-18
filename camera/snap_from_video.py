import cv, cv2
import sys


fps = 15

video = cv2.VideoCapture(sys.argv[1])

cv.NamedWindow("Video",cv.CV_WINDOW_AUTOSIZE)


counter = 0
while video.grab():
        counter += 1
        flag, frame = video.retrieve()
        if flag:
                #gray_frm = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                #cv2.imwrite('frame_'+str(counter)+'.png',gray_frm)
				#cv.ShowImage("Video",frame)
				cv2.imshow("Video",frame)
				cv.WaitKey(1000/fps)

