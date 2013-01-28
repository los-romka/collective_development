import pprint
import sys
from apiclient.discovery import build

api_key = sys.argv[1]

service = build('plus', 'v1', developerKey=api_key)

#people_resource = service.people()
#people_document = people_resource.get(userId='103582189468795743999').execute()


#print "ID: " + people_document['id']
#print "Display name: " + people_document['displayName']
#print "Image URL: " + people_document['image']['url']
#print "Profile URL: " + people_document['url']

activities_resource = service.activities()
request = activities_resource.list(
                                   userId='103582189468795743999',
                                   collection='public',
                                   maxResults='2')

while request != None:
    activities_document = request.execute()
    if 'items' in activities_document:
        print 'got page with %d' % len( activities_document['items'] )
        for activity in activities_document['items']:
            print activity['id'], activity['object']['content']
    
    request = serviceUnauth.activities().list_next(request, activities_document)

print "----------------------"