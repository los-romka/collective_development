from django.db import models

class Post(models.Model):
	image_url = models.CharField(max_length=200)
	renew = models.DateTimeField('date of renewal')

	def __unicode__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=200)
	posts = models.ManyToManyField(Post)

	def __unicode__(self):
		return self.name


class Album(models.Model):
	name = models.CharField(max_length=200)
	tags = models.ManyToManyField(Tag)

	def __unicode__(self):
		return self.name


class Admin(models.Model):
	login = models.CharField(max_length=200)
	hashpass = models.CharField(max_length=200)
	renew = models.DateTimeField('date of total renewal')