# Create your views here.
from django.http import HttpResponse
import datetime

def cur(request):
	now = datetime.datetime.now()
	html = "<html><body><p>It is now %s</p></body></html>" % now
	return HttpResponse(html)
