# Create your views here.
from django.http         import Http404
from django.shortcuts    import render_to_response
from frontend.models     import *
from django.template     import Context, loader
from django.http         import HttpResponse
from sys                 import *
from apiclient.discovery import build

# preparing API platform
service = build(    'plus',
                    'v1', 
developerKey=       'AIzaSyAKCO6eEQHQLN32ZARi2TOoJXVP88EZW4c')
activities_resource = service.activities()
request = activities_resource.list(
userId=             '100915540970866628562',#'103582189468795743999',
collection=         'public',
maxResults=         '100' )
var = []
activities_document = request.execute()
if 'items' in activities_document:                                                          # if account is not empty
    for activity in activities_document['items']:                                           # taking every activity
        if 'actor' not in activity['object']:                                               # if activity is not reshared
            if 'attachments' in activity['object']:                                         # if activity has attachments
                if activity['object']['attachments'][0]['objectType'] == "photo":           # if attachement type is photo
                    var.append(activity['object']['attachments'][0]['fullImage']['url'])   
                    
                    # Geting a list of items prom users profile and parsing them
                    hash_tag_string = activity['object']['content']
                    get_tags_list( hash_tag_string )

# Parsing tag info 
# in : string with hashtags
# out: list of strings-tags
def get_tags_list(hashstring):
  spis = []
  for e in range( 0,hashstring.count("ot-hashtag") ):
    r = hashstring.find('#')+1
    hashstring = hashstring[r:]
    t = hashstring.find('<')
    spis.append( hashstring[:t] )
  print spis




def albums(request):
    return render_to_response('albums.html')

def about(request):
    return render_to_response('about.html')

def home(request):

    #albums_list = Album.objects.all()
    return render_to_response('index.html',{ 'lst':var })