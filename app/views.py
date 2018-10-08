
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
from urllib.request import urlopen
from runcode.views import *
from runcode.models import *
from datetime import datetime
import json, re

#Basic Settings on date


datetime.today()
real_year=datetime.today().year
real_month=datetime.today().month
real_day=datetime.today().day
t = ['월', '화', '수', '목', '금', '토', '일']

choice = 0

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
	user_key = return_json_str['user_key']

	if return_str == '급식알림' :
		choice = 1
		print("choice: "+str(choice))
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
		print("choice: "+str(choice))
		return JsonResponse({
		    'message' : {
		    	'text' : '사용 가능한 명령어의 리스트를 보고 싶으시면 --list를 입력하세요. 도움말을 보고 싶으시면 --help를 입력하세요. 홈으로 돌아가고 싶으시면 --home을 입력하세요.'
		    }
	    })
	elif return_str == '챗봇' :
		choice = 3
		print("choice: "+str(choice))
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
			print("choice: "+str(choice))
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
			#print("return_str : "+return_str)
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
		elif choice == 2 or choice == 0:
			message = return_str
			'''
			print("message : "+message)
			url = "http://kakao.pythonanywhere/runcode/run"
			headers = {'Content-Type': 'application/x-www-form-urlencoded'}
			res = requests.post(url, data=message)
			j = json.loads(res.text)
			jsonString = json.dumps(j, indent=4)
			dict = json.loads(jsonString)
			warnings = str(dict['Warnings'])
			errors = str(dict['Errors']) 
			result = str(dict['Result'])
			stats = str(dict['Stats'])
			print("result :"+result+" & stats :"+stats)
			'''
			url = "https://rextester.com/rundotnet/run"
			headers = {'Host': 'rextester.com', 'Connection': 'keep-alive', 'Accept': 'text/plain, */*; q=0.01' ,'Origin': 'https://rextester.com'
		, 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
		, 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Referer': 'https://rextester.com/rundotnet'
		, 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'}

			cookies = {'Cookie': '__utmz=178476455.1533087180.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmc=178476455; ASP.NET_SessionId=5ispjysxn0kh5iy4uz0afxpo; __utma=178476455.1346840277.1533087180.1538900674.1538902623.22; __utmt=1; .REXTESTER=F293D23BFD81DE732D7F7AC1911F57A5270931E19C1ADC0B140386B7C20D03AE14F4D0B527712DEC150CF216DABAA81F3F5421C68B3D396C88FB90A98D1499AEE474FD27A79E11E3A9A3207B65EAC80BB25D9F2377C169993AE7982129F6D1385A543B684CB300A08AC7626D754270B1D6FEE5472BE67486167C2E5F1D8FE0774FE31939DADA147043EE94501A7FC367; __utmb=178476455.12.10.1538902623'}
			res = requests.post(url, headers=headers , cookies=cookies, data=message)
			#print(res.status_code)
			#print(res.text)

			j = json.loads(res.text)
			#print("j:" +j)
			jsonString = json.dumps(j, indent=4)
			#print("jsonString:" +jsonString)

			dict = json.loads(jsonString)
			#print("dict:"+str(dict))
			warnings = str(dict['Warnings'])
			errors = str(dict['Errors']) 
			result = str(dict['Result'])
			stats = str(dict['Stats'])

			print("chatbot run code")
			'''register = UserInfo(
				run_user = user_key,
				run_language = register_pwd,
				user_name = register_name,
				created_date = datetime.now()
			)

			register.save()'''

			return JsonResponse({
				'message' : {
				    'text' : result
				}
			})
 			


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
from runcode.views import *
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
		choice = 1
		return JsonResponse({
			'message' : {
		    	'text' : 'test1',
		    	'choice' : '1'
		    },
		    'keyboard' : {
			    'type': 'buttons',
		        'buttons' : ['오늘','내일','뒤로가기']
	    	}
	    })
	elif return_str == '코드실행기' :
		return JsonResponse({
		    'message' : {
		    	'text' : '사용 가능한 명령어의 리스트를 보고 싶으시면 --list를 입력하세요. 도움말을 보고 싶으시면 --help를 입력하세요. 홈으로 돌아가고 싶으시면 --home을 입력하세요.',
		    	'choice' : '2'
		    }
	    })
	elif return_str == '챗봇' :
		return JsonResponse({
		    'message' : {
		    	'text' : '아직 지원하지 않는 기능입니다. 다음 업데이트를 기다려 주세요!',
		    	'choice' : '3'
			},
			'keyboard' : {
				'type' : 'buttons',
				'buttons' : ['뒤로가기']
			}
		})
	
	else :
		if return_str == '--home' or return_str == '뒤로가기' :
			return JsonResponse({
				'message' : {
				   	'text' : 'test2',
				   	'choice' : choice
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
		#elif choice == 2:
