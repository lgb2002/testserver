
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
from runcode.views import *
import json, re

#Basic Settings on date

choice = 0
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
	global choice
	print("choice: "+str(choice))
	message = ((request.body).decode('utf-8'))
	return_json_str = json.loads(message)
	return_str = return_json_str['content']

	if return_str == '급식알림' :
		choice = 1
		return JsonResponse({
			'message' : {
		    	'text' : 'test1'
		    },
		    'keyboard' : {
			    'type': 'buttons',
		        'buttons' : ['오늘','내일','뒤로가기']
	    	}
	    })
	elif return_str == '코드실행기' :
		choice = 2
		return JsonResponse({
		    'message' : {
		    	'text' : '사용 가능한 명령어의 리스트를 보고 싶으시면 --list를 입력하세요. 도움말을 보고 싶으시면 --help를 입력하세요. 홈으로 돌아가고 싶으시면 --home을 입력하세요.'
		    }
	    })
	elif return_str == '챗봇' :
		choice = 3
		return JsonResponse({
		    'message' : {
		    	'text' : '아직 지원하지 않는 기능입니다. 다음 업데이트를 기다려 주세요!'
			},
			'keyboard' : {
				'type' : 'buttons',
				'buttons' : ['뒤로가기']
			}
		})
	
	else :
		if return_str == '--home' or return_str == '뒤로가기' :
			choice = 0
			return JsonResponse({
				'message' : {
				   	'text' : 'test2'
			    },
				'keyboard' : {
					'type' : 'buttons',
					'buttons' : ['급식알림','코드실행기','챗봇']
				}
			})
		elif choice == 1:
			r = datetime.today().weekday()
			if return_str == '오늘' :
				day = real_day
			elif return_str == '내일' :
				day = real_day + 1
				if r == 6 :
					r = 0
				else :
					r = r + 1
			print("return_str : "+return_str)
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
		elif choice == 2:
			message = return_str
			url = "http://kakao.pythonanywhere/runcode/run"
			headers = {'Host': 'kakao.pythonanywhere.com', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0', 'Origin': 'http://kakao.pythonanywhere.com',
'Upgrade-Insecure-Requests': '1', 'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'http://kakao.pythonanywhere.com/runcode/run', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
'Cookie': '_ga=GA1.2.1355811774.1532426694; csrftoken=gifaHd6LjiCpxsRAvP4EQwJLnRQNmxhLg6ehmTBJfYxs7HYhbBE57XVpS593aNnh; _gid=GA1.2.1446735685.1538794759'}
			res = requests.post(url, headers=headers , data=message)
			j = json.loads(res.text)
			jsonString = json.dumps(j, indent=4)
			dict = json.loads(jsonString)
			warnings = str(dict['Warnings'])
			errors = str(dict['Errors']) 
			result = str(dict['Result'])
			stats = str(dict['Stats'])
			print("result :"+result+" & stats :"+stats)

			return JsonResponse({
				'message' : {
				    'text' : result
				}
			})
 			

