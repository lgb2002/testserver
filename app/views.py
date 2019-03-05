
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlencode
from runcode.views import *
from runcode.models import *
from datetime import datetime
import json, re

#Output Message Array
default_message = ['급식알림','코드실행기','챗봇']
schoolmeal_message = ['오늘','내일','뒤로가기']
coderunner_message = ['']
chatbot_message = ['뒤로가기']

#Basic Settings on date
datetime.today()
real_year=datetime.today().year
real_month=datetime.today().month
real_day=datetime.today().day
t = ['월', '화', '수', '목', '금', '토', '일']
#date = [(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0),(12,0),(13,0),(14,0),(15,0),(16,0),(17,0),(18,0),(19,0),(20,0),(21,0),(22,0),(23,0),(24,0),(25,0),(26,0),(27,0),(28,0),(29,0),(30,0),(31)]
#print("test(time) :"+str(real_year)+'/'+str(real_month)+'/'+str(real_day))


#CodeRunner
Lang = [' ','C#', 'Visual Basic', 'F#', 'Java', 'Python', 'C (gcc)', 'C++ (gcc)', 'Php', 'Pascal', 'Objective-C', 'Haskell', 'Ruby', 'Perl', 'Lua', 'Assembly', 'Sql Server', 'Javascript', 'Common Lisp', 'Prolog', 'Go', 'Scala', 'Scheme', 'Node.js', 'Python 3', 'Octave', 'C (clang)', 'C++ (clang)', 'C++ (vc++)', 'C (vc)', 'D', 'R', 'Tcl', 'MySql', 'PstgreSQL', 'Oracle', 'Client Side', 'Swift', 'Bash', 'Ada', 'Erlang', 'Elixir', 'Ocaml', 'Kotlin', ' ', 'Fortran']
UsedLang = ['Assembly', 'Bash', 'C#', 'C++ ', 'C', 'Java', 'Javascript', 'Lua', 'MySql', 'Node.js', 'Oracle', 'Pascal', 'Php', 'Python', 'R', 'Ruby', 'Sql Server', 'Swift', 'Visual Basic']

num = "0"
language = ""

def get_m(r) :
	if r == 5 or r == 6 :
		m = 0
	else :
		m = 1
	return m


def get_menu(day) :
	'''
	imsi2 = "http://www.puhung.hs.kr/wah/main/schoolmeal/calendar.htm?menuCode=80"
	html2 = urlopen(imsi2)
	soup2 = BeautifulSoup(html2.read(,0), "html.parser")
	test2 = soup2.find(class_="Contents_schoolmeal_Date")
	test2 = test2.get_text()
	print("second test : "+test2)
	return "hello"
	'''
	
	try:
		#url = "http://www.puhung.hs.kr/wah/main/schoolmeal/calendar.htm?menuCode=80"
		#imsi = "http://www.puhung.hs.kr/wah/main/schoolmeal/view.htm?menuCode=80&moveType=&domain.year="+str(real_year)+"&domain.month="+str(real_month)+"&domain.day="+str(day)
		#date = "domain.year="+str(real_year)+"&domain.month="+str(real_month)+"&domain.day="+str(day)

		imsi = "https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%EB%B6%80%ED%9D%A5%EA%B3%A0+%EA%B8%89%EC%8B%9D"
		html = urlopen(imsi)
		soup = BeautifulSoup(html, "html.parser")
		test = soup.find_all('li', 'menu_info')
		print("before test[0]:"+test[0].get_text())

		#Date Data
		date_data = []
		for test0 in test:
			test0 = test0.get_text()
			date_data.append(test0[test0.find('월')+2:test0.find('일')])

		print("Day:"+str(day))
		text = ""
		for i in date_data:
			text += i

		print("date_data:"+text)

		if str(day) in date_data:
			index = date_data.index(str(day))
		else:
			test = "급식을 제공하지 않는 날입니다."
			return test

		#Menu Data
		print("index:"+str(index))
		print("after test[0]:"+test[0])
		menu = test[index]
		print("menu:"+menu)
		menu = re.sub(" ?\d ?[.]*"," ",menu)
		menu = re.sub(" +","\n",menu)
		menu = re.sub("a-zA-Z"," ",menu)
		menu = menu[5:len(menu)]

		#test = "I will start the service tomorrow. Sorry;"
		return menu
	except urllib.error.HTTPError:
		test = "식단을 찾다가 길을 잃었습니다. 한 번만 다시 급식을 확인해보세요."
		return test
	else:
		test = "알 수 없는 원인으로 에러괴물이 발생했습니다. 대피하세요!"
		return test


def keyboard(request) :
	return JsonResponse({
        'type' : 'buttons',
        'buttons' : default_message
    })


@csrf_exempt
def answer(request) :
	global num
	global language
	message = ((request.body).decode('utf-8'))
	return_json_str = json.loads(message)
	return_str = return_json_str['content']
	user_key = return_json_str['user_key']
	message_type = return_json_str['type']

	if return_str == '--exit' :
		print("escape from coderunner")
		return JsonResponse({
			'message' : {
		    	'text' : '중지했습니다.'
		    },
		    'keyboard' : {
			    'type': 'buttons',
		        'buttons' : default_message
	    	}
	    })
	elif return_str == default_message[0] :
		return JsonResponse({
			'message' : {
		    	'text' : '어느 요일의 급식이 궁금하세요?'
		    },
		    'keyboard' : {
			    'type': 'buttons',
		        'buttons' : schoolmeal_message
	    	}
	    })
	elif return_str == default_message[1] :
		return JsonResponse({
		    'message' : {
		    	'text' : '--exit를 입력하면 언제든지 코드실행기를 중지시킬 수 있습니다.  사용 가능한 명령어의 리스트를 보고 싶으시면 --list를 입력하세요. 도움말을 보고 싶으시면 --help를 입력하세요. 홈으로 돌아가고 싶으시면 --home을 입력하세요. code 실행을 원하시면 --lang을 입력하세요.'
		    }
	    })
	elif return_str == default_message[2] :
		return JsonResponse({
		    'message' : {
		    	'text' : '아직 지원하지 않는 기능입니다. 다음 업데이트를 기다려 주세요!'
			},
			'keyboard' : {
				'type' : 'buttons',
				'buttons' : chatbot_message
			}
		})

	else :
		if return_str == '--home' or return_str == '뒤로가기' :
			return JsonResponse({
				'message' : {
				   	'text' : '안녕하세요! 부흥고 급식 알리미입니다. 무엇을 도와드릴까요?'
			    },
				'keyboard' : {
					'type' : 'buttons',
					'buttons' : default_message
				}
			})
		elif return_str in schoolmeal_message :
			r = datetime.today().weekday()
			if return_str == schoolmeal_message[0] :
				day = real_day
			elif return_str == schoolmeal_message[1] :
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
			        'buttons' : schoolmeal_message
				}
			})
		elif return_str == '--lang':
			return JsonResponse({
				'message' : {
				    'text' : '다음의 언어 중 사용하실 언어를 입력해주세요.',
				},
				'keyboard' : {
				    'type': 'buttons',
			        'buttons' : UsedLang
				} 
			})
		elif return_str in UsedLang :
			language = return_str
			num = Lang.index(return_str)
			#print("language_index : "+num)
			url = "http://kakao.pythonanywhere.com/assets/"+str(num)+"-"+language+".txt"
			#print("url : "+url)
			file = urlopen(url)
			text = file.read().decode("utf-8")
			print("text : "+text)
			return JsonResponse({
				'message' : {
				    'text' :  text + " 언어의 기본 형식입니다. 위 내용을 복사한 뒤 코드를 작성해 함께 전송하면 올바른 결과값이 출력됩니다. --why를 입력하시면 자세한 설명을 볼 수 있습니다."
				}
			})

		elif return_str == "--why":
			return JsonResponse({
				'message' : {
				    'text' : "주석과 시스템 관련 코드는 기본적으로 공식 약속입니다. 또한  hello world 는 모든 프로그래밍 언어의 전통입니다. 따라서 복사 붙여넣기를 하지 않고 코드만 전송하실 경우 error 가 발생합니다."
				}
			})

		else : #type(return_str) == str: #last elif
			code = return_str
			plus = 'LanguageChoiceWrapper='+str(num)+'&'+urllib.parse.urlencode({'Program' : code})
			print("plus: "+plus)
			message = '&EditorChoiceWrapper=1&LayoutChoiceWrapper=1&Input=&Privacy=&PrivacyUsers=&Title=&SavedOutput=&WholeError=&WholeWarning=&StatsToSave=&CodeGuid=&IsInEditMode=False&IsLive=False'
			message = plus+message
			print("after message : "+message)
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

			run = Run(
				run_user = user_key,
				run_language = language,
				code = code,
				run_date = datetime.now()
			)
			run.save()

			return JsonResponse({
				'message' : {
				    'text' : result
				}
			})
			'''
		else:
			return JsonResponse({
				'message' : {
				    'text' : '에러괴물이 나타났어요! 도망가요!'
				}
			})'''

#choice = "000"

'''
variable 'choice' is function of array

1 = '급식알림'
	1 = '오늘'
	2 = '내일'
	3 = '뒤로가기'
2 = '코드실행기'

3 = '챗봇'
	1 = '뒤로가기'

3th array value is not defined yet
'''