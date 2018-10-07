from django.shortcuts import render
import requests, json, os, urllib
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlencode
from django.utils import timezone
from runcode.models import *
from datetime import datetime

def index(request):
	login = 0
	if login:
		print("login : " + login)
		return render(request, 'runcode/index.html', {})
	else:
		return render(request, 'runcode/login.html', {
			'error' : 'error'
			})
		'''return HttpResponse("Login Error")'''


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
			return render(request, 'runcode/login.html', {'user_id' :user_id, 'user_pwd' : user_pwd, 'error' : 'No Error'})

		except UserInfo.DoesNotExist:
			print(" Error! No Match UserInformation! ")
			login = Login(login_id = get_id, login_pwd = get_pwd, login_date = datetime.now(), login_error = "No Match")
			login.save()
			imsi_login = Login.objects.filter(login_id = get_id, login_pwd = get_pwd).order_by('login_date').last()
			error = imsi_login.login_error
			return render(request, 'runcode/login.html', {'user_id' : "No id", 'user_pwd' : "No pwd", 'error' : error})







@csrf_exempt
def run(request):
	#choice = request.POST.get('choice','')
	#print("choice:"+choice)

	if request.method == "POST":
		message = str(request.body, encoding='utf-8')
		#if choice == 4:
			#message = str(request.body, encoding='utf-8')
		#elif choice != 4:
			#message = str(request.body, encoding='utf-8')

	else :
		return render(request, 'runcode/index.html', {
	    	'warnings' : "None",
	    	'errors' : "None",
	    	'result' : "None",
	    	'stats' : "None"
	    	})

	print("test message:" + message)

	url = "http://rextester.com/rundotnet/Run"
	headers = {'Accept': 'text/plain, */*; q=0.01', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Referer':
'http://rextester.com/l/bash_online_compiler', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
'X-Requested-With': 'XMLHttpRequest'}

	res = requests.post(url, headers=headers , data=message)

	j = res.json()
	jsonString = json.dumps(j, indent=4)

	dict = json.loads(jsonString)
	warnings = str(dict['Warnings'])
	errors = str(dict['Errors']) 
	result = str(dict['Result'])
	stats = str(dict['Stats'])

	'''print("text : "+res.text)
	print("headers : "+str(res.headers))
	print("raise_for_status : "+str(res.raise_for_status))
	print("url : "+res.url)'''

	'''
	return JsonResponse({
	    'runcode/run' : {
	    	'warnings' : warnings,
	    	'errors' : errors,
	    	'result' : result,
	    	'stats' : stats
	    	}
	    })
	'''
	'''if choice == 4:
		return render(request, 'runcode/index.html', {
		    	'warnings' : warnings,
		    	'errors' : errors,
		    	'result' : result,
		    	'stats' : stats
		    	})
	else:
		return render(request, 'runcode/index.html', {
		    	'warnings' : warnings,
		    	'errors' : errors,
		    	'result' : result,
		    	'stats' : stats
		    	})'''
	return render(request, 'runcode/index.html', {
		    'warnings' : warnings,
		   	'errors' : errors,
		   	'result' : result,
		   	'stats' : stats
		   	})
	#elif request.POST.get('choice') != 4:
