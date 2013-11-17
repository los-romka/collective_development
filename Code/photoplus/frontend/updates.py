from frontend.models     import Post, Tag
from django.core.exceptions import ObjectDoesNotExist
from frontend.rfc3339				import *
from apiclient.discovery import build

def refresh_db(new_data):
    
	for element in new_data:
		try:
			p = Post.objects.get( image_url = element[0] )
			p.delete()
		except ObjectDoesNotExist:
			pass
		p = Post( image_url = element[0] , renew = element[1] , post_url = element[2] , post_title = element[3] )
		p.save()
		#eeefasdf
		
		for tag in element[4]:
			try:
				t = Tag.objects.get( name = tag )
			except ObjectDoesNotExist:
				t = Tag( name = tag )
				t.save()
			t.posts.add(p)
			t.save()
	Post.objects.order_by('-renew')

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

	
def get_one_page_of_activities(page_token = ''):
	service = build(     'plus',
						 'v1', 
	developerKey =       'AIzaSyAKCO6eEQHQLN32ZARi2TOoJXVP88EZW4c')
	activities_resource = service.activities()
	request = activities_resource.list(
	userId =             '100915540970866628562',                                               #'103582189468795743999',
	collection =         'public',
	maxResults =         '30',
	pageToken =           page_token
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
	
def get_all_photo_on_one_page( page_token = ''):
	return filter_only_photo_from_page( get_one_page_of_activities (page_token ) )
	
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
		act_list.append( act_struct )
	return act_list
	
def refresh_db_with_days(days):
	result_activity_list = get_all_photo_on_one_page()
	result_activity_list = filter_by_date(result_activity_list, days)
	activity = result_activity_list
	while len(activity['items']) != 0 and 'nextPageToken' in activity:
		activity = get_all_photo_on_one_page( activity['nextPageToken'] )
		activity = filter_by_date(activity, days)
		result_activity_list['items'] += activity['items']
	refresh_db (api_data_extraction_old ( result_activity_list ) )

def refresh_db_with_quantity( quantity ):
	result_activity_list = get_all_photo_on_one_page()
	activity = result_activity_list
	while 'nextPageToken' in activity and len( result_activity_list['items']) <= quantity :
		activity = get_all_photo_on_one_page( activity['nextPageToken'] )
		back_index = quantity - len( result_activity_list['items'] ) - len( activity['items'] )
		if back_index >= 0: 
			back_index = len( activity['items'] )
		result_activity_list['items'] += activity['items'][:back_index]
	refresh_db (api_data_extraction_old ( result_activity_list ) )
		
def refresh_db_with_all ():
	result_activity_list = get_all_photo_on_one_page()
	activity = result_activity_list
	while 'nextPageToken' in activity:
		activity = get_all_photo_on_one_page( activity['nextPageToken'] )
		result_activity_list['items'] += activity['items']
	refresh_db (api_data_extraction_old ( result_activity_list ) )
