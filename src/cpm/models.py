from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image

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
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()

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
	project_plan = models.URLField(max_length=1000,blank=True)
	business_plan = models.URLField(max_length=1000,blank=True)
	wiki_link = models.URLField(max_length=1000,blank=True)
	prototype_url = models.URLField(max_length=1000,blank=True)
	weblink_url = models.URLField(max_length=1000,blank=True)
	def __unicode__(self):
		return str(self.id)

class Schedule(models.Model):
	project_name = models.ForeignKey('Project',unique=False)
	task_name = models.CharField(max_length=500, blank=False, null=False)
	assigned_to = models.ForeignKey('Role')
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	def __unicode__(self):
		return str(self.id)

class OrderStatus(models.Model):	
	name = models.CharField(max_length=50, blank=False, null=False)
	status_id = models.IntegerField(blank=False, null=False)
	def __unicode__(self):
		return str(self.name)

class OrderPriority(models.Model):	
	name = models.CharField(max_length=50, blank=False, null=False)
	priority_id = models.IntegerField(blank=False, null=False)
	def __unicode__(self):
		return str(self.name)

class Material(models.Model):
	project_name = models.ForeignKey('Project',unique=False)
	order_category = models.CharField(max_length=500, blank=False, null=False)
	order_sub_category = models.CharField(max_length=500, blank=False, null=False)
	order_item = models.CharField(max_length=500, blank=False, null=False)
	order_vendor = models.CharField(max_length=500,blank=True, null=True,default='Amazon')
	order_item_url = models.URLField(max_length=1000)
	order_quantity =  models.IntegerField(validators=[MaxValueValidator(250),MinValueValidator(1)])
	order_currency = models.CharField(max_length=5,blank=True, null=True,default='Rs')
	order_unit_price = models.DecimalField(max_digits=6, decimal_places=2,validators=[MinValueValidator(0)])
	order_status = models.ForeignKey('OrderStatus')
	author = models.CharField(max_length=200,blank=False)
	added_on = models.DateTimeField(auto_now_add = False, auto_now = True)
	est_lead_time = models.CharField(max_length=10,blank=False)
	order_priority = models.ForeignKey('OrderPriority',null=False,blank=False)
	order_hsn = models.CharField(max_length=15, blank=True)

class Prototype(models.Model):
	project_name = models.ForeignKey('Project',unique=False)
	pname = models.CharField(max_length=200)
	description = models.CharField(max_length=500)
	uploaded_on = models.DateTimeField(auto_now_add = False, auto_now = True)
	photo = models.ImageField(upload_to='photo')

class MaterialComment(models.Model):
	material = models.ForeignKey('Material',unique=False)
	author = models.CharField(max_length=200,blank=False)
	commented_on = models.DateTimeField(auto_now_add = False, auto_now = True)
	comment = models.CharField(max_length=2000,blank=False)

class ScheduleComment(models.Model):
	schedule = models.ForeignKey('Schedule',unique=False)
	author = models.CharField(max_length=200,blank=False)
	commented_on = models.DateTimeField(auto_now_add = False, auto_now = True)
	comment = models.CharField(max_length=2000,blank=False)

class CategoryList(models.Model):
	category = models.CharField(max_length=200,blank=True)
	sub_category = models.CharField(max_length=200,blank=True)
	def __unicode__(self):
		return str(self.category)

class VendorList(models.Model):
    vendor_name = models.CharField(max_length=200,blank=True)
    GSTIN = models.CharField(max_length=200,blank=True,null=True)
    address = models.CharField(max_length=200,blank=True,null=True)
    contact_person = models.CharField(max_length=200,blank=True,null=True)
    contact_num = models.IntegerField(blank=True,null=True)
    website = models.URLField(blank=True,null=True)

class ReadCommentTrack(models.Model):
	user_name = models.CharField(max_length=200,blank=False)
	order_id = models.IntegerField(blank=False,null=False)
	project_id = models.IntegerField(blank=False,null=False)
	read_flag = models.CharField(max_length=1,blank=False,default="N")

class Courier(models.Model):
	name = models.CharField(max_length=200,blank=True)
	slug = models.CharField(max_length=200,blank=True)
	def __unicode__(self):
		return str(self.name)

class TrackingInfo(models.Model):
	tracking_no = models.CharField(max_length=50,blank=True)
	courier_id  = models.ForeignKey('Courier',unique=False)
	added_on = models.DateTimeField(auto_now_add = False, auto_now = True)
	material = models.ForeignKey('Material',unique=False)



