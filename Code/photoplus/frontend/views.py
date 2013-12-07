from django.http         import Http404
from django.shortcuts    import render_to_response
from django.template     import Context, loader, Template
from django.http         import HttpResponse
from apiclient.discovery import build
from frontend.models     import *
from sys                 import *
from math                import *
from django.core.mail      import send_mail
from django.template       import RequestContext
from django.http      import HttpResponseRedirect
from frontend.forms       import ReCaptchaForm
from frontend.forms       import buyForm
from frontend.models      import *
from django.core.mail      import EmailMultiAlternatives
from django.core.mail      import EmailMessage
from django.conf      import settings
from email.MIMEImage      import MIMEImage
from django          import template
from config             import *
# import gdata.photos.service
from datetime            import date, timedelta
import re
#import gdata.media
#import gdata.geo
import cgi
import datetime, time, calendar

import sys, traceback
from frontend.updates   import *

LAST_VISIT_TO_ACCOUNT = 0


def clear_db( ):

    p = Post.objects.all()
    t = Tag.objects.all()
    p.clear()
    t.clear()
    return

def contact(request):
    al = Album.objects.all()
    a = Author.objects.get(id=1)
    form = ReCaptchaForm()
    if request.POST:
        form = ReCaptchaForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', a.email), [a.email], fail_silently=False
                    )
            return HttpResponseRedirect('/about/')
    else:
        form = ReCaptchaForm(  initial={'subject': 'I love your site!'}
                 )
    return render_to_response('contact.html', {'form': form, 'album_list':al}, context_instance=RequestContext(request))


def buy(request, idP, resolution):    
    try:
        al = Album.objects.all()
        a = Message.objects.get(id=1)
        pr = Price.objects.get( id = resolution)
        a = Message.objects.get(id=1)
        pr = Price.objects.get( id = resolution)
        idP = str(idP)

    except Post.DoesNotExist:
        raise Http404
   
    t_to = Template(a.information_to) #to you
    t_from = Template(a.information_from) #from you/ means from admin
    s_to = Template(a.subject_to)
    s_from = Template(a.subject_from)

    codepage = request.get_host()
       
    form = buyForm()
    if request.POST:
        form = buyForm(request.POST)
        if form.is_valid():
    
            cd = form.cleaned_data

            subject_to = a.subject_to
            email_from = a.email
            email_to = cd['Email']
            country = cd['Country']
            street1 = cd['Address1']
            street2 = cd['Address2']
            city = cd['City']
            state = cd['State']
            zip_code = cd['Index']
            f_name = cd['FirstName']
            l_name = cd['LastName']
            price = pr.price
            size = str(pr.size) + u"*" + str(pr.on)
            post_title = "photo"
            image_url =  "https://plus.google.com/photos?pid="+idP+"&oid="+ACCOUNT_ID
            post_url =  image_url
        
            order = Order(name= l_name + u" " + f_name,
              adress = street1 + u", " + street2 + u", " + city + u", " + state + u", " + country + u", " + zip_code,
              photo_id = image_url,
              price = price,
              size = size,
              status = 'RECEIVED'
            )
            order.save()       
            idorder = order.id
            orderref = codepage + u'/order/' +   str(idorder) + u'/'
   
            c = Context({"f_name": f_name, "l_name": l_name, "country": country, "street1": street1, "street2": street2, "city":city, "state": state,  "zip_code": zip_code, "price": price, "size": size, "post_title":post_title, "image_url":image_url, "post_url": post_url, "orderref": orderref, "idorder": idorder })
        
            message_from = t_from.render(c)
            subjectmessage_from = s_from.render(c)

            message_to = t_to.render(c)
            subjectmessage_to = s_to.render(c)
    
            msg_from= EmailMessage(subjectmessage_from, message_from, email_from, [email_to]) 
            msg_from.content_subtype = "html"  # Main content is now text/html
           
            msg_from.send()

            msg_to = EmailMessage(subjectmessage_to, message_to, email_from, [email_from]) 
            msg_to.content_subtype = "html"  # Main content is now text/html
           
            msg_to.send()
            return HttpResponseRedirect('/preview/' + str(idP))
    else:
        form = buyForm()
    return render_to_response('buy.html', {'form': form, 'buy':a, 'album_list':al }, context_instance=RequestContext(request))


#--------------------------------------------------------------------------------------------------
#                                          ABOUT
#--------------------------------------------------------------------------------------------------

def about(request):
    try:
        a = Author.objects.get(id=1)
        al = Album.objects.all()
    except Post.DoesNotExist:
        raise Http404
    return render_to_response('about.html',{ 'about':a , 'album_list':al })
#--------------------------------------------------------------------------------------------------
#                                          PREVIEW
#--------------------------------------------------------------------------------------------------
# def preview(request, idP ):
#     try:
#         idP = int(idP)
#         photo = Post.objects.get( id = idP )
#         prices = Price.objects.all()
#     except Post.DoesNotExist:
#         raise Http404
#     return render_to_response('preview.html',{ 'photo':photo , 'prices':prices })

def preview(request, photoId):
    try:
        photo = str(photoId)
        prices = Price.objects.all()
    except Post.DoesNotExist:
        raise Http404
    photo_url = 'https://plus.google.com/u/0/photos/'+ACCOUNT_ID+'/albums/'+BEST_PHOTO_ALBUM+'/'+photo
  
   # raise Exception, photo_url
    return render_to_response('preview.html',{ 'photo':photo ,'photo_url': photo_url,'account':ACCOUNT_ID, 'albumId':BEST_PHOTO_ALBUM, 'photoId': photoId, 'prices':prices })  
#--------------------------------------------------------------------------------------------------
#                                      GET_PAGINATOR_DATA
#--------------------------------------------------------------------------------------------------
def get_paginator_data( page, pages, adjacent_pages=2 ):
    startPage = max(page - adjacent_pages, 1)
    if startPage <= 3: startPage = 1
    endPage = page + adjacent_pages + 1
    if endPage >= pages - 1: endPage = pages + 1
    page_numbers = [n for n in range(startPage, endPage) \
            if n > 0 and n <= pages]
    if page != 1:
        has_previous = True
    else:
        has_previous = False
    if page != pages:
        has_next = True
    else:
        has_next = False
    if has_previous:
        previous_p = page - 1
    else:
        previous_p = 1
    if has_next:
        next_p = page + 1
    else:
        next_p = pages
    
    return {
        'page': page,
        'pages': pages,
        'page_numbers': page_numbers,
        'next': next_p,
        'previous': previous_p,
        'has_next': has_next,
        'has_previous': has_previous,
        'show_first': 1 not in page_numbers,
        'show_last': pages not in page_numbers,
    }

#--------------------------------------------------------------------------------------------------
#                                       DESCRIBE_ALBUM
#--------------------------------------------------------------------------------------------------
def album( request , idA, page = 1):
    
    page = int(page)
    
    if (page < 1):
        raise Http404
    try:
        album = Album.objects.get( id = idA)
        al = Album.objects.all()

        photos = []
        for tag in album.tags.all():
            posts = tag.posts.all()
            for post in posts:
                if post not in photos:
                    photos.append(post)
    except Album.DoesNotExist:
        raise Http404
#    photos.sort(key=lambda post: post['id'])
    photos.sort(reverse=True)

    num_last = 10 * page
    num_first = 10 * (page - 1)
    
    pages = int(ceil(len(photos) / 10.0))
    paginator = get_paginator_data( page, pages , 2 )
    photos = photos[num_first:num_last]
    
    num_first = num_first + 1
    num_last = num_first + len(photos) - 1
    
    return render_to_response('albums.html',{'photos':photos, 'album':album , 'album_list':al, 'paginator':paginator, 'nl':num_last, 'nf':num_first})


#--------------------------------------------------------------------------------------------------

def home_page( request, page ):
    
    page = int(page)
    num_last = 10 * page
    num_first = 10 * (page - 1)
    
    try:
        last = Post.objects.order_by('-renew')[num_first:num_last]
        al = Album.objects.all()
    except Post.DoesNotExist:
        raise Http404
    
    num_first = num_first + 1
    num_last = num_first + len(last) - 1
    
    pages = int(ceil(Post.objects.count() / 10.0))
    paginator = get_paginator_data( page, pages , 2 )
    
    return render_to_response('index.html',{ 'last':last, 'paginator':paginator, 'nl':num_last, 'nf':num_first, 'album_list':al })

#-----------------------------------------------------------------------------------------------------

def home( request ):
    #refresh_db_with_quantity(get_need_updates())

    t = Thread(target = refresh_db_with_quantity, args = get_need_updates())
    t.start()
    t.join()
    try:
        last = Post.objects.order_by('-renew')[0:10]
        al = Album.objects.all()
    except Post.DoesNotExist:
        raise Http404
    
    page = 1
    pages = int(ceil(Post.objects.count() / 10.0))
    paginator = get_paginator_data( page, pages , 2 )
    num_last = len(last)
    
    
    return render_to_response('index.html',{ 'last':last,'account': ACCOUNT_ID,'album_id': BEST_PHOTO_ALBUM, 'best':last[:3], 'paginator':paginator, 'nl':num_last, 'nf':1, 'album_list':al })

def change_albums_name(album_name):
    album_name.strip()
    album_name.replace(' ', '-')
    return album_name


def order(request, idOrder):
    try:
        al = Album.objects.all()
        orderlast = Order.objects.get(id=idOrder)
        ordersall = Order.objects.filter(name=orderlast.name, adress = orderlast.adress)

    except Post.DoesNotExist:
        raise Http404
    return render_to_response('order.html',{ 'ordersall':ordersall , 'orderlast':orderlast, 'album_list':al })


