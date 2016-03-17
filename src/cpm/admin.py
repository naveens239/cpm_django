from django.contrib import admin

# Register your models here.
from .forms import SignUpForm, AddNewProjectForm
from .models import SignUp, Project, Stage, StageSetting, Role, Team, Plan


class SignUpAdmin(admin.ModelAdmin):
   list_display = ["__unicode__", "timestamp", "updated"]
   form = SignUpForm
   #class Meta:
   #     model = SignUp
admin.site.register(SignUp, SignUpAdmin)

class ProjectAdmin(admin.ModelAdmin):
   list_display = ["name","status","completion","start_date","end_date"]
   form = AddNewProjectForm
admin.site.register(Project, ProjectAdmin)

class StageAdmin(admin.ModelAdmin):
   list_display = ["stage_number","stage_item"]
admin.site.register(Stage, StageAdmin)

class StageSettingAdmin(admin.ModelAdmin):
   list_display = ["project_name","total_true_checks","checked_items"]  
admin.site.register(StageSetting, StageSettingAdmin)
  
class TeamAdmin(admin.ModelAdmin):
   list_display = ["project_name","member_name","member_role"]  
admin.site.register(Team, TeamAdmin)

class RoleAdmin(admin.ModelAdmin):
   list_display = ["name"]  
admin.site.register(Role, RoleAdmin)

class PlanAdmin(admin.ModelAdmin):
	list_display = ["project_name","project_plan","business_plan","wiki_link"]
admin.site.register(Plan,PlanAdmin)