import pygame
import Image
from pygame.locals import *
import sys

from opencv import cv as opencv
# Magic class with a method for grabbing images
from opencv import highgui

from opencv import Ipl2PIL

camera = highgui.cvCreateCameraCapture(-1)
cascade = opencv.cvLoadHaarClassifierCascade('haarcascade_hand_fist.xml', opencv.cvSize(1,1))
eye_cascade = opencv.cvLoadHaarClassifierCascade('/usr/local/share/opencv/haarcascades/haarcascade_mcs_mouth.xml', opencv.cvSize(1,1))

def get_image():
    im = highgui.cvQueryFrame(camera)
    detect(im)
    #convert Ipl image to PIL image
    return Ipl2PIL(im)

def draw_bounding_boxes(cascade_list, img, r,g,b, width):
    if cascade_list:
        for rect in cascade_list:
            opencv.cvRectangle(img, opencv.cvPoint( int(rect.x), int(rect.y)),
                         opencv.cvPoint(int(rect.x + rect.width), int(rect.y + rect.height)),
                         opencv.CV_RGB(r,g,b), width)

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
    faces = opencv.cvHaarDetectObjects(grayscale, cascade, storage, 1.2, 2, opencv.CV_HAAR_DO_CANNY_PRUNING, opencv.cvSize(100, 100))
#    eyes = opencv.cvHaarDetectObjects(grayscale, eye_cascade, storage, 1.2, 2, opencv.CV_HAAR_DO_CANNY_PRUNING, opencv.cvSize(60,60))
    draw_bounding_boxes(faces, image, 127,255,0, 3)
 #   draw_bounding_boxes(eyes, image, 255,127,0, 1)
    

fps = 30.0
pygame.init()
window = pygame.display.set_mode((640,480))

pygame.display.set_caption("Face-recognition Demo")
screen = pygame.display.get_surface()

#demo image preparation
cv_im = highgui.cvLoadImage("demo.jpg")
detect(cv_im)
pil_im = Ipl2PIL(cv_im)

def read_demo_image():
    return pil_im

while True:
    # Fixed demo for when you have no Webcam
    #im = read_demo_image()
    
    # UNCOMMENT this and comment out the demo when you wish to use webcam
    im = get_image()
    
    pil_img = pygame.image.frombuffer(im.tostring(), im.size, im.mode)
    screen.blit(pil_img, (0,0))
    pygame.display.flip()
    pygame.time.delay(int(1000.0/fps))
