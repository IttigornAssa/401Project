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
		t = 5
		while (t > 0):
			time.sleep(1)
			print(str(t))
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
		print("complete commit")
		conn.commit()

		# connection API Trello
		url = 'https://api.trello.com/1/board/uXomENXS/actions?key=86dea335c1203f4164c12d4a22905cf7&token=6ddeefb4235c59a2ebe43f64048774d61c55684b98c72b78bd4c6415cff05c94'
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
				r3 = str(use_idtimeStamp)
				demoDatabases2.execute("INSERT INTO myapp_cardRecord  (\"idCard\", \"actionCard\",\"timestamp_id\")VALUES ('{}', '{}', '{}')".format(r1,r2,r3))
				conn2.commit()
			except KeyError as e:
				pass
			finally:
				pass
	changeQ = []
	demoDatabases3.execute("SELECT DISTINCT \"idCard\" FROM public.myapp_cardrecord  where \"timestamp_id\" ="+str(5)+";")
		# demoDatabases3.execute("SELECT \"idCard\" , \"actionCard\" , \"timestamp_id\"  , \"dates\" FROM public.myapp_timestamp inner join public.myapp_cardrecord on public.myapp_cardrecord.timestamp_id =  public.myapp_timestamp.id where public.myapp_timestamp.id ="+ str(x) +";")
	for row in demoDatabases3 :
		# print(row,row[0])
		postgreSQL_select_Query1 = "select \"idCard\", \"actionCard\" ,\"timestamp_id\" from public.myapp_cardrecord  where \"idCard\" = "+ "'"+row[0]+ "' and \"timestamp_id\" ="+str(6)+";"
		table1.execute(postgreSQL_select_Query1)
		idCardCheck = table1.fetchall()
		for x  in idCardCheck :
			print(x[0],x[2])
	

	conn.close()
	conn2.close()
	conn3.close()
	return render(request,'home.html')

	# listState
	# comment

	