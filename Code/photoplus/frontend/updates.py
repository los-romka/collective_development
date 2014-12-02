from models     import Post, Tag
from django.core.exceptions import ObjectDoesNotExist
from rfc3339				import *
from apiclient.discovery import build
from django.http      import HttpResponseRedirect
from config             import ACCOUNT_ID
from threading			import *

lock = Lock()
isBusy = False

def refresh_db(new_data, all_records = False):
	if len(new_data) == 0:
		return
	
	if not all_records:
		new_ids = [element[5] for element in new_data]
		Post.objects.filter(post_id__in=new_ids).delete()

	for element in new_data:
		p = Post.objects.create(image_url = element[0] , renew = element[1] , post_url = element[2] , post_title = element[3], post_id = element[5], photo_id = element[6])		
			
		for tag in element[4]:
			t,created = Tag.objects.get_or_create(name = tag)
			t.posts.add(p)

def get_tags_list( hashstring ):

    hashstring = hashstring.replace("&#","")
    tags_list = []
    for e in range( 0,hashstring.count("ot-hashtag") ):
        r = hashstring.find('#')+1
        hashstring = hashstring[r:]
        t = hashstring.find('<')
        tags_list.append( hashstring[:t] )
    return tags_list
	
def strip_title( text ):
    if ( text.startswith("<b>") != True ):
        return ""
    pos = text.find("</b>")
    if (pos == -1):
        return ""
    title = text[3:pos]
    
    if ( (">" in title) or ("<" in title) or (len(title) > 30 ) ):
        return ""
    return title

def get_activities_resource():
	service = build(     'plus',
						 'v1', 
	developerKey =       'AIzaSyAKCO6eEQHQLN32ZARi2TOoJXVP88EZW4c')
	return service.activities()

def get_one_page_of_activities(page_token = '', max_res = '10'):
	activities_resource = get_activities_resource();
	request = activities_resource.list(
	userId =             ACCOUNT_ID,       
	collection =         'public',
	maxResults =         max_res,
	pageToken =           page_token,
	fields = 'nextPageToken,items(id, updated, url,  object(actor, content, attachments(id,objectType, fullImage/url)))'
	)
	return request.execute()
	
def filter_only_photo_from_page(list_of_activities):
	if 'items' not in list_of_activities:
		list_of_activities['items'] = []
		return list_of_activities
	filtered_list = []
	
	for activity in list_of_activities['items']:
		if 'actor' not in activity['object'] and 'attachments' in activity['object'] and activity['object']['attachments'][0]['objectType'] == "photo":
			filtered_list.append(activity)
	list_of_activities['items'] = filtered_list
	return list_of_activities	
	
def get_all_photo_on_one_page( page_token = '', max_res = '100'):
	return filter_only_photo_from_page( get_one_page_of_activities (page_token, max_res) )
	
def filter_by_date( activity, num_days ):
	items = []
	min_day = date.today() - timedelta(days = num_days)
	for its in activity['items']:
		current = parse_datetime( its['updated']).date()
		if current > min_day:
			items.append(its)
		activity['items'] = items
	return activity
	
def api_data_extraction_old(activities_document):
	
	act_list = []
	for activity in activities_document['items']:
		tags = get_tags_list( activity['object']['content'])
		if 'no' in tags or 'No' in tags or 'NO' in tags:
			continue
		act_struct = []
		act_struct.append( activity['object']['attachments'][0]['fullImage']['url'] ) 
		act_struct.append( activity['updated'] )
		act_struct.append( activity['url'] )
		act_struct.append( strip_title( activity['object']['content'][:40] ) )
		#act_struct.append( get_tags_list( activity['object']['content'] ) )
		act_struct.append( tags )
		act_struct.append( activity['id'])
		act_struct.append( activity['object']['attachments'][0]['id'].split('.')[1])

		
		act_list.append( act_struct )

	return act_list



def get_need_updates():
	global isBusy
	
	with lock:
		if isBusy:
			return 0, []
		isBusy = True
	
	if Post.objects.count() == 0:
		refresh_db_with_all()
		return 0, []
	
	data = api_data_extraction_old ( get_all_photo_on_one_page(max_res = '5') )
		
	new_ids = [ element[5] for element in data ]
	new_renew = [ element[1] for element in data ] 
	
	
	p = Post.objects.order_by('-renew')
	p = p[0]
	old_id = p.post_id
	old_renew = p.renew
	
	try:
		index = new_ids.index(old_id)
	except ValueError:
		return 0, data
	
	if new_renew[index] != old_renew :
		return index + 1, data;
	return index, data

	
def refresh_db_with_days(days):
	result_activity_list = get_all_photo_on_one_page()
	result_activity_list = filter_by_date(result_activity_list, days)
	activity = result_activity_list
	while len(activity['items']) != 0 and 'nextPageToken' in activity:
		activity = get_all_photo_on_one_page( activity['nextPageToken'] )
		activity = filter_by_date(activity, days)
		result_activity_list['items'] += activity['items']
	refresh_db (api_data_extraction_old ( result_activity_list ) )
	
	
def refresh_db_with_quantity( obj ):
	global isBusy
	
	quantity = obj[0]
	data = obj[1]
	if quantity == 0 :
		with lock:
			isBusy = False
		return 
	
	if data != []:
		refresh_db (data )
		with lock:
			isBusy = False
		return
		
	result_activity_list = get_all_photo_on_one_page()	
	activity = result_activity_list
	while 'nextPageToken' in activity and len( result_activity_list['items']) < quantity :
		activity = get_all_photo_on_one_page( activity['nextPageToken'] )
		result_activity_list['items'] += activity['items']
		
	result_activity_list['items'] = result_activity_list['items'][0:quantity]

	refresh_db (api_data_extraction_old ( result_activity_list ) )
	with lock:
		isBusy = False
	
def clear_all_db():
	Post.objects.all().delete()
	Tag.objects.all().delete()
	

def refresh_db_with_all ():
	
	result_activity_list = get_all_photo_on_one_page()
	activity = result_activity_list
	while 'nextPageToken' in activity:
		activity = get_all_photo_on_one_page( activity['nextPageToken'] )
		result_activity_list['items'] += activity['items']
	with lock:
		clear_all_db()
		refresh_db (api_data_extraction_old ( result_activity_list ), True )
	
#functions for forced update

def forced_refresh(request, mode = 1):
	
	if int(mode) == 1:
		refresh_db_with_quantity((100, []))
	if int(mode) == 2:
		refresh_db_with_days(30)
	if int(mode) == 3:
		refresh_db_with_all()
	return HttpResponseRedirect('../../../../admin/')
#end of functions for forced refresh
