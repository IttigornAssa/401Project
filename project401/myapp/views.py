from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from requests import get
from psycopg2 import connect
from django.shortcuts import render, redirect
from trello import TrelloClient
import requests 
import json
from django.http import JsonResponse
from array import *
from json.decoder import JSONDecodeError
import sys
from datetime import date
from datetime import datetime
# from django.utils import timezone

def demoDatabases(request):
	
	
	# connection database timeStamp
	conn = connect("dbname='trello_test' user='postgres' host='localhost' password='1234'")
	demoDatabases = conn.cursor()
	# connect  database CardRecord
	conn2 = connect("dbname='trello_test' user='postgres' host='localhost' password='1234'")
	demoDatabases2 = conn2.cursor()
	conn3 = connect("dbname='trello_test' user='postgres' host='localhost' password='1234'")
	demoDatabases3 = conn3.cursor()
	
	# connect to compare table 1
	conntable1 = connect("dbname='trello_test' user='postgres' host='localhost' password='1234'")
	table1 = conntable1.cursor()
	# connect to compare table 2
	conntable2 = connect("dbname='trello_test' user='postgres' host='localhost' password='1234'")
	table2 = conntable2.cursor()
	# auto input(insert)
	for n in range(2) :
		# COUNTDOWN
		import time
		t = 5
		while (t > 0):
			time.sleep(1)
			print("count down :"+str(t))
			t = t-1
		# date - time
		from datetime import time
		datetimes = datetime.now()
		todayzone = datetimes.strftime("%x")
		formatedDate = datetimes.strftime("%Y-%m-%d %H:%M:%S")
		# timezone = datetimes.strftime("%H:%M")
		# timezone = timezone.now()
		# Insert to database


		demoDatabases.execute("INSERT INTO myapp_timeStamp  (\"datetime\"  )VALUES ('{}')".format(formatedDate))
		conn.commit()

		# connection API Trello
		url = 'https://api.trello.com/1/board/LXSisJxP/actions?key=86dea335c1203f4164c12d4a22905cf7&token=6ddeefb4235c59a2ebe43f64048774d61c55684b98c72b78bd4c6415cff05c94'
		apiTrello = requests.get(url)
		data_json = apiTrello.json()

		# select id timeStamp
		postgreSQL_select_Query_timeStamp = "select \"id\"  from myapp_timeStamp "
		demoDatabases.execute(postgreSQL_select_Query_timeStamp)
		idtimeStamp = demoDatabases.fetchall()
		use_idtimeStamp = ''
		for row in idtimeStamp :
			use_idtimeStamp = row[0]
		# idLength 
		idLength = int(use_idtimeStamp) + 1
		# getJson + addData to cardRecord
		for historycard in data_json :
			try:
			# insert to database
				r1 = str(historycard['data']['card']['id'])
				r2 = str(historycard['type'])
				r3 = ''
		
				try:
					r3 = str(historycard['data']['card']['desc'])
				except KeyError as e:
					r3 = "N/A"
				finally:
					pass
				r4 = ''

				try:
					r4 = str(historycard['data']['text'])
				except KeyError as e:
					r4 = "N/A"
				finally:
					pass
				r5 = str(use_idtimeStamp)
				demoDatabases2.execute("INSERT INTO myapp_cardRecord  (\"idCard\", \"actionCard\", \"descCard\", \"commentCard\" ,\"timestamp_id\")VALUES ('{}', '{}', '{}', '{}', '{}')".format(r1,r2,r3,r4,r5))
				conn2.commit()
			except KeyError as e:
				pass
			finally:
				pass
	changeQ = []
	# current ID
	loopRetroact = idLength - 1
	loopRetroact2 = idLength - 2
	fixloop = loopRetroact 
	# Req Change count

	# demoDatabases3.execute("SELECT \"idCard\" , \"actionCard\" , \"timestamp_id\"  , \"dates\" FROM public.myapp_timestamp inner join public.myapp_cardrecord on public.myapp_cardrecord.timestamp_id =  public.myapp_timestamp.id where public.myapp_timestamp.id ="+ str(x) +";")
	for i in range(fixloop):
		if loopRetroact != 1 :
			countlastHistory = 0
			countlastertHistory = 0
			demoDatabases3.execute("SELECT DISTINCT \"idCard\" FROM public.myapp_cardrecord")		
			for row in demoDatabases3 :
				chklastHistory = 0
				chklastertHistory= 0
				postgreSQL_select_Query1 = "select \"idCard\", \"actionCard\" ,\"timestamp_id\" ,\"descCard\"  from public.myapp_cardrecord  where \"idCard\" = "+ "'"+row[0]+ "' and \"timestamp_id\" ="+str(loopRetroact)+";"
				table1.execute(postgreSQL_select_Query1)
				idCardCheck = table1.fetchall()
				for lastHistory  in idCardCheck :
					if lastHistory[1] == 'updateCard' :
						if lastHistory[3] == 'N/A':
							countlastHistory = countlastHistory+1
						else :
							chklastHistory = chklastHistory+1
							if chklastHistory > 1 :
								countlastHistory = countlastHistory+1
					elif lastHistory[1] == 'commentCard' :				
						countlastHistory = countlastHistory	
					elif lastHistory[1] == 'createCard' :
						countlastHistory = countlastHistory	+1 
					else :
						countlastHistory = countlastHistory+1

				postgreSQL_select_Query2 = "select \"idCard\", \"actionCard\" ,\"timestamp_id\" ,\"descCard\" from public.myapp_cardrecord  where \"idCard\" = "+ "'"+row[0]+ "' and \"timestamp_id\" ="+str(loopRetroact2)+";"
				table2.execute(postgreSQL_select_Query2)
				idCardCheck2 = table2.fetchall()
				for lastertHistory  in idCardCheck2 :
					if lastertHistory[1] == 'updateCard' :
						if lastertHistory[3] == 'N/A':
							countlastertHistory = countlastertHistory+1
						else :
							chklastertHistory = chklastertHistory+1
							if chklastertHistory > 1 :
								countlastertHistory = countlastertHistory+1
					elif lastertHistory[1] == 'commentCard' :
						countlastertHistory = countlastertHistory	
					elif lastertHistory[1] == 'createCard' :
						countlastertHistory = countlastertHistory	+1 
					else :
						countlastertHistory = countlastertHistory+1

		
			loopRetroact = loopRetroact -1
			loopRetroact2 = loopRetroact2 -1
			print(str(countlastHistory-countlastertHistory))

	conn.close()
	conn2.close()
	conn3.close()
	return render(request,'home.html')

	# listState
	# comment

	