from django.shortcuts import render
import requests,json
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
			'Program' : '#!/bin/bash # GNU bash, version 4.3.46 echo "Hello, world!";' ,
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
			'IsLive' : 'False'}
	res = requests.post(url, data=data)
	print(res.request)

	return render(request, 'runcode/index.html', {})
	