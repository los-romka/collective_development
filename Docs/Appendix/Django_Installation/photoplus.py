#!/usr/bin/env python
# -*- coding: latin-1 -*-
"""
frontend_album
frontend_album_tags
frontend_tag
frontend_message
frontend_order
frontend_price
frontend_author
"""
import subprocess
tables="frontend_album frontend_album_tags frontend_tag frontend_message frontend_order frontend_price frontend_author"
user="root"
file_name="photoplus"
dir_pr="/srv/www/photoplus"
def dump_tables(user, file_name):	
	er1 = subprocess.call("mysqldump -u %s -p --opt photoplus %s > %s.sql --no-create-info" % (user,tables,file_name), shell=True)
	#print "----------------------git clone collective_development %s" % er1
	return ""
def install_tables(user, file_name):	
	er1 = subprocess.call("mysql -u %s -p photoplus < %s.sql" % (user,file_name), shell=True)
	#print "----------------------git clone collective_development %s" % er1
	return ""
def bd_create(user):	
	er1 = subprocess.call("mysqladmin -u %s -p create photoplus --default-character-set=utf8 " % user, shell=True)
	#print "----------------------git clone collective_development %s" % er1
	return ""
def manage_syncdb(dir_pr):	
	er1 = subprocess.call("python %s/manage.py syncdb" % dir_pr, shell=True)
	#print "----------------------git clone collective_development %s" % er1
	return ""
def bd_drop(user):	
	er1 = subprocess.call("mysqladmin -u %s -p drop photoplus" % user, shell=True)
	#print "----------------------git clone collective_development %s" % er1
	return ""
import sys
x=''
z=''
#print("Введите, 1 то бы начать установку и 0 что бы закончить:")
#x = raw_input("\x1b[3;32mВведите, y что бы начать установку и любую другую букву что бы закончить: \x1b[0m")
#x = int(raw_input ("Введите, y что бы начать установку и любую другую букву что бы закончить: "))
x='y'
if x == 'y':
	y = raw_input("\x1b[3;32m введите <b> - что бы извлечь данные из БД, <i> - что бы установить данные в БД, <0> - что я открыл? надо бы закрыть, пока ничего не попортил: \x1b[0m")
	
	if y == 'b':
		vr_file_name=raw_input("как назвать файл  с данными? enter для photoplus :")		
		if vr_file_name != '':
			file_name=vr_file_name
		vr_user=raw_input("login mysql? enter для root :")		
		if vr_user != '':
			user=vr_user
		dump_tables(user,file_name)
		print "Если всё в порядке, то данные теперь в файле %s" % file_name
	if y == 'i':
		vr_user=raw_input("login mysql? enter для root :")		
		if vr_user != '':
			user=vr_user
		z = raw_input("\x1b[3;32m Drop-nem бд photoplus если есть ? <y> - Drop-nem <n> не, пошли дальше\x1b[0m")
		if z == 'y':
			bd_drop(user)
		z = raw_input("\x1b[3;32m Если бд photoplus не создана, надо бы создать <y> - создать <n> уже сам всё создал\x1b[0m")
		if z == 'y':
			bd_create(user)
		z = raw_input("\x1b[3;32m запустить srv/www/photoplus manage.py syncdb ? <y> - запустить, <n> нет, уже сделал сам\x1b[0m")
		
		if z == 'y':
			z = raw_input("\x1b[3;32m Enter если проект находится по адресу /srv/www/photoplus, иначе введите адрес проекта:\x1b[0m")
			if z != '':
				dir_pr=z
			manage_syncdb(dir_pr)
		z = raw_input("\x1b[3;32m Будем заливать данные, ранее сохраненные (они должны находится в той же дерриктории)? <y> - конечно <n> нет таких данных...\x1b[0m")		
		if z == 'y':				
			vr_file_name=raw_input("как назватется файл  с данными? enter для photoplus :")		
			if vr_file_name != '':
				file_name=vr_file_name
			install_tables(user,file_name)

print "Вот и всё...."