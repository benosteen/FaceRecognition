import opencv
from opencv import highgui

import PIL

import os

class CascadeNotFound(Exception):
  pass

class CouldntReadAsImagefile(Exception):
  pass

class ImageFileNotFound(Exception):
  pass

class Recogniser(object):
  def __init__(self, cascade_dir="/usr/local/share/opencv/haarcascades"):
    self._cached_cascades = {}
    self.cascade_dir = cascade_dir
    self.register_cascades()

  def register_cascades(self):
    self.cascades = []
    for cached_cascade in self._cached_cascades:
      del self._cached_cascades[cached_cascade]
    if os.path.isdir(self.cascade_dir):
      for file in [x for x in os.listdir(self.cascade_dir) if x.endswith(".xml")]:
        self.cascades.append(file)

  def get_cascade(self, cascade_name):
    self._cached_cascades[cascade_name] = opencv.cvLoadHaarClassifierCascade(
            os.path.join(self.cascade_dir, cascade_name), opencv.cvSize(1,1))
            #cascade_name, opencv.cvSize(1,1))
    return self._cached_cascades[cascade_name]


  def detect_in_image_file(self, filename, cascade_name, recogn_w = 50, recogn_h = 50, autosearchsize=False):
    if os.path.isfile(filename):
      try:
        pil_image = PIL.Image.open(filename)
      except:
        raise CouldntReadAsImagefile
      if autosearchsize:
        recogn_w, recogn_h = int(pil_image.size[0]/10.0), int(pil_image.size[1]/10.0)
      return self.detect(pil_image, cascade_name, recogn_w, recogn_h)
    else:
      raise ImageFileNotFound

  def detect(self, pil_image, cascade_name, recogn_w = 50, recogn_h = 50):
    # Get cascade:
    cascade = self.get_cascade(cascade_name)

    image = opencv.PIL2Ipl(pil_image) 
    image_size = opencv.cvGetSize(image)
    grayscale = image
    if pil_image.mode == "RGB": 
      # create grayscale version
      grayscale = opencv.cvCreateImage(image_size, 8, 1)
      # Change to RGB2Gray - I dont think itll affect the conversion
      opencv.cvCvtColor(image, grayscale, opencv.CV_BGR2GRAY)
 
    # create storage
    storage = opencv.cvCreateMemStorage(0)
    opencv.cvClearMemStorage(storage)
 
    # equalize histogram
    opencv.cvEqualizeHist(grayscale, grayscale)
 
    # detect objects
    return opencv.cvHaarDetectObjects(grayscale, cascade, storage, 1.2, 2, opencv.CV_HAAR_DO_CANNY_PRUNING, opencv.cvSize(recogn_w, recogn_h))

