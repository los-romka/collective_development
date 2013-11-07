"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.

from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        
        Tests that 1 + 1 always equals 2.
        
        self.assertEqual(1 + 1, 2)
"""

# coding: utf-8
import re
from django.core import mail
from django_webtest import WebTest
from webtest import TestApp
 
class SanityTests(WebTest):
    fixtures = ['users.json']

#TS_sanity_001 
    def testUrls(self):
        resp = self.app.get('/') 
        assert resp.status_int == 200
        resp = self.app.get('/preview/1/')
        assert resp.status_int == 200 
        resp = self.app.get('/buy/1/1/')
        assert resp.status_int == 200
        resp = self.app.get('/preview_best/1/')
        assert resp.status_int == 200
        resp = self.app.get('/albums/1/')
        assert resp.status_int == 200
        resp = self.app.get('/albums/1/1')
        assert resp.status_int == 200
        resp = self.app.get('/about/')
        assert resp.status_int == 200 
        resp = self.app.get('/about/feedback/')
        assert resp.status_int == 200

logger.setLevel(previous_level)
"""#TS_sanity_001 
    def testHome(self):
        resp_home = self.app.get('/') 
        assert resp_home.status_int == 200

    def testPreview(self): 
        resp_preview = self.app.get('/preview/1/')
        assert resp_preview.status_int == 200

    def testBuy(self): 
        resp_preview = self.app.get('/buy/1/1/')
        assert resp_preview.status_int == 200

    def testPreview_best(self): 
        resp_best = self.app.get('/preview_best/1/')
        assert resp_best.status_int == 200

    def testAlbum(self): 
        resp_album = self.app.get('/albums/1/')
        assert resp_album.status_int == 200

    def testAbout(self): 
        resp_about = self.app.get('/about/')
        assert resp_about.status_int == 200

    def testFeedback(self): 
        resp_feedback = self.app.get('/about/feedback/')
        assert resp_feedback.status_int == 200

#TS_sanity_002
    def testHeader(self):  
        resp_home = self.app.get('/')
        resp_home.mustcontain('<head>','</head>')
        resp_home.mustcontain('<title>Vashchenko.com</title>')

    def testFooter(self):        
        resp_about = self.app.get('/')
        resp_about.mustcontain('<foot>','</foot>')
        resp_about.mustcontain('Copyright 2013','Yuri Vashchenko. All rights reserved')

    def testBody(self):
        resp_feedback = self.app.get('/')
        resp_feedback.mustcontain('<body>','</body>')
        resp_feedback.mustcontain('HOME','GALLERY','ABOUT')

#TS_sanity_003
    def testPreviewButtons(self):  
        resp_preview = self.app.get('/about/')
        resp_preview.showbrowser()
        assert resp_preview.status_int == 200
        resp_preview.click(u'buyButton')"""
