from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab
from django.db import models
from .models import SignUp,Project,Stage,StageSetting,Team,Role,Plan, Schedule, Material,OrderPriority
from .models import Prototype, ScheduleComment, MaterialComment, CategoryList, VendorList,Courier, TrackingInfo
from django.utils import timezone




class ContactForm(forms.Form):
    first_name = forms.CharField(required = False)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Please enter your message','rows': 5,'cols': 40,'style': 'height: 7em;'}))
    def clean_email(self):
       email = self.cleaned_data.get('email')
       email_base, provider = email.split("@")
       domain, extension = provider.split(".")
       if not domain in ["gmail","yahoo"]:
           raise forms.ValidationError("Please use a valid email address")
       if not extension in ["com","edu"]:
           raise forms.ValidationError("Please use a valid email address")
       return email

class SignUpForm(forms.ModelForm):
    class Meta:
      model = SignUp
      fields = ['first_name', 'last_name', 'email']
    def clean_email(self):
       email = self.cleaned_data.get('email')
       email_base, provider = email.split("@")
       domain, extension = provider.split(".")
       if not domain in ["gmail","yahoo"]:
           raise forms.ValidationError("Please use a valid email address")
       if not extension in ["com","edu"]:
           raise forms.ValidationError("Please use a valid email address")
       return email
       
    def clean_name(self):
        first_name = self.cleaned_data.get('first_name') 
        last_name = self.cleaned_data.get('last_name')  
        if (["0-9"] in first_name) or(["0-9"] in last_name):
           raise forms.ValidationError("Please enter a valid name")
        return first_name, last_name

class AddNewProjectForm(forms.ModelForm):
    class Meta:
      model = Project
      #fields = ['name', 'status', 'completion'] 
      fields =['name','start_date','end_date']
    name = forms.CharField(required = True)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}))
    end_date =forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}))
    def clean_name(self):
      project_name = self.cleaned_data.get('name')
      characters = ["?","/","$","\\"]
      if any(char in characters for char in project_name):
        raise forms.ValidationError("Project name cannot have special characters")
      return project_name
    # def clean_date(self):
    #     start_date = cleaned_data.get("start_date")
    #     end_date = cleaned_data.get("end_date")
    #     if end_date < start_date:
    #         msg = "Project estimated end date should be greater than start date."
    #         self._errors["end_date"] = self.error_class([msg])
    #     return start_date
    #start_date =forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))
    
    # CHOICES_status = (('Ongoing', 'Ongoing',), ('Completed', 'Completed',))
    # status = forms.ChoiceField(widget=forms.RadioSelect, required = True, choices=CHOICES_status)
    # completion = forms.IntegerField(required = True) 
    
class TeamAddForm(forms.ModelForm):
  class Meta:
    model = Team
    fields=['member_name','role_name']
  role_name = forms.ChoiceField(required = True,choices = ((role.id, role.name) for role in Role.objects.all()))
  member_name = forms.CharField(required = True)

class TeamEditForm(forms.ModelForm):
  class Meta:
    model = Team
    fields=['member_name','role_name','model_instance']
  role_name = forms.ChoiceField(required = True,choices = ((role.id, role.name) for role in Role.objects.all()))
  member_name = forms.CharField(required = True)
  model_instance = forms.CharField(widget=forms.HiddenInput())

class ProjectStageForm(forms.ModelForm):
  class Meta:
      model = Stage
      fields = ['stage_item']
  #stage_item = forms.ModelMultipleChoiceField(required=False,queryset=Stage.objects.values_list('stage_item', flat=True), widget=forms.CheckboxSelectMultiple)
  #stage_item = forms.ModelMultipleChoiceField(required=False,queryset=Stage.objects.all(), widget=forms.CheckboxSelectMultiple)
  stage_item = forms.MultipleChoiceField(required = False,choices = ((sub.id, sub.stage_item) for sub in Stage.objects.all()), widget=forms.CheckboxSelectMultiple())

class ProjectPlanForm(forms.ModelForm):
  class Meta:
      model = Plan 
      fields = ["project_plan","business_plan","wiki_link","prototype_url","weblink_url"]
  project_plan = forms.URLField(required=False)
  business_plan = forms.URLField(required=False)
  wiki_link = forms.URLField(required=False)
  prototype_url = forms.URLField(required=False)
  weblink_url = forms.URLField(required=False)

class ScheduleForm(forms.ModelForm):
  class Meta:
    model = Schedule 
    fields = ["task_name","start_date","end_date"]
  assigned_to = forms.ChoiceField(required = True,choices = ((role.id, role.name) for role in Role.objects.all()))
  start_date = forms.DateField(required = True,widget=forms.DateInput(attrs={'class': 'datepick'}))
  end_date =forms.DateField(required = True, widget=forms.DateInput(attrs={'class': 'datepick'}))


class ScheduleEditForm(forms.ModelForm):
  class Meta:
    model = Schedule
    fields= ["task_name","model_instance"]
  assigned_to = forms.ChoiceField(choices = ((role.id, role.name) for role in Role.objects.all()))
  start_date = forms.DateField(required=False,widget=forms.DateInput(attrs={'class': 'datepick'}))
  end_date =forms.DateField(required=False,widget=forms.DateInput(attrs={'class': 'datepick'}))
  model_instance = forms.CharField(widget=forms.HiddenInput())


class ScheduleCommentForm(forms.ModelForm):
  class Meta:
    model = ScheduleComment
    fields= ["author","model_instance"]
  model_instance = forms.CharField(widget=forms.HiddenInput())
  # comment = forms.CharField(required=True,max_length=2000,label=("Comment:"),error_messages={'required':'My Field',})

class MaterialForm(forms.ModelForm):
  class Meta:
    model = Material 
    fields = ["order_category","order_sub_category","order_item","order_vendor","order_item_url","order_quantity","order_currency","order_unit_price"]
    # widgets = {
    #         'Category': flopforms.widgets.Input(datalist=Material.objects.all().values_list("order_category","order_category").distinct())
    #     }
  #select = forms.CharField(widget=forms.Select(choices=CHOICES))
  
  #order_category = forms.CharField(required = True, widget=forms.TextInput(attrs={ms}select=(Material.objects.all().values_list("order_category","order_category").distinct())))
  order_category = forms.ChoiceField(required = True, choices = CategoryList.objects.all().values_list("category","category").distinct())
  #order_category = forms.ChoiceField(required = True, choices = ((mat.order_category,mat.order_category) for mat in Material.objects.all().distinct()))
  #order_category = forms.CharField(required=True,max_length=500)
  order_sub_category = forms.ChoiceField(required = True, choices = CategoryList.objects.all().values_list("sub_category","sub_category").distinct())

  #order_sub_category = forms.CharField(required=True,max_length=500)
  order_item = forms.CharField(required=True,max_length=500)
  order_vendor = forms.ChoiceField(required = True, choices = VendorList.objects.all().values_list("vendor_name","vendor_name").distinct())
  order_item_url = forms.URLField(required=False,max_length=1000,help_text="Please enter the URL of the page.",initial="http://")
  order_quantity =  forms.IntegerField(required=True,  min_value=1, initial=1)
  RELEVANCE_CHOICES = (("Rs", ("Rs")),("$", ("$")))
  order_currency =  forms.ChoiceField(required=False,choices=RELEVANCE_CHOICES)
  order_unit_price = forms.DecimalField(required=False,max_digits=6, decimal_places=2, min_value=0, initial=0.00)
  est_lead_num = forms.IntegerField(required=True,  min_value=0, initial=1)
  DAY_CHOICES = (("d","day(s)"),("w", "week(s)"),("m","month(s)"))
  est_lead_days =forms.ChoiceField(required=False,choices=DAY_CHOICES)
  order_priority = forms.ChoiceField(required = True,choices = ((op.priority_id, op.name) for op in OrderPriority.objects.all()))
  order_hsn = forms.CharField(required=False,max_length=16)
  #order_status = forms.ChoiceField(required = True,choices= )
  def __init__(self, *args, **kwargs):
    super(MaterialForm, self).__init__(*args, **kwargs)
    self.fields['order_category'].label = "Category"
    self.fields['order_category'].choices = CategoryList.objects.all().values_list("category","category").distinct()
    self.fields['order_sub_category'].label = "Sub Category"
    self.fields['order_sub_category'].choices = CategoryList.objects.all().values_list("sub_category","sub_category").distinct()
    self.fields['order_item'].label = "Item"
    self.fields['order_quantity'].label = "Quantity"
    self.fields['order_currency'].label = "Currency"
    self.fields['order_unit_price'].label = "Estimated Price"
    self.fields['order_vendor'].label = "Vendor"
    self.fields['order_vendor'].choices = VendorList.objects.all().values_list("vendor_name","vendor_name").distinct()
    self.fields['order_item_url'].label = "URL to Item" 
    self.fields['est_lead_num'].label = "Est Lead Time"
    self.fields['est_lead_days'].label = " "
    self.fields['order_priority'].label = "Order Priority"
    self.fields['order_hsn'].label = "HSN Code"
    
class MaterialCommentForm(forms.ModelForm):
  class Meta:
    model = MaterialComment
    fields= ["author","model_instance"]
  model_instance = forms.CharField(widget=forms.HiddenInput())

class PrototypeForm(forms.ModelForm):
  class Meta:
    model = Prototype
    fields=["pname","description","photo"]
  pname = forms.CharField(required=True,max_length=500,label=("Picture Title:"),error_messages={'required':'My Field',})
  description = forms.CharField(required=True,max_length=500,widget=forms.Textarea,label=("Picture Description:"),error_messages={'required':'My Field',})
  photo = forms.ImageField()

class ProcessURLForm(forms.Form):
  process_link = forms.URLField(required=False,max_length=1000,help_text="Please prefix http://",initial="http://")

class OrderListingForm(forms.ModelForm):
  class Meta:
    model = CategoryList
    fields=["category_choice","category","sub_category_choice","sub_category"]
  category_choice = forms.ChoiceField(required = True, choices = CategoryList.objects.all().values_list("category","category").distinct())
  category = forms.CharField(required=False,max_length=200,label=("Category"))
  sub_category_choice = forms.ChoiceField(required = True, choices = CategoryList.objects.all().values_list("sub_category","sub_category").distinct())
  #sub_category_choice = forms.ChoiceField(required = True, choices = CategoryList.objects.all().values_list("sub_category","sub_category").distinct())
  sub_category = forms.CharField(required=False,max_length=200,label=("Sub Category"))
  def __init__(self, data=None, *args, **kwargs):
    super(OrderListingForm, self).__init__(data, *args, **kwargs)
    CAT_CHOICES = list(CategoryList.objects.all().values_list("category","category").distinct())
    CAT_CHOICES_OTHERS = [('','')] + CAT_CHOICES + [('Others','Others')]
    self.fields['category_choice'].choices = CAT_CHOICES_OTHERS
    SUB_CAT_CHOICES = list(CategoryList.objects.all().values_list("sub_category","sub_category").distinct())
    SUB_CAT_CHOICES_OTHERS = [('','')] + SUB_CAT_CHOICES + [('Others','Others')]
    self.fields['sub_category_choice'].choices = SUB_CAT_CHOICES_OTHERS
    if data and data.get('category_choice', None) == "Others":
      self.fields['category'].required = True
    if data and data.get('sub_category_choice', None) == "Others":
      self.fields['sub_category'].required = True
  #vendor = forms.CharField(required=False,max_length=200,label=("Vendor"))
 
class VendorListingForm(forms.ModelForm):
  class Meta:
     model = VendorList
     fields=['vendor_name','GSTIN','address','contact_person','contact_num',"website"]
  vendor_name = forms.CharField(required=True, max_length=200,label="Vendor Name")
  GSTIN =  forms.CharField(error_messages={'required':'Please enter a valid GSTIN'},required=False,label="GSTIN",max_length=15)
  address = forms.CharField(widget=forms.Textarea,required=False,label="Address")
  contact_person = forms.CharField(required=False,max_length=200,label="Contact Person")
  contact_num = forms.IntegerField(error_messages={'required':'Please enter a valid phone number'},required=False,min_value=0000000000,max_value=9999999999,label="Phone")
  website = forms.URLField(error_messages={'required':'Please enter a website address'},label="Website Link",required=False,help_text="Please prefix http://",initial="http://")

class ExcelForm(forms.Form):
  excel_file = forms.FileField(required=False,label="Excel File")

class TrackingForm(forms.ModelForm):
  class Meta:
    model = TrackingInfo
    fields=["tracking_number","slug"]
  tracking_number  = forms.CharField(required=False,label="Tracking No:")
  slug = forms.ChoiceField(required = False,label = "Courier",choices = ((courier.id,courier.name) for courier in Courier.objects.all()))
