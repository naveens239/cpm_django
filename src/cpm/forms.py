from django import forms
from .models import SignUp,CreateNewProject

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
      model = CreateNewProject
      fields = ['project_name', 'project_status', 'project_completion'] 
    project_name = forms.CharField(required = True)
    CHOICES_status = (('Ongoing', 'Ongoing',), ('Completed', 'Completed',))
    project_status = forms.ChoiceField(widget=forms.RadioSelect, required = True, choices=CHOICES_status)
    project_completion = forms.IntegerField(required = True)
    def clean_project_completion(self):
      completion = self.cleaned_data.get('project_completion')
      if completion<0 or completion >100:
           raise forms.ValidationError("Please enter a numeric value between 0 and 100")
      return completion