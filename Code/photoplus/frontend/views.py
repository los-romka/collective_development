


from django.http         import Http404
from django.shortcuts    import render_to_response
from django.template     import Context, loader
from django.http         import HttpResponse

from apiclient.discovery import build
from frontend.models     import *
from sys                 import *





# Parsing tag info 

# in : string with hashtags
# out: list of tags( strings )

def get_tags_list( hashstring ):

    spis = []
    for e in range( 0,hashstring.count("ot-hashtag") ):
        r = hashstring.find('#')+1
        hashstring = hashstring[r:]
        t = hashstring.find('<')
        spis.append( hashstring[:t] )
    return spis





# Extracting data from 
# personal account of Yuri Vashchenko

# in : ---
# out: list of structures like ---> [ url , [ #1_ht , #2_ht , ..

# ! Important: single use of this function spares 1 / 10.000 of API request !

def api_data_extraction():
    
    service = build(     'plus',
                         'v1', 
    developerKey =       'AIzaSyAKCO6eEQHQLN32ZARi2TOoJXVP88EZW4c')
    activities_resource = service.activities()
    request = activities_resource.list(
    userId =             '100915540970866628562',                                               #'103582189468795743999',
    collection =         'public',
    maxResults =         '100' )

    act_list = []
    activities_document = request.execute()
    if 'items' in activities_document:                                                          # if account is not empty
        for activity in activities_document['items']:                                           # taking every activity
            if 'actor' not in activity['object']:                                               # if activity is not reshared
                if 'attachments' in activity['object']:                                         # if activity has attachments
                    if activity['object']['attachments'][0]['objectType'] == "photo":           # if activity type is photo

                        act_struct = []                                                         # [ url , [ #1_ht , #2_ht , ... ] ]
                        act_struct.append( activity['object']['attachments'][0]['fullImage']['url'] ) 
                        act_struct.append( activity['updated'] )
                        act_struct.append( get_tags_list( activity['object']['content'] ) )

                        act_list.append( act_struct )
    return act_list





def refresh_db_with_new_data( ):

    new_data = api_data_extraction()
    for element in new_data:
        p = Post( image_url = element[0] , renew = element[1] )
        p.save()
        if len(element) == 3:
            for tag in element[2]:
                t = Tag ( name = tag )
                t.save()
                t.posts.add(p)
                t.save()
    return





def clear_db( ):

    p = Post.objects.all()
    t = Tag.objects.all()
    p.entry_set.clear()
    t.entry_set.clear()
    return





def albums( request ):

    return render_to_response('albums.html')





def about( request ):

    return render_to_response('about.html')





def home( request ):

    #refresh_db_with_new_data()
    try:
        p = Post.objects.all()
    except Post.DoesNotExist:
        raise Http404
    return render_to_response('index.html',{ 'lst':p })




