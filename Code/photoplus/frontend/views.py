# Create your views here.
from django.http import Http404
from django.shortcuts import render_to_response
from frontend.models import *

def albums(request):
	return render_to_response('albums.html')

def about(request):
	return render_to_response('about.html')

def home(request):
	return render_to_response('index.html')


