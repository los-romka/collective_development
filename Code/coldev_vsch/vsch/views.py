# Create your views here.
from django.http import Http404
from django.shortcuts import render_to_response
from vsch.models import *

def home(request):
	return render_to_response('index.html')


