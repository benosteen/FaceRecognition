import pygame
import Image
from pygame.locals import *
import sys

import opencv
# Magic class with a method for grabbing images
from opencv import highgui

camera = highgui.cvCreateCameraCapture(-1)

def get_image():
    im = highgui.cvQueryFrame(camera)
    detect(im)
    #convert Ipl image to PIL image
    return opencv.adaptors.Ipl2PIL(im)

def detect(image):
    image_size = opencv.cvGetSize(image)
 
    # create grayscale version
    grayscale = opencv.cvCreateImage(image_size, 8, 1)
    opencv.cvCvtColor(image, grayscale, opencv.CV_BGR2GRAY)
 
    # create storage
    storage = opencv.cvCreateMemStorage(0)
    opencv.cvClearMemStorage(storage)
 
    # equalize histogram
    opencv.cvEqualizeHist(grayscale, grayscale)
 
    # detect objects
    cascade = opencv.cvLoadHaarClassifierCascade('haarcascade_frontalface_alt.xml', opencv.cvSize(1,1))
    faces = opencv.cvHaarDetectObjects(grayscale, cascade, storage, 1.2, 2, opencv.CV_HAAR_DO_CANNY_PRUNING, opencv.cvSize(50, 50))

    if faces:
        for face in faces:
            # Hmm should I do a min-size check?
            # Draw a Chartreuse rectangle Chartruese rocks ;)
            opencv.cvRectangle(image, opencv.cvPoint( int(face.x), int(face.y)),
                         opencv.cvPoint(int(face.x + face.width), int(face.y + face.height)),
                         opencv.CV_RGB(127, 255, 0), 2) # RGB #7FFF00 width=2

fps = 30.0
pygame.init()
window = pygame.display.set_mode((640,480))

pygame.display.set_caption("Face-recognition Demo")
screen = pygame.display.get_surface()

#demo image preparation
cv_im = highgui.cvLoadImage("demo.jpg")
detect(cv_im)
pil_im = opencv.adaptors.Ipl2PIL(cv_im)

def read_demo_image():
    return pil_im

while True:
    # Fixed demo for when you have no Webcam
    im = read_demo_image()
    
    # UNCOMMENT this and comment out the demo when you wish to use webcam
    #im = get_image()
    
    pil_img = pygame.image.frombuffer(im.tostring(), im.size, im.mode)
    screen.blit(pil_img, (0,0))
    pygame.display.flip()
    pygame.time.delay(int(1000.0/fps))
