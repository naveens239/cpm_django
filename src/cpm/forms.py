from django import forms
from django.db import models
from .models import SignUp,Project,Stage,StageSetting,Team,Role,Plan


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
      fields = ["project_plan","business_plan","wiki_link"]
