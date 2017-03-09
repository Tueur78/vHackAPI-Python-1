#!/usr/bin/python2.7
#-*- coding: utf-8 

from classes import API
from classes import IP
from classes import Passwords
from utils import Utils
from ocr import OCR
import time
import json
import subprocess
from PIL import Image
import base64
import pytesseract
import cStringIO
import requests
import re


class Console:
	def myinfo(self):
		ut = Utils()
		temp = ut.requestString("user::::pass::::gcm::::uhash", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + "eW7lxzLY9bE:APA91bEO2sZd6aibQerL3Uy-wSp3gM7zLs93Xwoj4zIhnyNO8FLyfcODkIRC1dc7kkDymiWxy_dTQ-bXxUUPIhN6jCUBVvGqoNXkeHhRvEtqAtFuYJbknovB_0gItoXiTev7Lc5LJgP2" + "::::" + "userHash_not_needed", "vh_update.php")
		return temp

	def requestPassword(self,ip):
		ut = Utils()
		arr = ut.requestArray("user::::pass::::target", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + ip, "vh_vulnScan.php")
		imgs = Passwords(arr)
		return imgs

	def enterPassword(self, passwd, target, uhash):
		passwd = passwd.split("p")
		ut = Utils()
		temp = ut.requestString("user::::pass::::port::::target::::uhash", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + str(passwd[1].strip()) + "::::" +  str(target) + "::::" + str(uhash), "vh_trTransfer.php")
		if temp == "10":
			return False
		else:
			return temp

	def scanUser(self):
		ut = Utils()
		arr = ut.requestArray("user::::pass::::", self.api.getUsername() + "::::" + self.api.getPassword() + "::::", "vh_scanHost.php")
		return arr

	def transferMoney(self, ip):
		ut = Utils()
		arr = ut.requestArray("user::::pass::::target", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + ip, "vh_trTransfer.php")
		return arr

	def clearLog(self, ip):
		ut = Utils()
		s = ut.requestString("user::::pass::::target", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + ip, "vh_clearAccessLogs.php")
		if s == "0":
			return True
		else:
			return False

	def uploadSpyware(self, ip):
		ut = Utils()
		s = ut.requestString("user::::pass::::target", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + ip, "vh_spywareUpload.php")
		if s == "0":
			return True
		else:
			return False 

	def getTournament(self):
		ut = Utils()
		temp = ut.requestString("user::::pass::::uhash", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + "UserHash_not_needed", "vh_update.php")
		if "tournamentActive" in temp:
			if not "2" in temp.split('tournamentActive":"')[1].split('"')[0]:
				return True
			else:
				return False

	def getIP(self, blank):
		ut = Utils()
		info = self.myinfo()
		info = json.loads(info)
		uhash = info['uhash']
		temp = ut.requestString("user::::pass::::uhash::::global", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + str(uhash) + "::::" + "0", "vh_getImg.php")
		jsons = json.loads(temp)
		for i in range(0, len(jsons["data"])):
			hostname = str(jsons["data"][i]["hostname"])
			imgstring = 'data: image/png;base64,'+jsons["data"][i]['img']
			imgstring = imgstring.split('base64,')[-1].strip()
			pic = cStringIO.StringIO()
			image_string = cStringIO.StringIO(base64.b64decode(imgstring))
			image = Image.open(image_string)

			# Overlay on white background, see http://stackoverflow.com/a/7911663/1703216
			#bg = Image.new("RGB", image.size, (255,255,255))
			#bg.paste(image,image)
			if "Hatched by the FBI" in pytesseract.image_to_string(image) or "Watched by the FBI" in pytesseract.image_to_string(image):
				return 1, hostname
			else:
				temp = ut.requestString("user::::pass::::uhash::::hostname", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + str(uhash) + "::::" + hostname, "vh_scanHost.php")
				try:
					jsons = json.loads(temp)
					return 0, str(jsons['ipaddress'])
				except TypeError:
					return 0, 0
				#print str(jsons['ipaddress'])
		

	def attackIP(self, ip, max):
		ut = Utils()
		info = self.myinfo()
		info = json.loads(info)
		uhash = info['uhash']
		temp = ut.requestString("user::::pass::::uhash::::target", self.api.getUsername() + "::::" + self.api.getPassword() + "::::" + uhash + "::::" + ip, "vh_loadRemoteData.php")

		jsons = json.loads(temp)
		
		o = OCR() 
		imgs = o.getSolution(str(temp))
		if imgs != None:
			try:
				user = jsons['username']
				winchance = jsons['winchance']
			except TypeError:
				return False
			try:
				if not "?" in str(winchance):
					fwlevel = jsons['fw']
					avlevel = jsons['av']
					spamlevel = jsons['spam']
					sdklevel = jsons['sdk']
					ipsplevel = jsons['sdk']
					money = jsons['money']
					saving = jsons['savings']
					anonymous = jsons['anonymous']
					username = jsons['username']
					winlo = jsons['winelo']
					winchance = jsons['winchance']
					spywarelevel = jsons['spyware']
				else:
					avlevel = "????"
					winchance = 0
					print "no scan username"
					return False

			except TypeError:
				fwlevel = jsons['fw']
				avlevel = jsons['av']
				spamlevel = jsons['spam']
				sdklevel = jsons['sdk']
				ipsplevel = jsons['sdk']
				money = jsons['money']
				saving = jsons['savings']
				anonymous = jsons['anonymous']
				username = jsons['username']
				winlo = jsons['winelo']
				winchance = jsons['winchance']
				spywarelevel = jsons['spyware']

			if type(winchance) == "int":
				if "?" in winchance:
					winchance = 0
					print "no chance"
					return False

			if not "?" in str(avlevel):
				if int(avlevel) < max and int(winchance) > 75 and str(anonymous) == "YES":
					password = self.enterPassword(imgs, ip, uhash)
					jsons = json.loads(password)
					if password:
						try:
							if not "?" in str(money) and str(jsons['result']) == 0:
								print "\n[TargetIP: " + str(ip) +"]\n\nMade " + "{:11,}".format(int(jsons['amount'])) + " and " + "{:2d}".format(int(jsons['eloch'])) + " Rep." + "\n Antivirus: "+ str(avlevel) + " Firewall: " + str(fwlevel) + " Sdk: " + str(sdklevel) + " TotalMoney: " + "{:11,}".format(int(money)) + "\n YourWinChance: " + str(winchance) + " Anonymous: "+ str(anonymous) +" username: "+ str(username) + " saving: " + str(saving)
								return True
							else:
								print "\n[TargetIP: " + str(ip) + "]\n\nMade " + "{:11,}".format(int(jsons['amount'])) + " and " + "{:2d}".format(int(jsons['eloch'])) + " Rep." + "\n Antivirus: "+ str(avlevel) + " Firewall: " + str(fwlevel) + " Sdk: " + str(sdklevel) + " TotalMoney: " + "{:11,}".format(int(money)) + "\n YourWinChance: " + str(winchance) + " Anonymous: " + str(anonymous) +" username: "+ str(username) + " saving: " + str(saving)
						except KeyError:
							print "Bad attack"
							return False
					else:
						print "Password Wrong"
						return False
				else:
					#print "\n"
					if int(avlevel) > max:
						print "Antivir to high " + str(avlevel)
						#print "passed"
						return False
					if int(winchance) < 75:
						print "winchance is poor: " + str(winchance)
						#print "passed"
						return False
					if str(anonymous) == "NO":
						print "No Anonymous need"
						#print "passed"
						return False
			else:
				print avlevel
				if len(avlevel) == 4:
					print avlevel
					print "Cant load User"
					return False
				else:
					print "Scan to low"
					return False
		else:
			print "Password Error"
			return False

	def attackIP2(self,ip,max):	
		ut = Utils()
		o = OCR(False)
		imgs = self.requestPassword(ip)
		selection = o.getPassword(imgs)
		print selection

	def attack(self, amount, max, wait):
		i1 = 0
		while i1 < amount:
			FBI, ips = self.getIP(True)
			if FBI == 0:
				if self.attackIP(ips,max):
					i1 += 1
					print "Waiting..."
					time.sleep(wait)
			else:
				print "Warning FBI Blocking account in " + str(ips) + " I'm not attack"

	def __init__(self,api):
		self.api = api
