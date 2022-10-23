#!/usr/bin/env python3

import RPi.GPIO as GPIO
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from getpass import getpass
from email import encoders
import picamera
import smtplib
import signal
import email
import time
import sys
import os

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
	#
	cameraObject.stop_preview()
	#
	cameraObject.close()
	
def MailImage():
	#
	currentDir = os.getcwd()
	#
	dirListing = os.listdir(currentDir)
	#
	imageFile = ""
	#
	for d in dirListing:
		#
		if(d.endswith('jpg')):
			#
			print("[*] Located image file: %s " % d)
			#
			imageFile = d
			#
	sender = 'pi.monitor@wsu.edu'
	#
	recipient = 'robert.gaines@wsu.edu'
	#
	timestamp = time.ctime()
    #
	subject = "Intruder Image -> %s " % timestamp
	#
	body = " Intruder Image -> %s " % timestamp 
    #
	message = MIMEMultipart()
    #
	message['From']    = sender
    #
	message['To']      = recipient
    #
	message['Subject'] = subject
    #
	message.attach(MIMEText(body,"plain"))
    #
	attachment = imageFile
    #
	if(os.path.exists(attachment)):
        #
		print('[*] Image file exists ')
        #
	else:
        #
		print("[!] File could not be located, departing ")
        #
		sys.exit(1)
        #
	with open(attachment,"rb") as attached_file:
		#
		part = MIMEBase("application","octet-stream")
        #
		part.set_payload(attached_file.read())
        #
	encoders.encode_base64(part)
    #
	part.add_header(
        "Content-Disposition",
        f"attachment; filename={attachment}",
        )
    #
	message.attach(part)
    #
	text = message.as_string()
    #
	with smtplib.SMTP("smtp.wsu.edu",25) as server:
		#
		server.sendmail(sender,recipient,text)
		#
	os.remove(imageFile)

def main():
	#
	os.chdir("/home/pi/Desktop/")
	#
	GPIO.setmode(GPIO.BCM)
	#
	DOOR_SENSOR_PIN = 18
	#
	GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	#
	baseCondition = None
	#
	openCondition = None
	#
	closedCondition = None
	#
	while(True):
		#
		baseCondition = openCondition
		#
		openCondition = GPIO.input(DOOR_SENSOR_PIN)
		#
		if(openCondition and (openCondition != baseCondition)):
			#
			print("[*] Door is Open! ")
			#
			TakePicture()
			#
			print("[*] Sending image ")
			#
			MailImage()
			#
			continue
		else:
			print("[X] Door is currently closed !")
			#
			time.sleep(1)
			#
		print("Running...")
		#
		time.sleep(1)

if(__name__ == '__main__'):
	#
	main()
