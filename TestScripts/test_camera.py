#!/usr/bin/env  python3

import picamera
import time

def TakePicture():
	#
	cameraObject = picamera.PiCamera()
	#
	cameraObject.resolution = (1024,768)
	#
	cameraObject.start_preview()
	#
	fileName = "intruder_"
	fileName += time.ctime()
	fileName += '.jpg'
	#
	cameraObject.capture(fileName)

TakePicture()
