
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
import json, re

#print(t) //test
#print(r) //test
#print(t[r]) //test

#Basic Settings on date
datetime.today()
real_year=datetime.today().year
real_month=datetime.today().month
real_day=datetime.today().day
t = ['월', '화', '수', '목', '금', '토', '일']
imsi = "http://www.puhung.hs.kr/wah/main/schoolmeal/view.htm?menuCode=80&moveType=&domain.year="+str(real_year)+"&domain.month="+str(real_month)+"&domain.day="+str(real_day)
html = urlopen(imsi)
soup = BeautifulSoup(html.read(), "html.parser")
test = soup.find(class_="Schoolmeal_Cont_Cont_Cont")
test = test.get_text()
test = re.sub(" ?\d ?[.]*"," ",test)
test = re.sub(" +","\n",test)
print(real_year)
print(real_month)
print(real_day)
print("imsi:"+imsi)
print(datetime.today().weekday()-1)
print("t[r]:"+t[datetime.today().weekday()-1])
print("t[r]:"+t[datetime.today().weekday()+1])
print("t[r]:"+t[datetime.today().weekday()+2])
print("t[r]:"+t[datetime.today().weekday()+3])
print("t[r]:"+t[datetime.today().weekday()+4])

def get_m(r) :
	if r == 5 or r == 6 :
		m = 0
	else :
		m = 1
	return m

def get_menu(day) :
	imsi = "http://www.puhung.hs.kr/wah/main/schoolmeal/view.htm?menuCode=80&moveType=&domain.year="+str(real_year)+"&domain.month="+str(real_month)+"&domain.day="+str(day)
	html = urlopen(imsi)
	soup = BeautifulSoup(html.read(), "html.parser")
	test = soup.find(class_="Schoolmeal_Cont_Cont_Cont")
	test = test.get_text()
	test = re.sub(" ?\d ?[.]*"," ",test)
	test = re.sub(" +","\n",test)
	return test

def keyboard(request) :
	return JsonResponse({
            'type' : 'buttons',
            'buttons' : ['어제','오늘','내일']
            })

@csrf_exempt
def answer(request) :
	message = ((request.body).decode('utf-8'))
	return_json_str = json.loads(message)
	return_str = return_json_str['content']

	r = datetime.today().weekday()
	if return_str == '어제' :
		day = real_day - 1
		if r == 0 :
			r = 6
		else :
			r = r - 1
	elif return_str == '오늘' :
		day = real_day
	elif return_str == '내일' :
		day = real_day + 1
		if r == 6 :
			r = 0
		else :
			r = r + 1

	m=get_m(r)
	if m :
	    imsi_text = t[r] + '요일의 메뉴는?!! \n\n\n ' + get_menu(day) 
	else :
	    imsi_text = t[r] + '요일은 급식이 제공되지 않습니다.'

	return JsonResponse({
	    'message' : {
	    	'text' : imsi_text
	    },
	    'keyboard' : {
	        'type': 'buttons',
            'buttons' : ['어제','오늘','내일']
	        }
	    })
