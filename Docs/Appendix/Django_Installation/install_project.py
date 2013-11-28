#!/usr/bin/env python
# -*- coding: latin-1 -*-
import subprocess

def InstallUpgrade():
	#первые два пункта вроде без комментариев
	er = subprocess.call('sudo apt-get update', shell=True)
	print "----------------------update %s" % er
	er1 = subprocess.call("sudo apt-get upgrade", shell=True)
	print "----------------------upgrade %s" % er1
	
	#установка апача и питона
	return ""
def installApache():
	er1 = subprocess.call("sudo apt-get install apache2 libapache2-mod-wsgi", shell=True)
	print "----------------------apache2 libapache2-mod-wsgi %s" % er1
	return ""
def installPython():	
	er1 = subprocess.call("sudo apt-get install python python-mysqldb", shell=True)
	print "----------------------python-mysqldb %s" % er1
	return ""
def installPHP():
	#устанавливаем пэхэпэ и гэцэцэ
	er1 = subprocess.call("sudo apt-get install php5 php5-mysql", shell=True)
	print "----------------------sudo apt-get install php5 php5-mysql %s" % er1
	er1 = subprocess.call("sudo apt-get install gcc", shell=True)
	print "----------------------sudo apt-get install gcc %s" % er1
	return ""
	
def installClonDJ():	
	er1 = subprocess.call("git clone https://github.com/django/django.git", shell=True)
	print "----------------------git clone django %s" % er1
	return ""
	
def instalDj():
	per=subprocess.Popen("pwd", shell=True, stdout=subprocess.PIPE)
	cwdJInst=""
	cwdJInst="%s" % per.stdout.readlines()
	cwdJInst1=cwdJInst[2:-4]
	cwdJInst=cwdJInst[2:-4]+"/django"
	
	print "cwdJInst %s" % cwdJInst
	er1 = subprocess.Popen("ls", cwd=cwdJInst, shell=False).wait()
	er1 = subprocess.Popen('sudo python setup.py install', cwd=cwdJInst, shell=True).wait()
	print "----------------------install django %s" % er1
	return ""
	
def instApiPyth():
	er1 = subprocess.call("sudo apt-get install python-pip", shell=True)
	print "----------------------install python-pip %s" % er1
	er1 = subprocess.call("sudo pip install google-api-python-client", shell=True)
	print "----------------------install google-api-python-client %s" % er1
	er1 = subprocess.call("sudo pip install django-admin-tools", shell=True)
	print "----------------------install django-admin-tools %s" % er1
	return ""
	
def instPil():
	er1 = subprocess.call("sudo apt-get build-dep python-imaging", shell=True)
	print "----------------------build-dep python-imaging %s" % er1
	er1 = subprocess.call("sudo ln -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/", shell=True)
	print "----------------------libfreetype.so %s" % er1
	er1 = subprocess.call("sudo ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/", shell=True)
	print "----------------------libjpeg.so %s" % er1
	er1 = subprocess.call("sudo ln -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/", shell=True)
	print "----------------------libz.so %s" % er1	
	er1 = subprocess.call("sudo install PIL", shell=True)
	print "----------------------pip install PIL %s" % er1		
	return ""
	
def cloneCol_Dev():	
	er1 = subprocess.call("git clone https://github.com/Interbellum/collective_development.git", shell=True)
	print "----------------------git clone collective_development %s" % er1
	return ""
	
def create_srv_www():	
	er1 = subprocess.call("sudo mkdir /srv/www", shell=True)
	print "----------------------sudo mkdir /home/toha/leanskript/photoplus   mkdir /srv/www %s" % er1
	return ""
	
def copyPhotoplus():
	cwdJInst=""
	per=subprocess.Popen("pwd", shell=True, stdout=subprocess.PIPE)

	cwdJInst="%s" % per.stdout.readlines()
	#print "cwdJInst %s" % cwdJInst
	cwdJInst=cwdJInst[2:-4]
	#print "cwdJInst %s" % cwdJInst
	#cwdJInst=cwdJInst[:-7]
	#print "cwdJInst %s" % cwdJInst
	er1 = subprocess.call("sudo cp -r %s/collective_development/Code/photoplus /srv/www" % cwdJInst, shell=True)
	print "----------------------sudo ../photoplus   copy %s" % er1
	return ""
def webTest():	
	er1 = subprocess.call("sudo pip install coverage", shell=True)
	print "----------------------sudo pip install coverage-------------------- %s" % er1
	
	er1 = subprocess.call("sudo pip install webtest", shell=True)
	print "----------------------sudo pip install webtest--------------------- %s" % er1

	er1 = subprocess.call("sudo pip install django-webtest", shell=True)
	print "----------------------sudo pip install django-webtest-------------- %s" % er1

	er1 = subprocess.call("sudo pip install django-coverage", shell=True)
	print "----------------------sudo pip install django-coverage------------- %s" % er1
	return ""
def instGdata():	
	er1 = subprocess.call("sudo pip install gdata", shell=True)
	print "----------------------sudo pip install coverage-------------------- %s" % er1
	return ""

import sys
x=''
print("Введите, 1 то бы начать установку и 0 что бы закончить:")
x = raw_input("\x1b[3;32mВведите, y что бы начать установку и любую другую букву что бы закончить: \x1b[0m")
#x = int(raw_input ("Введите, y что бы начать установку и любую другую букву что бы закончить: "))
if x == 'y':
	y = raw_input("Как насчет apt-get update и upgrade? (О, это надо - y, ну его нафиг - n) : \x1b[0m")
	if y == 'y':
		InstallUpgrade()	
	y = raw_input("Как насчет apache? (Надо бы - y, ну его нафиг -n) : \x1b[0m")
	if y == 'y':
		installApache()
	y = raw_input("Как насчет python, с его примочками для мускула? (\x1b[3;32mставим - y, \x1b[3;31mну его нафиг -n) : \x1b[0m")
	if y == 'y':
		installPython()		
	y = raw_input("Как насчет PHP? (\x1b[3;32mставим - y, \x1b[3;31mну его нафиг -n) : \x1b[0m")
	if y == 'y':
		installPHP()
	y = raw_input("Может скланируем себе джанго из репозитория? (ставим - y, ну его нафиг -n) : \x1b[0m")
	if y == 'y':
		installClonDJ()
	y = raw_input("А устанавливать джанго будем? (ставим - y, ну его нафиг -n) : \x1b[0m")
	if y == 'y':
		instalDj()
	y = raw_input("Ну тут всё разом, гугл апи, админка и ещё одно питонорасширение? (ставим - y, ну его нафиг -n) : \x1b[0m")
	if y == 'y':
		instApiPyth()
	y = raw_input("Как насчет Python Imaging Library? там и скачка, и установка, и настройка.. (\x1b[3;32mставим - y, \x1b[3;31mну его нафиг -n) : \x1b[0m")
	if y == 'y':
		instPil()
	#webtest
	y = raw_input("Как насчет библиотек для webtest-a? там и скачка, и установка, и настройка.. (\x1b[3;32mставим - <y>, \x1b[3;31mну его нафиг -n) : \x1b[0m")
	if y == 'y':
		webTest()	
	y = raw_input("Как насчет библиотек gdata? там и скачка, и установка, и настройка.. (\x1b[3;32mставим - <y>, \x1b[3;31mну его нафиг -n) : \x1b[0m")
	if y == 'y':
		instGdata()		
		
	
	y = raw_input("Кланировать проект с мастера  будем? (\x1b[3;32mставим - y, \x1b[3;31mну его нафиг -n) : \x1b[0m")
	if y == 'y':	
		cloneCol_Dev()
	y = raw_input("Надо бы создать каталог srv_www.... (\x1b[3;32mставим - y, \x1b[3;31mну его нафиг -n) : \x1b[0m")
	if y == 'y':
		create_srv_www()
	y = raw_input("Наконец, копируем фотоплюс в созданный каталог. без  предыдущего шага может  не получится (\x1b[3;32mставим - y, \x1b[3;31mну его нафиг -n) : \x1b[0m")
	if y == 'y':
		copyPhotoplus()
	
else: print "установка прервана"

print "the end"