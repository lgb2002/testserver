from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
 
def keyboard(request):
 
        return JsonResponse({
                'type' : 'buttons',
                'buttons' : ['1','2']
                })

@csrf_exempt
def message(request):
        #message = ((request.body).decode('utf-8')) 
        return_json_str = json.loads(request)
        print(request)
        return_str = return_json_str['content']
 
        return JsonResponse({
                'message': {
                        'text': "you type "+return_str+"!"
                },
                'keyboard': {
                        'type': 'buttons',
                        'buttons': ['1','2']
                }
        })