
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
import json, re

#Basic Settings on date

datetime.today()
real_year=datetime.today().year
real_month=datetime.today().month
real_day=datetime.today().day
t = ['월', '화', '수', '목', '금', '토', '일']

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
	print("test : "+test)
	test = re.sub(" ?\d ?[.]*"," ",test)
	print("test : "+test)
	test = re.sub(" +","\n",test)
	test = re.sub("a-zA-Z"," ",test)
	print("test : "+test)
	return test

def keyboard(request) :
	return JsonResponse({
            'type' : 'buttons',
            'buttons' : ['급식알림','코드실행기','챗봇']
            })

@csrf_exempt
def answer(request) :
	message = ((request.body).decode('utf-8'))
	return_json_str = json.loads(message)
	return_str = return_json_str['content']
	print("test, is this error?")

	if return_str == '급식알림' :
		return JsonResponse({
		    'keyboard' : {
		        'type': 'buttons',
	            'buttons' : ['오늘','내일','뒤로가기']
		    }
	    })
	elif return_str == '코드실행기' :
		return JsonResponse({
		    'message' : {
		    	'text' : '사용 가능한 명령어의 리스트를 보고 싶으시면 --list를 입력하세요. 도움말을 보고 싶으시면 --help를 입력하세요. 홈으로 돌아가고 싶으시면 --home을 입력하세요.'
		    }
	    })
	elif return_str == '챗봇' :
		return JsonResponse({
		    'message' : {
		    	'text' : '아직 지원하지 않는 기능입니다. 다음 업데이트를 기다려 주세요!'
			},
			'keyboard' : {
				'type' : 'buttons',
				'buttons' : ['뒤로가기']
			}
		})


	r = datetime.today().weekday()
	if return_str == '오늘' :
		day = real_day
	elif return_str == '내일' :
		day = real_day + 1
		if r == 6 :
			r = 0
		else :
			r = r + 1
	elif return_str == '뒤로가기' || return_str == '--home' :
		return JsonResponse({
			'keyboard' : {
				'type' : 'buttons',
				'buttons' : ['급식알림','코드실행기','챗봇']
			}
		})
	'''
	test1=get_menu(day)
	print("today real_day : " + str(real_year) +"/"+str(real_month)+"/"+str(real_day))
	print("today day : " + str(real_year) +"/"+str(real_month)+"/"+str(day))
	imsi = "http://www.puhung.hs.kr/wah/main/schoolmeal/view.htm?menuCode=80&moveType=&domain.year="+str(real_year)+"&domain.month="+str(real_month)+"&domain.day="+str(day)
	print("imsi : "+imsi)
	'''
	m=get_m(r)
	if m :
	    imsi_text = t[r] + '요일의 메뉴는?!! \n\n\n ' + get_menu(day)
	else :
	    imsi_text = t[r] + '요일은 급식이 제공되지 않습니다.'

	print("No error!")
	return JsonResponse({
	    'message' : {
	    	'text' : imsi_text
	    },
	    'keyboard' : {
	        'type': 'buttons',
            'buttons' : ['오늘','내일','뒤로가기']
	        }
	    })
