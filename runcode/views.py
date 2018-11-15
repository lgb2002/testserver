from django.shortcuts import render
import requests, json, os, urllib
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from urllib.parse import urlencode
from django.utils import timezone
from runcode.models import *
from datetime import datetime
from ipware.ip import get_ip
from django.core.exceptions import MultipleObjectsReturned

def logout(request):
	ip = get_ip(request)
	login_user = UserLogin.objects.get(user_ip = ip)
	login_user.last_id = ""
	login_user.last_pwd = ""
	login_user.login_now = False
	return render(request, 'runcode/login.html', {})

def profile(request):
	return render(request, 'runcode/profile.html', {})

def login_check(request):
	ip = get_ip(request)
	
	login_user = UserLogin.objects.get(user_ip = ip)
	check = login_user.login_now
	if check :
		id = login_user.last_id
		user = UserInfo.objects.get(user_id = id)
		name = user.user_name
		data = UserData.objects.get(user_name = name)
		visit_lank = data.visit_lank
		return render(request, 'runcode/profile.html', {'name' : name, 'visit_lank' : str(visit_lank)})
	else :
		return render(request, 'runcode/login.html', {'check' : 0})
		
	return render(request, 'runcode/profile.html', {'name' : "error"})

def login_success(ip, name):
	login_user = UserLogin.objects.get(user_ip = ip)
	login_user.login_now = True
	login_user.login_date = datetime.now()
	user = UserInfo.objects.get(user_name = name)
	login_user.last_id = user.user_id
	login_user.last_pwd = user.user_pwd
	login_user.save()


def manual(request):
	return render(request, 'runcode/manual.html', {})

def services(request):
	return render(request, 'runcode/services.html', {})

def home(request):
	
	ip = get_ip(request)
	print(ip)

	try:
		login_user = UserLogin.objects.get(user_ip = ip)
	except UserLogin.MultipleObjectsReturned:
		print("hi")
		test = UserLogin.objects.filter(user_ip = ip).distinct('login_data')
		test.delete()
		login = UserLogin(
			user_ip = ip,
			login_now = False,
			login_date = datetime.now()
		)
		login.save()
	except UserLogin.DoesNotExist:
		login = UserLogin(
			user_ip = ip,
			login_now = False,
			login_date = datetime.now()
		)
		login.save()
		
	posts = Learning.objects.all().order_by('id')
	return render(request, 'runcode/home.html', {'posts':posts})

@csrf_exempt
def register(request):
	if request.method == "POST":
		
		register_id = request.POST.get('userid')
		register_pwd = request.POST.get('userpwd')
		register_name = request.POST.get('username')

		print("userid : "+register_id+" userpwd : "+register_pwd+" username : "+register_name)

		try:
			register_user = UserInfo.objects.get(user_name = register_name)
			try:
				register_user = UserInfo.objects.get(user_id = register_id)
				print("id exist")
				return render(request, 'runcode/register.html', {
					'result' : 'id exist'
				})
			except UserInfo.DoesNotExist:
				print("name exist")
				return render(request, 'runcode/register.html', {
					'result' : 'name exist'
				})
		except UserInfo.DoesNotExist:
			print("success")
			register = UserInfo(
				user_id = register_id,
				user_pwd = register_pwd,
				user_name = register_name,
				created_date = datetime.now()
			)
			register.save()

			data = UserData(
				user_name = register_name,
			    visit_lank = 0,
			    study_lank = "0_0_0_0_0_0_0",
			    coding_lank = "0_0_0_0_0_0_0"
			)
			data.save()

			return render(request, 'runcode/register.html', {
				'user_id' : register_id,
				'user_pwd' : register_pwd,
				'user_name' : register_name,
				'result' : 'success'
			})
	else:
		return render(request, 'runcode/register.html',{})




@csrf_exempt
def login(request):
	if request.method == "POST":
		
		get_id = request.POST.get('userid')
		get_pwd = request.POST.get('userpwd')

		try:
			imsi_user = UserInfo.objects.get(user_id = get_id, user_pwd = get_pwd)
			user_id = imsi_user.user_id
			user_pwd = imsi_user.user_pwd
			user_name = imsi_user.user_name
			data = UserData.objects.get(user_name = user_name)
			data.visit_lank += 1
			data.save()

			login = Login(
				login_id = user_id,
				login_pwd = user_pwd, 
				login_date = datetime.now(),
				login_error = "No Error"
				)
			login.save()
			ip = get_ip(request)
			login_success(ip, user_name)
			#login_check(request)
			return render(request, 'runcode/login.html', {'user_name': user_name, 'user_id' :user_id, 'user_pwd' : user_pwd, 'error' : 'No Error'})

		except UserInfo.DoesNotExist:
			alert(" Error! No Match UserInformation! ")
			login = Login(
				login_id = get_id,
				login_pwd = get_pwd, 
				login_date = datetime.now(),
				login_error = "No Match"
				)
			login.save()
			imsi_login = Login.objects.filter(login_id = get_id, login_pwd = get_pwd).order_by('login_date').last()
			error = imsi_login.login_error
			return render(request, 'runcode/login.html', {'user_id' : "No id", 'user_pwd' : "No pwd", 'error' : error})
	else:
		return render(request, 'runcode/login.html', {})







@csrf_exempt
def run(request):

	if request.method == "POST":
		message = str(request.body, encoding='utf-8')
	else : 
		return render(request, 'runcode/home.html', {
	    	'warnings' : "None",
	    	'errors' : "None",
	    	'result' : "None",
	    	'stats' : "None"
	    	})
	print("test message:" + message)

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
	warnings = str(dict['Warnings'])
	errors = str(dict['Errors']) 
	result = str(dict['Result'])
	stats = str(dict['Stats'])

	'''
	print("text : "+res.text)
	print("headers : "+str(res.headers))
	print("raise_for_status : "+str(res.raise_for_status))
	print("url : "+res.url)
	'''

	if errors == "None" and warnings == "None":
		return render(request, 'runcode/home.html', {
	    	'warnings' : warnings,
	    	'errors' : errors,
	    	'result' : result,
	    	'stats' : stats ,
	    	'alert' : 'success'
	    	})




	return render(request, 'runcode/home.html', {
		'warnings' : warnings,
		'errors' : errors,
		'result' : result,
		'stats' : stats
		})