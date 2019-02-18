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
def showBoard(request):

# board
	url = 'https://api.trello.com/1/boards/WcwnHFhZ/?key=86dea335c1203f4164c12d4a22905cf7&token=6ddeefb4235c59a2ebe43f64048774d61c55684b98c72b78bd4c6415cff05c94'
	r  = requests.get(url)
	last_board =  r.json()
	print("BOARD-ID")
	print(last_board['id'])
	print(last_board['name'] + "\n")
	print("_________________________________________")

# card
	url2 = 'https://api.trello.com/1/boards/WcwnHFhZ/cards?key=86dea335c1203f4164c12d4a22905cf7&token=6ddeefb4235c59a2ebe43f64048774d61c55684b98c72b78bd4c6415cff05c94'
	r2 = requests.get(url2)
	card = r2.json()
	i=0
	idArray = []
	idCheckList = []
	print("CARD-ID")
	for cardid in card :
		# idCard
		print("ID: " + cardid['id'])
		# idBoard
		print("ID-Board: " + cardid['idBoard'])
		# listid
		print("ID-List: " + cardid['idList'] )
		# idChecklists 
		print("ID-Checklists: " + str(cardid['idChecklists']).replace("'","").replace("[","").replace("]","") )
		idArray.insert(i,str(cardid['id']))
		idCheckList.insert(i,str(cardid['idChecklists']).replace("'","").replace("[","").replace("]",""))
		print(idArray[i] +" has ---> "+ idCheckList[i] +"\n")
		idTest = ''
		if len(cardid['idChecklists']) > 1 :
			alphabet = idCheckList[i]
			data = alphabet.split() #split string into a list
			for listid in data :
   				print(str(listid).replace(",",""))
   				idTest = str(listid).replace(",","") 
		

		# URL check complete / incomplete by CheckList
		if str(idCheckList[i]) == '':
			# assingn value
			pass
		else:
			if idTest != '' :
				urlChk = 'https://api.trello.com/1/checklists/'+idTest+'?key=86dea335c1203f4164c12d4a22905cf7&token=6ddeefb4235c59a2ebe43f64048774d61c55684b98c72b78bd4c6415cff05c94'	
			else:
				urlChk = 'https://api.trello.com/1/checklists/'+idCheckList[i]+'?key=86dea335c1203f4164c12d4a22905cf7&token=6ddeefb4235c59a2ebe43f64048774d61c55684b98c72b78bd4c6415cff05c94'
			
			rChk = requests.get(urlChk)
			chk = rChk.json()
			completes = 0
			for j in range(len(chk['checkItems'])) :
				if chk['checkItems'][j]['state'] == "complete":
					completes = completes+1
			print(chk['checkItems'][j]['state'])
			urlnameCard = 'https://api.trello.com/1/card/'+str(chk['idCard'])+'?key=86dea335c1203f4164c12d4a22905cf7&token=6ddeefb4235c59a2ebe43f64048774d61c55684b98c72b78bd4c6415cff05c94'
			rnameCard = requests.get(urlnameCard)
			nameCard = rnameCard.json()
			percent = (completes*100)/len(chk['checkItems'])
			print("Name Card: "+str(nameCard['name'])+" is Finish [[[ "+ str(percent) +" % ]]]")

		i = i+1
	print("*********** HAS CARD "+str(i)+" ***********")
	print("_________________________________________")
	

# listID
	url3 = 'https://api.trello.com/1/boards/WcwnHFhZ/lists/?key=86dea335c1203f4164c12d4a22905cf7&token=6ddeefb4235c59a2ebe43f64048774d61c55684b98c72b78bd4c6415cff05c94'
	r3 = requests.get(url3)
	lists = r3.json()
	#keep state
	keepState = []
	#keep amount of state
	amount = 0
	count = 0
	print("LIST-ID")
	for listid in lists :
		# idList 
		print("ID: " + listid['id'])
		# name (State)
		print("STATE: " + listid['name'])
		keepState.insert(count,[str(listid['name']),amount])
		# idBoard
		print("ID-Board: " + listid['idBoard'] +"\n")
		print("_________________________________________"+ str(keepState) + "\n")
		count = count+1

#listID && Card id --> show amount's card for state
	CardOfList = ''
	# l=0 
	for k in range(len(card)) :
		urlCardOfList = 'https://api.trello.com/1/cards/'+str(card[k]['id'])+'/list?key=86dea335c1203f4164c12d4a22905cf7&token=6ddeefb4235c59a2ebe43f64048774d61c55684b98c72b78bd4c6415cff05c94'
		rCardOfList = requests.get(urlCardOfList)
		CardOfList = rCardOfList.json()
		# print(CardOfList['name'])
		# print(len(keepState))
		# print(str(CardOfList['name']) +" "+ str(keepState[0][0]))
		l=0
		while l < count:
			# print(m[l][0]  +"--->"+ str(CardOfList['name']))
			if str(CardOfList['name']) == str(keepState[l][0]):
				keepState[l][1] = keepState[l][1] + 1
			l =l + 1
	print(str(keepState) +"\n\n")




# ACTION
	url4 = 'https://api.trello.com/1/boards/WcwnHFhZ/actions?key=86dea335c1203f4164c12d4a22905cf7&token=6ddeefb4235c59a2ebe43f64048774d61c55684b98c72b78bd4c6415cff05c94'
	r4 = requests.get(url4)
	action = r4.json()
	print("ACTION-ID")
	for actions in action :
		# idAction
		print("ID: " + actions['id'])
		# idBoard
		print("ID-Board: " + actions['data']['board']['name'] )
		try:
			print("LIST : "+actions['data']['list']['name'])
		except KeyError as e:
			pass
		finally:
			pass

		try:
			print("After : "+ actions['data']['listAfter']['name'])
		except KeyError as e:
			pass
		finally:
			pass

		try:
			print("Before : "+actions['data']['listBefore']['name'])
		except KeyError as e:
			pass
		finally:
			pass
		print("\n")
		



	return render(request,'home.html')
	




def showTest(request):
	# date
	import time
	# today = date.today()
	datetimes = datetime.now()
	today = datetimes.strftime("%x")
	times = datetimes.strftime("%X")
	times2 = datetimes.strftime("%H:%M")
	# tomonth = date.tomonth()
	# toyear = date.toyear()
	#url board trello
	url = 'https://api.trello.com/1/board/dri2ZNet/actions?key=86dea335c1203f4164c12d4a22905cf7&token=6ddeefb4235c59a2ebe43f64048774d61c55684b98c72b78bd4c6415cff05c94'
	r = requests.get(url)
	action = r.json()
	idCard = []
	reQChange = []
	amount = 0 
	conn = connect("dbname='trello_test' user='postgres' host='localhost' password='1234'")
	c = conn.cursor()

	for showAction in action :
	# print(str(action[0]['data']['card']['id'])+" " +str(action[0]['type']))
		
		try:
			
			idCard.insert(amount,str(showAction['data']['card']['id']))
			reQChange.insert(amount,str(showAction['type']))
			# print(str(showAction['data']['card']['id'])+" " +str(showAction['type']))
			print(str(amount)+" "+idCard[amount] +" "+reQChange[amount])
			# insert to database
			c.execute("INSERT INTO myapp_currentcard  (\"idCard\", \"typeCard\", \"date\",\"currenttime\")VALUES ('{}', '{}', '{}', '{}')".format(idCard[amount] , reQChange[amount],today,times2))
			c.execute("INSERT INTO myapp_historycard  (\"idCard\", \"typeCard\", compare, \"date\",\"currenttime\")VALUES ('{}', '{}', '{}', '{}', '{}')".format(idCard[amount] , reQChange[amount],"before",today,times2))
			conn.commit()
			amount = amount + 1 

		except KeyError as e:
			pass
		finally:
			pass

	count = 0
	# COUNTDOWN
	import time
	t = 22
	while (t > 0):
		time.sleep(1)
		print(str(t))
		t = t-1
	# print(str(t))
	from datetime import time
	if t == 0 :
		url = 'https://api.trello.com/1/board/dri2ZNet/actions?key=86dea335c1203f4164c12d4a22905cf7&token=6ddeefb4235c59a2ebe43f64048774d61c55684b98c72b78bd4c6415cff05c94'
		r = requests.get(url)
		action = r.json()
		idCard = []
		reQChange = []
		amount = 0 
		conn = connect("dbname='trello_test' user='postgres' host='localhost' password='1234'")
		conn2 = connect("dbname='trello_test' user='postgres' host='localhost' password='1234'")
		c = conn.cursor()
		c2 = conn2.cursor()
		#delete -> update 
		c.execute("DELETE FROM myapp_currentcard where  id != 0 ")
		for showAction in action :
		# insert to database
			
			try:
				idCard.insert(amount,str(showAction['data']['card']['id']))
				reQChange.insert(amount,str(showAction['type']))
			# insert
				c.execute("INSERT INTO myapp_currentcard  (\"idCard\", \"typeCard\",\"date\",\"currenttime\")VALUES ('{}', '{}', '{}', '{}')".format(idCard[amount] , reQChange[amount],today,times2))
			#increase insert 
				c.execute("INSERT INTO myapp_historycard  (\"idCard\", \"typeCard\", \"compare\",\"date\",\"currenttime\")VALUES ('{}', '{}', '{}', '{}', '{}')".format(idCard[amount] , reQChange[amount],"after",today,times2))
				conn.commit()
				amount = amount + 1 
			except KeyError as e:
				pass
			finally:
				pass

		#all id Card
		amountCard = 0
		#sum Change
		sumChange = 0
		# Change req
		countAfter = 0
		countBefore = 0
	try:
		# postgreSQL_select_Query = "select * from myapp_historycard"
		postgreSQL_select_Query = "select DISTINCT \"idCard\" from myapp_historycard"
		c.execute(postgreSQL_select_Query)
		historycard = c.fetchall() 
		print("Print each row and it's columns values")
		for row in historycard :
			amountCard  = amountCard +1
			print("ID = ", row[0])
			# print("TYPE = ", row[2])
			# print("C-P  = ", row[3], "\n") 
			# postgreSQL_select_Query2 = "select \"idCard\", \"typeCard\" ,\"compare\" from myapp_historycard where \"idCard\" = "+ "'"+row[0]+ "'"  +  "and \"compare\" = 'after'" 
			postgreSQL_select_Query2 = "select \"idCard\", \"typeCard\" ,\"compare\" from myapp_historycard where \"idCard\" = "+ "'"+row[0]+ "'" 
			c2.execute(postgreSQL_select_Query2)
			compareAfter = c2.fetchall()
			print("Print Card ****************************")
			#chk update
			checkCount = 0
			chkUpdateAfter = 0
			chkUpdateBefore = 0
			for rowAfter in compareAfter :
				#chk AFTER
				if rowAfter[2] == 'after' :
					# print("ID = ", rowAfter[0])
					# print("TYPE = ", rowAfter[1])
					# print("C-P = ", rowAfter[2])
					if rowAfter[1] == 'updateCard' :
						chkUpdateAfter = chkUpdateAfter+1
						# print("YES 1","\n")
						if chkUpdateAfter > 2 :
							# print("YES UPDATE2 ***************","\n")
							countAfter = countAfter+1
							print(countAfter)
					else :
						# print("YES 3","\n")
						countAfter = countAfter+1
			
				#chk BEFORE 
				else :
					# print("ID = ", rowAfter[0])
					# print("TYPE = ", rowAfter[1])
					# print("C-P = ", rowAfter[2])
					if rowAfter[1] == 'updateCard' :
						# print("YES 4","\n")
						chkUpdateBefore = chkUpdateBefore+1
						if chkUpdateBefore > 2 :
							# print("YES 5","\n")
							countBefore = countBefore+1 
					else :
						# print("YES 6","\n")
						countBefore = countBefore+1
				
				checkCount = checkCount+1	
		sumChange =   countAfter - countBefore
		# print("############"+str(sumChange) +"  "+str(countBefore) +"############")
		print("############ "+str(sumChange) +" ############")
	except (Exception, psycopg2.Error) as error :
			print("Error while fetching data from PostgreSQL", error)
	else:
		pass
	finally:
		pass


	conn.close()
	conn2.close()
	return render(request,'home.html')


def countdown(request):
	t = 10
	while (t > 0):
		time.sleep(1)
		print(str(t))
		t = t-1
	print(str(t))
	return render(request,'home.html')