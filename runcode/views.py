from django.shortcuts import render
import requests, json, os, urllib
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlencode
from .models import Post
from django.utils import timezone


def index(request):
	login = 0
	if login:
		print("login : " + login)
		return render(request, 'runcode/index.html', {})
	else:
		return render(request, 'runcode/login.html', {})
		'''return HttpResponse("Login Error")'''


def login(request):
	posts = Post.objects.filter(published_data__lte=timezone.now()).order_by('published_data')
	return render(request, 'runcode/login.html', {'posts':posts})


@csrf_exempt
def run(request):

	if request.method == "POST":
		message = str(request.body, encoding='utf-8')
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
	return render(request, 'runcode/index.html', {
	    	'warnings' : warnings,
	    	'errors' : errors,
	    	'result' : result,
	    	'stats' : stats
	    	})