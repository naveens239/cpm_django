from django.contrib import admin

# Register your models here.
from .forms import SignUpForm, AddNewProjectForm
from .models import SignUp,CreateNewProject

class SignUpAdmin(admin.ModelAdmin):
   list_display = ["__unicode__", "timestamp", "updated"]
   form = SignUpForm
   #class Meta:
   #     model = SignUp
admin.site.register(SignUp, SignUpAdmin)

class NewProjectAdmin(admin.ModelAdmin):
   list_display = ["project_name","project_status","project_completion"]
   form = AddNewProjectForm
admin.site.register(CreateNewProject, NewProjectAdmin)
