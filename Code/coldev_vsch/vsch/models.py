from django.db import models

class Post(models.Model):
	post_url = models.CharField(max_length=200)
	image_url = models.CharField(max_length=200)
	creation_date = models.DateTimeField('date of creation')
	renewal_date = models.DateTimeField('date of renewal')

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

	


