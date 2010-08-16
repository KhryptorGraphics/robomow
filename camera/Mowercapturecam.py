#! /usr/bin/env python

import sys, pygame, sys, time
import os
from PIL import Image
from PIL import ImageEnhance, ImageStat
from PIL import ImageFilter
from pygame.locals import *
import opencv 

# import the necessary things for OpenCV
from opencv import cv
from opencv import highgui
#from opencv.cv import *   
#from opencv.highgui import *   
#from CVtypes import cv


# the codec existing in cvcapp.cpp,
# need to have a better way to specify them in the future
# WARNING: I have see only MPEG1VIDEO working on my computer
H263 = 0x33363255
H263I = 0x33363249
MSMPEG4V3 = 0x33564944
MPEG4 = 0x58564944
MSMPEG4V2 = 0x3234504D
MJPEG = 0x47504A4D
MPEG1VIDEO = 0x314D4950
AC3 = 0x2000
MP2 = 0x50
FLV1 = 0x31564C46

res = (320,240)
pygame.init()
screen = pygame.display.set_mode((320,240))
pygame.display.set_caption('Webcam')
pygame.font.init()
font = pygame.font.SysFont("Courier",11)

def disp(phrase,loc):
    s = font.render(phrase, True, (200,200,200))
    sh = font.render(phrase, True, (50,50,50))
    screen.blit(sh, (loc[0]+1,loc[1]+1))
    screen.blit(s, loc)
brightness = 1.0
contrast = 1.0
shots = 0



# so, here is the main part of the program

if __name__ == '__main__':

    # a small welcome
    print "OpenCV Python capture video"

    # first, create the necessary window
    highgui.cvNamedWindow ('Camera', highgui.CV_WINDOW_AUTOSIZE)
    highgui.cvNamedWindow ('Color Segmentation', highgui.CV_WINDOW_AUTOSIZE)
    highgui.cvNamedWindow ('Canny', highgui.CV_WINDOW_AUTOSIZE)

    # move the new window to a better place
    highgui.cvMoveWindow ('Camera', 10, 10)

    try:
        # try to get the device number from the command line
        device = int (sys.argv [1])

        # got it ! so remove it from the arguments
        del sys.argv [1]
    except (IndexError, ValueError):
        # no device number on the command line, assume we want the 1st device
        device = 0

    if len (sys.argv) == 1:
        # no argument on the command line, try to use the camera
        capture = highgui.cvCreateCameraCapture (device)
        highgui.cvSetCaptureProperty(capture, highgui.CV_CAP_PROP_FRAME_WIDTH, 320)
        highgui.cvSetCaptureProperty(capture, highgui.CV_CAP_PROP_FRAME_HEIGHT, 240)
        contrast = highgui.cvGetCaptureProperty(capture, highgui.CV_CAP_PROP_CONTRAST)
        print contrast
    else:
        # we have an argument on the command line,
        # we can assume this is a file name, so open it
        capture = highgui.cvCreateFileCapture (sys.argv [1])            

    # check that capture device is OK
    if not capture:
        print "Error opening capture device"
        sys.exit (1)

    # capture the 1st frame to get some propertie on it
    frame = highgui.cvQueryFrame (capture)

    # get size of the frame
    frame_size = cv.cvGetSize (frame)
    #print "frame_size = ", frame_size
    
    # get the frame rate of the capture device
    fps = highgui.cvGetCaptureProperty (capture, highgui.CV_CAP_PROP_FPS)
    if fps == 0:
        # no fps getted, so set it to 30 by default
        fps = 30

    # create the writer
    writer = highgui.cvCreateVideoWriter ("captured.mpg", MPEG1VIDEO,
                                          fps, frame_size, True)

    # check the writer is OK
    if not writer:
        print "Error opening writer"
        sys.exit (1)
    print "starting loop"
    while 1:
        # do forever

        # 1. capture the current image
        #frame = highgui.cvQueryFrame (capture)
        #frame = highgui.cvGrabFrame (capture)
        #img = highgui.cvRetrieveFrame (capture)
        #cvGrabFrame(capture);          // capture a frame
        #img=cvRetrieveFrame(capture);  // retrieve the captured frame
        #cvWriteFrame(writer,img);      // add the frame to the file
        

        # handle events
        #k = highgui.cvWaitKey ()
        #print

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                highgui.cvReleaseVideoWriter (writer)
                highgui.cvDestroyAllWindows()
                highgui.cvReleaseCapture (capture)
                pygame.quit()
                #sys.exit()
                break
        
        keyinput = pygame.key.get_pressed()
        #print "key pressed: ", keyinput
        
        if keyinput[K_SPACE]:
            img = highgui.cvQueryFrame (capture)
            if frame is None:
                # no image captured... end the processing
                break
            # display the frames to have a visual output
            highgui.cvShowImage ('Camera', img)
            # write the frame to the output file
            #highgui.cvWriteFrame (writer, img)
        
        if keyinput[K_ESCAPE]:
            # user has press the ESC key, so exit
            highgui.cvReleaseVideoWriter (writer)
            highgui.cvDestroyAllWindows()
            highgui.cvReleaseCapture (capture)
            pygame.quit()
            #sys.exit ()
            break
        
        if keyinput[K_s]:
            highgui.cvSaveImage("snapshot.BMP", img)

        if keyinput[K_b]:
            PILimg = opencv.adaptors.Ipl2PIL(img)
            PILimg = PILimg.filter(ImageFilter.BLUR)
            opencvimg = opencv.adaptors.PIL2Ipl(PILimg)
            highgui.cvShowImage ('Canny', opencvimg)

        if keyinput[K_c]:
            PILimg = opencv.adaptors.Ipl2PIL(img)
            PILimg = PILimg.filter(ImageFilter.CONTOUR)
            opencvimg = opencv.adaptors.PIL2Ipl(PILimg)
            highgui.cvShowImage ('Canny', opencvimg)

        if keyinput[K_t]:
            PILimg = opencv.adaptors.Ipl2PIL(img)
            PILstats =ImageStat.Stat(PILimg)
            print "stat.extrema = ", PILstats.extrema
            print "stat.count = ", PILstats.count
            print "stat.sum = ", PILstats.sum
            print "stat.sum2 = ", PILstats.sum2
            print "stat.mean = ", PILstats.mean
            print "stat.median = ", PILstats.median
            print "stat.rms = ", PILstats.rms
            print "stat.stddev = ", PILstats.stddev
            
        if keyinput[K_e]:
            PILimg = opencv.adaptors.Ipl2PIL(img)
            PILimg = PILimg.filter(ImageFilter.FIND_EDGES)
            opencvimg = opencv.adaptors.PIL2Ipl(PILimg)
            highgui.cvShowImage ('Canny', opencvimg)

        if keyinput[K_m]:
            PILimg = opencv.adaptors.Ipl2PIL(img)
            PILimg = PILimg.filter(ImageFilter.MaxFilter(5))
            opencvimg = opencv.adaptors.PIL2Ipl(PILimg)
            highgui.cvShowImage ('Canny', opencvimg)
            
        if keyinput[K_1]:
            contrast += 0.1
            #highgui.cvSetCaptureProperty(capture, highgui.CV_CAP_PROP_CONTRAST, contrast)
            print "contrast =", contrast
            #print highgui.cvGetCaptureProperty(capture, highgui.CV_CAP_PROP_CONTRAST)
            PILimg = opencv.adaptors.Ipl2PIL(img)
            PILimg = ImageEnhance.Brightness(PILimg).enhance(contrast)
            #convert PIL image Ipl image
            opencvimg = opencv.adaptors.PIL2Ipl(PILimg) 
            highgui.cvShowImage ('Canny', opencvimg)
        
        if keyinput[K_p]:
            # convert it to PIL image
            #im = PIL.Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
            # convert it to IPL image
            #iplimage = adaptors.PIL2Ipl(im)
            #if (sys.argv[2] > 0):
            #    segments = int(sys.argv[2])
            #else:
            #for now just save as a BMP on 
            #highgui.cvSaveImage("snapshot.BMP", img)
            #PILimg = Image.open("snapshot.BMP")
            
            #convert Ipl image to PIL image
            PILimg = opencv.adaptors.Ipl2PIL(img)
            
            segments = 4              
            
            x, y = PILimg.size

            xsegs = x / segments
            ysegs = y / segments
            
            #print x, y
            for yy in range(0, y, ysegs):
                for xx in range(0,x,xsegs):
                    #j = raw_input("press any key")
                    #print "xx, yy =", xx, yy, xx+xsegs, yy+ysegs

                    box = (xx, yy, xx+xsegs, yy+ysegs)
                    cell = PILimg.crop(box)

                    CellPixels = list(cell.getdata())

                    rgbpixel = 0
                    rgbtotal = 0
                    rtotal = 0
                    gtotal =0
                    btotal =0
                    I3Total = 0
                    TotalPixels = 0
                    for pixel in CellPixels:
                        #for rgb in CellPixels[TotalPixels]:
                        #print "pixel RGB = ", pixel
                        r = pixel[0]
                        rtotal += r
                        g = pixel[1]
                        gtotal += g
                        b = pixel[2]
                        btotal += b
                        #print "rgb = ", r, g, b
                        rgbpixel = r+g+b
                        #i1 = (r+g+b) / 3
                        #i2 = (r-b)
                        i3 = ((2*g) - r - b)/2
                        #print "i1 = ", i1
                        #print "i2 = ", i2
                        #print "i3 = ", i3
                        I3Total += i3
                        rgbtotal += rgbpixel/3
                        TotalPixels += 1

                    I3Avg = I3Total / TotalPixels
                    rgbtotalavg = rgbtotal / TotalPixels
                    ravg = rtotal / TotalPixels
                    gavg = gtotal / TotalPixels
                    bavg = btotal / TotalPixels
                    #print "TotalPixels = ", TotalPixels
                    #print "I3Ttotal = ", I3Total
                    #print "I3Avg = ", I3Avg
                    #print "rgbtotalavg = ", rgbtotalavg 
                    #print "ravg = ", ravg
                    #print "gavg = ", gavg
                    #print "bavg = ", bavg

                    if gavg > ravg and gavg > bavg:
                            ravg = 0
                            gavg = 200
                            bavg =0
                    if ravg > bavg and ravg > gavg:
                            ravg = 200
                            gavg = 0
                            bavg =0
                    #cell.save("i.jpg", "JPEG")
                    #cell.paste((i1,i1,i1), box)
                    #cell.save("i1.jpg", "JPEG")
                    #cell.paste((i2,i2,i2), box)
                    #cell.save("i2.jpg", "JPEG")
                    #cell.paste((I3Avg,I3Avg,I3Avg), (0,0,xsegs,ysegs))
                    #cell.save("i3.jpg", "JPEG")
                    #cell.paste((ravg ,gavg ,bavg ), (0,0,xsegs,ysegs))
                    #cell.save("i4.jpg", "JPEG")
                    PILimg.paste((ravg ,gavg ,bavg ), (xx, yy, xx+xsegs, yy+ysegs))
            PILimg.save("Grass8_Postprocess.jpg", "JPEG")
            #PILimg.show()
            #print "trying to show pic"
            #highgui.cvShowImage ('Camera', PILimg)

            #convert PIL image Ipl image
            opencvimg = opencv.adaptors.PIL2Ipl(PILimg)
            print "processed"
            camshot = pygame.image.frombuffer(PILimg.tostring(), res, "RGB")
            screen.blit(camshot, (0,0))
            
            #opencvimg = highgui.cvLoadImage("Grass8_Postprocess.jpg")
            highgui.cvShowImage ('Color Segmentation', opencvimg)
            
            # handle events
            #print "waiting on key press"
            #k = highgui.cvWaitKey ()

            #xsegs = x / segments
            #ysegs = y / segments
        #disp("B:" + str(brightness), (10,16))  
        disp("hello:", (10,28))
        #print "hello"
        pygame.time.wait(10) 
        pygame.display.flip()
    # end working with the writer
    # not working at this time... Need to implement some typemaps...
    # but exiting without calling it is OK in this simple application
    #highgui.cvReleaseVideoWriter (writer)
