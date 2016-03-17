from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class SignUp(models.Model):
	email = models.EmailField()
	first_name = models.CharField(max_length=20, blank=False, null=False)
	last_name = models.CharField(max_length=20, blank=False, null=False)
	timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
	updated = models.DateTimeField(auto_now_add = False, auto_now = True)
	
	def __unicode__(self): # python 3 is __str__
	   return str(self.first_name+" "+self.last_name)


    
class Project(models.Model):
	name = models.CharField(max_length=50, blank=False, null=False, unique=True)
	status = models.CharField(max_length=15,blank = False,null=False)
	completion = models.IntegerField(blank=False, null=False,validators=[MaxValueValidator(100), MinValueValidator(1)])
	start_date = models.DateTimeField(auto_now_add = True, auto_now = False)
	end_date = models.DateTimeField(auto_now_add = True, auto_now = False)

	def __unicode__(self):
		return str(self.name)

class Stage(models.Model):
	stage_number = models.IntegerField(blank=False,null=False,validators=[MaxValueValidator(3),MinValueValidator(1)])
	stage_item = models.CharField(max_length = 500, blank=False, null=False, unique = True)

class StageSetting(models.Model):
	project_name = models.ForeignKey('Project')
	total_true_checks = models.IntegerField(validators=[MaxValueValidator(25),MinValueValidator(0)])
	checked_items = models.CharField(max_length=1000)
	def __unicode__(self):
		return str(self.project_name)

class Role(models.Model):
	name = models.CharField(max_length=50, blank=False, null=False)
	def __unicode__(self):
		return str(self.name)
class Team(models.Model):
	project_name = models.ForeignKey('Project',unique=False)
	member_name = models.CharField(max_length=50, blank=False, null=False)
	member_role = models.ForeignKey('Role')
	def __unicode__(self):
		return str(self.id)
class Plan(models.Model):
	project_name = models.ForeignKey('Project')
	project_plan = models.CharField(max_length=1000)
	business_plan = models.CharField(max_length=1000)
	wiki_link = models.CharField(max_length=1000)
	def __unicode__(self):
		return str(self.id)


