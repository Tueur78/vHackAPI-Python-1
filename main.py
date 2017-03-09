#!/usr/bin/python2.7
#-*- coding: utf-8 

from classes import API
from classes import IP
from console import Console
from update import Update
from utils import Utils
from botnet import Botnet
from random import randrange, uniform
from collections import Counter 
import time
import json


# Enter username and password
api = API("username","password")
# Enter Max Antivir to attack in normal mode
maxanti_normal = 1500

# Enter Max Antivir to attack tournament
maxanti_tournament = 1900

# Enter Amount of Attacks normal
attacks_normal = 3

# Enter Amount of Attacks in tournament
attacks_tournament = 100

# Enter Updates (inet, hdd, cpu, ram, fw, av, sdk, ipsp, spam, scan, adw)
#updates = ["ipsp", "adw", "fw", "scan", "sdk", "av"]
updates = ["ipsp", "scan", "sdk", "av"]
#updates = ["ipsp",  "sdk"]
#Do you want to attack during tournament [True, False]
joinTournament = True
#Time to wait between each cycle in seconds
wait = round(uniform(0,1), 2)
wait_load = round(uniform(1,5), 2)

c = Console(api)
u = Update(api)
b = Botnet(api)
updatecount = 0
attackneeded = False

while True:
	attackneeded = False

	stat = "0"
	while "0" in stat:
		stat = u.startTask(updates[updatecount])
		if "0" in stat:
			print "updating " + updates[updatecount] + " level +1"
			#print "Started Update
			print "Waiting... in update"
			#u.useBooster()
			time.sleep(wait_load)
			updatecount += 1
			if updatecount == 14:
				while updatecount > 0:
					print(u.getTasks())
					#u.useBooster()

				if updatecount: 
					pass
					#u.finishAll()

			if updatecount >= len(updates):
				updatecount = 0

		elif "1" in stat:
			attackneeded = True

	if joinTournament:
		if c.getTournament():
			attackneeded = True

	if attackneeded == False:
		wait_load = round(uniform(1,5), 2)
		usebooster = u.getTasks()
		json_data = json.loads(usebooster)
		try:
			while len(json_data["data"]) > 1:
				if int(json_data["boost"]) > 5:
					u.useBooster()
					print "Use the booster in rest " + str(int(json_data["boost"])-1)
					# UPDATE Value
				else:
					print "you are < 5 boost."
					break
				usebooster = u.getTasks()
				json_data = json.loads(usebooster)
		except KeyError:
			pass

	if b.attackable():
		print "Attacking with Botnet"
		attackbot = b.attackall()
		print attackbot

	if attackneeded:
		c.attack(attacks_tournament, maxanti_tournament, wait)
		wait = round(uniform(0,1), 2)

	else:
		print "Waiting... in normal " + str(wait_load) + "s"
		attackneeded = True

		if attackneeded:
			c.attack(attacks_normal, maxanti_normal, wait_load)
			attackneeded = False
		wait_load = round(uniform(1,5), 2)
