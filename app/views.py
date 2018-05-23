from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from bs4 import BeautifulSoup
import requests
from datetime import datetime

def get_html(url) :
	_html = ""
	resp = requests.get(url)
	if resp.status_code == 200:
		_html = resp.text
	return _html

datetime.today()
year=datetime.today().year
month=datetime.today().month
day=datetime.today().day

imsi = "http://www.puhung.hs.kr/wah/main/schoolmeal/view.htm?menuCode=80&moveType=&domain.year="+str(year)+"&domain.month="+str(month)+"&domain.day="+str(day)
html = get_html(imsi)
soup = BeautifulSoup(html, 'html.parser')
test = soup.find('<div class="Schoolmeal_Cont_Cont_Cont">')




@csrf_exempt
def keyboard(request):
	return JsonResponse({
            'type' : 'buttons',
            'buttons' : ['today','tommorow']
            })
def answer(request):
	    message = ((request.body).decode('utf-8')) 
	    return_json_str = json.loads(message)
	    return_str = return_json_str['content']

	    return JsonResponse({
	        'message': {
	            'text': "you choose!\n"+return_str+" : \n"+test
	            },
	            'keyboard': {
	            'type': 'buttons',
	           	'buttons' : ['today','tommorow']
	            }
	        })