from django.shortcuts import render
import requests,json, os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
from urllib.request import urlopen


def index(request):
	return render(request, 'runcode/index.html', {})


def run(request):
	url = 'http://rextester.com/rundotnet/Run'
	data ={'LanguageChoiceWrapper' : '38' ,
			'EditorChoiceWrapper' : '1' ,
			'LayoutChoiceWrapper' : '1' ,
			'Input' : '' ,
			'Privacy' : '' ,
			'PrivacyUsers' : '' ,
			'Title' : '' ,
			'SavedOutput' : '' ,
			'WholeError' : '' ,
			'WholeWarning' : '' ,
			'StatsToSave' : '' ,
			'CodeGuid' : '' ,
			'IsInEditMode' : 'False' ,
			'IsLive' : 'False' ,
			'Program' : '#!/bin/bash # GNU bash, version 4.3.46 echo "Hello, world!";' }
	res = requests.post(url, data=data)
	j = res.json()
	'''print(data)'''
	jsonString = json.dumps(j, indent=4)
	print(jsonString)
	dict = json.loads(jsonString)
	warnings = str(dict['Warnings'])
	errors = str(dict['Errors']) 
	result = dict['Result']
	stats = dict['Stats']
	'''
	print(res.text)
	print("result :"+result)
	print("warnings :"+warnings)
	print("errors : "+errors)
	print("stats : "+stats)
	'''
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