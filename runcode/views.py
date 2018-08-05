from django.shortcuts import render
import requests, json, os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
from urllib.request import urlopen


def index(request):
	return render(request, 'runcode/index.html', {})


@csrf_exempt
def run(request):

	if request.method == "POST":
		message = str(request.body, encoding='utf-8')
		print("test message : " + message)
		'''return_json_str = json.loads(message)
		test = return_json_str['content']'''
		'''Language = message[10 : 12]
		Program = message[22 : len(message)-1]
		print("Language : "+Language)
		print("Program : "+Program)'''
	test = open("data.txt", 'w')
	test.write(message)

	url = 'http://rextester.com/rundotnet/Run'
	'''data = {'LanguageChoiceWrapper' : '38' ,
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
			'IsLive' : 'False' 
			}'''

	'''data['Program'] = message'''

	'''print("data['Program']: "+data['Program'])'''
	files = {'file' : open('data.txt', 'rb')}
	res = requests.post(url, files=files)
	j = res.json()
	jsonString = json.dumps(j, indent=4)
	print(jsonString)
	dict = json.loads(jsonString)
	warnings = str(dict['Warnings'])
	errors = str(dict['Errors']) 
	result = str(dict['Result'])
	stats = str(dict['Stats'])
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