#from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def keyboard(request):
	return JsonResponse(
		{
		'type' : 'buttons',
		'buttons' : ['hello', 'world', 'lgb'] 
		}
	)

@csrf_exempt
def message(request):
	json_str = (request.body).decode('utf-8')
	received_json = json.loads(json_str) #JSON File Decoding
	content_name = received_json['content']	
	if content_name == 'hello':
		return JsonResponse(
			{
				'message' : {
					'text' : 'You say hello'
				}
			}
		)
	elif content_name == 'world':
		return JsonResponse(
			{
				'message' : {
					'text' : 'We are the world'
				}
			}
		)
	elif content_name == 'lgb':
		return JsonResponse(
			{
				'message' : {
					'text' : 'Your id is lgb'
				}
			}
		)