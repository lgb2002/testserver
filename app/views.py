from django.shortcuts import render
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

	#button = ['hello', 'world', 'lgb']

	json_str = (request.body).decode('utf-8')
	received_json = json.loads(json_str) #JSON File Decoding
	content_name = received_json['content']	

	#user_name = received_json['user_key']
	#user_name
	#type_name = received_json['type']
	#type_name

	If content_name == "hello":
		return JsonResponse(
			{

				'message' : {
					'text' : 'You say hello'
				},
				'keyboard' : {
					'type' : 'buttons',
					'buttons' : ['hello', 'world', 'lgb']
				}
			}
		)
	elif content_name == "world":
		return JsonResponse(
			{

				'message' : {
					'text' : 'We are the world'
				},
				'keyboard' : {
					'type' : 'buttons',
					'buttons' : ['hello', 'world', 'lgb']
				}
			}
		)
	elif content_name == "lgb":
		return JsonResponse(
			{

				'message' : {
					'text' : 'Your id is lgb'
				},
				'keyboard' : {
					'type' : 'buttons',
					'buttons' : ['hello', 'world', 'lgb']
				}
			}
		)