from django.contrib import admin

# Register your models here.
from .forms import SignUpForm, AddNewProjectForm
from .models import SignUp, Project, Stage, StageSetting, Role, Team, Plan, Schedule,Material, OrderStatus,Prototype,OrderPriority
from .models import MaterialComment, ScheduleComment, Courier, TrackingInfo, CategoryList, VendorList,ReadCommentTrack


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
	list_display = ["project_name","project_plan","business_plan","wiki_link","prototype_url","weblink_url"]
admin.site.register(Plan,PlanAdmin)

class ScheduleAdmin(admin.ModelAdmin):
	list_display = ["project_name","task_name","assigned_to","start_date","end_date"]
admin.site.register(Schedule,ScheduleAdmin)


class OrderStatusAdmin(admin.ModelAdmin):
   list_display = ["name", "status_id"]  
admin.site.register(OrderStatus, OrderStatusAdmin)

class OrderPriorityAdmin(admin.ModelAdmin):
   list_display = ["name", "priority_id"]  
admin.site.register(OrderPriority, OrderPriorityAdmin)

class MaterialAdmin(admin.ModelAdmin):
   list_display = ["project_name","order_category","order_sub_category","order_item","order_vendor",
                  "order_item_url","order_quantity","order_currency","order_unit_price","order_status",
                  "author","added_on","est_lead_time","order_priority","order_hsn"]
admin.site.register(Material, MaterialAdmin)

class PrototypeAdmin(admin.ModelAdmin):
   list_display = ["project_name","uploaded_on","pname","description","photo"]
admin.site.register(Prototype,PrototypeAdmin)

class MaterialCommentAdmin(admin.ModelAdmin):
   list_display = ["material","author","commented_on","comment"]
admin.site.register(MaterialComment,MaterialCommentAdmin)

class ScheduleCommentAdmin(admin.ModelAdmin):
   list_display = ["schedule","author","commented_on","comment"]
admin.site.register(ScheduleComment,ScheduleCommentAdmin)

class CategoryListAdmin(admin.ModelAdmin):
   list_display = ["category","sub_category"]
admin.site.register(CategoryList,CategoryListAdmin)

class VendorListAdmin(admin.ModelAdmin):
   list_display = ["vendor_name","GSTIN","address","contact_person","contact_num","website"]
admin.site.register(VendorList,VendorListAdmin)

class ReadCommentTrackAdmin(admin.ModelAdmin):
   list_display = ["user_name","order_id","project_id","read_flag"]
admin.site.register(ReadCommentTrack,ReadCommentTrackAdmin)

class CourierAdmin(admin.ModelAdmin):
   list_display = ["name","slug"]
admin.site.register(Courier, CourierAdmin)

class TrackingInfoAdmin(admin.ModelAdmin):
   list_display = ["tracking_no","courier_id","added_on","material"]
admin.site.register(TrackingInfo, TrackingInfoAdmin)

