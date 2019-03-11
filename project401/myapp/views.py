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
	for n in range(1) :
		# COUNTDOWN
		import time
		t = 1
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


		# demoDatabases.execute("INSERT INTO myapp_timeStamp  (\"datetime\"  )VALUES ('{}')".format(formatedDate))
		# conn.commit()

		# connection API Trello
		url = 'https://api.trello.com/1/board/dZbJ6bKF/actions?key=86dea335c1203f4164c12d4a22905cf7&token=6ddeefb4235c59a2ebe43f64048774d61c55684b98c72b78bd4c6415cff05c94'
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

				r5 = ''
				try:
					r5 = str(historycard['data']['listAfter']['name'])
				except KeyError as e:
					r5 = "N/A"
				finally:
					pass

				r6 = str(use_idtimeStamp)
				# 42 tsmp
				# demoDatabases2.execute("INSERT INTO myapp_cardRecord  (\"idCard\", \"actionCard\", \"descCard\", \"commentCard\", \"listafterCard\" ,\"timestamp_id\")VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(r1,r2,r3,r4,r5,r6))
				# conn2.commit()
			except KeyError as e:
				pass
			finally:
				pass
	changeQ = []
	# table1-ID
	loopRetroact = idLength - 1

	# table2-ID
	loopRetroact2 = idLength - 2

	# loop for calculate
	fixloop = loopRetroact 

	# fix 1 count 
	

	# demoDatabases3.execute("SELECT \"idCard\" , \"actionCard\" , \"timestamp_id\"  , \"dates\" FROM public.myapp_timestamp inner join public.myapp_cardrecord on public.myapp_cardrecord.timestamp_id =  public.myapp_timestamp.id where public.myapp_timestamp.id ="+ str(x) +";")
	for i in range(fixloop):
		if loopRetroact != 1 :
			fix = 1
			# count to calculate
			countlastHistory = 0
			countlastertHistory = 0

			# check Delete / MoveCard
			deleteHistory = 0
			deleteLaster = 0
			beforeDelete = 0


			# seleact all card DISTINCT
			demoDatabases3.execute("SELECT DISTINCT \"idCard\" FROM public.myapp_cardrecord")		
			for row in demoDatabases3 :
				chklastHistory = 0
				chklastertHistory= 0
				postgreSQL_select_Query1 = "select \"idCard\", \"actionCard\" ,\"timestamp_id\" ,\"descCard\" , \"listafterCard\" from public.myapp_cardrecord  where \"idCard\" = "+ "'"+row[0]+ "' and \"timestamp_id\" ="+str(loopRetroact)+";"
				table1.execute(postgreSQL_select_Query1)
				idCardCheck = table1.fetchall()
				for lastHistory  in idCardCheck :
					if lastHistory[1] == 'deleteCard' :
						deleteHistory = 1 
					elif lastHistory[1] == 'updateCard' :
						if lastHistory[3] == 'N/A':
							if lastHistory[4] == 'N/A':
								pass
							else :
								countlastHistory = countlastHistory	+1 
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

				postgreSQL_select_Query2 = "select \"idCard\", \"actionCard\" ,\"timestamp_id\" ,\"descCard\" ,\"listafterCard\" from public.myapp_cardrecord  where \"idCard\" = "+ "'"+row[0]+ "' and \"timestamp_id\" ="+str(loopRetroact2)+";"
				table2.execute(postgreSQL_select_Query2)
				idCardCheck2 = table2.fetchall()
				for lastertHistory  in idCardCheck2 :
					if lastertHistory[1] == 'deleteCard' :
						deleteLaster = 1
					elif lastertHistory[1] == 'updateCard' :
						if lastertHistory[3] == 'N/A':
							if lastertHistory[4] == 'N/A':
								pass
							else :
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
				if fix == 1 :
					if deleteHistory == 1 :
						if deleteLaster != 1 :
							beforeDelete = countlastertHistory + 1 
							countlastHistory =countlastHistory + beforeDelete
							fix = 0

	


# 1
# 4
# 2
# 0
# 1
# 4
# 7


# 4
#-5	7-8
# 4	6-7
# 2	5-6
# 0	4-5	
# 1	3-4
# 4	2-3
# 7 1-2
		
			loopRetroact = loopRetroact -1
			loopRetroact2 = loopRetroact2 -1
			# print(str(countlastHistory))
			# print(str(countlastertHistory))
			print(str(countlastHistory-countlastertHistory))

	conn.close()
	conn2.close()
	conn3.close()
	return render(request,'home.html')

	# listState
	# comment

	