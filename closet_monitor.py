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
import ssl
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
	
def MailImage(sender,recipient,password):
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
	sender = sender
	#
	recipient = recipient
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
	context = ssl.create_default_context()
        #
	ssl_version=ssl.PROTOCOL_TLSv1
        #
	with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as server:
                #
		server.login(sender,password)
                #
		server.sendmail(sender,recipient,text)
                #
	os.remove(imageFile)

def main():
	#
	print("[*] T Closet Monitoring Script")
	#
        '''
        This version of the script is designed to employ an authenticated connection to
        an SMTP relay (gmail at the moment).
        
        You will need to tweak the script if you wish to use the campus SMTP relay.

        '''
	#
	sender = input("[+] Enter the sender's e-mail address-> ")
	#
	recipient = input("[+] Enter the recipient's e-mail address-> ")
	#
	password = getpass("[+] Enter the sender's password-> ")
	#
	print("[*] Starting the monitoring loop...")
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
			MailImage(sender,recipient,password)
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
