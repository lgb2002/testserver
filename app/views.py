from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from bs4 import BeautifulSoup
#from urllib.request import urlopen
from datetime import datetime
import re

datetime.today()
year=datetime.today().year
month=datetime.today().month
day=datetime.today().day

imsi = "http://www.puhung.hs.kr/wah/main/schoolmeal/view.htm?menuCode=80&moveType=&domain.year="+str(year)+"&domain.month="+str(month)+"&domain.day="+str(day)
#html = urlopen(imsi)
#soup = BeautifulSoup(html.read(), "html.parser")
#test = soup.find(class_="Schoolmeal_Cont_Cont_Cont")
#test2 = test.get_text()
#m = re.sub(" ?\d ?[.]*"," ",test2)
#m = re.sub(" +","\n",m)
#print(m)
 

def keyboard(request):
	return JsonResponse({
            'type' : 'buttons',
            'buttons' : ['today','tommorow']
            })

@csrf_exempt
def answer(request):
	    message = ((request.body).decode('utf-8')) 
	    return_json_str = json.loads(message)
	    return_str = return_json_str['content']

	    return JsonResponse({
	        'message' : {
	            'text' : "you choose!"+return_str+" : "#+test
	            },
	        'keyboard' : {
	            'type': 'buttons',
	           	'buttons' : ['today','tommorow']
	            }
	        })