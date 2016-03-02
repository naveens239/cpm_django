from __future__ import unicode_literals

from django.db import models

# Create your models here.
class SignUp(models.Model):
	email = models.EmailField()
	first_name = models.CharField(max_length=20, blank=False, null=False)
	last_name = models.CharField(max_length=20, blank=False, null=False)
	timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
	updated = models.DateTimeField(auto_now_add = False, auto_now = True)
	
	def __unicode__(self): # python 3 is __str__
	   return str(self.first_name+" "+self.last_name)

class CreateNewProject(models.Model):
	project_name = models.CharField(max_length=30, blank=False, null=False, unique=True)
	project_status = models.CharField(max_length=10,blank=False, null=False)
	project_completion = models.IntegerField(blank=False, null=False)

	def __unicode__(self):
		return str(self.project_name)