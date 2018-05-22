from django.shortcuts import render
from django.http import JsonResponse

def keyboard(request):

	return JsonResponse(
		{
		'type' : 'buttons',
		'buttons' : ['test1', 'test2', 'test3'] 
		}
	)