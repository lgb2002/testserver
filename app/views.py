from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from bs4 import BeautifulSoup
import requests
from datetime import datetime

datetime.today()
year=datetime.today().year
month=datetime.today().month
day=datetime.today().day

html = get_html("www.puhung.hs.kr/wah/main/schoolmeal/view.htm?menuCode=80&moveType=&domain.year="+year+"&domain.month="+month+"&domain.day="+day)
soup = BeautifulSoup(html, 'html.parser')
test = soup.find('<div class="Schoolmeal_Cont_Cont_Cont">')


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

        if
        return JsonResponse({
                'message': {
                        'text': "you choose!\n"+return_str" : \n"+test
                },
                'keyboard': {
                        'type': 'buttons',
                        'buttons': ['1','2']
                }
        })