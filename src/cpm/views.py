from django.shortcuts import render, render_to_response,redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import ContactForm, SignUpForm,AddNewProjectForm,ProjectStageForm,TeamAddForm,TeamEditForm, ProjectPlanForm
from django.core.mail import send_mail
from django.conf import settings
from .models import Project, Stage, StageSetting, Team, Role,Plan
import json, ast

# Create your views here.
def home(request):
    title = "Sign Up Now"
    # if request.user.is_authenticated():
         # title = "Welcome %s" %(request.user)
    form = SignUpForm(request.POST or None)
    context = {
        "title": title,
        "form" : form
    }
   
    if form.is_valid():
        form.save()
        #instance=form.save(commit=False)

        #instance.save()

        context = {
           "title": "Thank you"
        }
    if request.user.is_authenticated() and request.user.is_staff:
        context={
            "queryset":[123,456]
        }    
    return render(request, "home.html",context)


def contact(request):
    title = 'Contact Us'
    title_align_center  = True
    form = ContactForm(request.POST or None)
    if form.is_valid():
        # for key in form.cleaned_data:
        #     print key
        #     print form.cleaned_data.get(key)
        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        form_first_name = form.cleaned_data.get("first_name")
        #print form.cleaned_data
        subject = 'Site contact form'
        from_email = settings. EMAIL_HOST_USER
        to_email = [from_email,'nbengt14@gmail.com']
        email_message =  "%s : %s via %s"%(
            form_first_name,
            form_message,
            form_email)
        send_mail(subject,
         email_message,
         from_email,
         to_email,
         fail_silently= False)
    context = {
        "form" : form,
        "title": title,
        "title_align_center":title_align_center,
    }
    return render(request, "forms.html", context)

# Create your views here.
def about(request):


    return render(request, "about.html",{})

def profile(request):
    project_data = Project.objects.all()
    context={
            "form":project_data
        }

    return render(request, "profile.html",context)    
def addproject(request):
    #print request.POST
    title = 'Add New Project'
    title_align_center  = True
    form = AddNewProjectForm(request.POST or None)
    
    if form.is_valid():

        # for key in form.cleaned_data:
        #     print key
        #     print form.cleaned_data.get(key)
        # form_prj_name = form.cleaned_data.get("name")
        # form_prj_status = form.cleaned_data.get("status")
        # form_prj_completion = form.cleaned_data.get("completion")
        # form.save()
        project_data = Project.objects.all()
      
        p = Project(name=form.cleaned_data.get("name"),status="Ongoing",completion = 0,start_date=start_date,end_date=end_date)
        p.save()
        context={
            "form":project_data               
        }
        return redirect('/profile/',context) 
        print'form data', form
    context = {
        "form" : form,
        "title": title,
        "title_align_center":title_align_center,
    }
    return render(request, "forms.html", context)

def projectoverview(request,name):
    print request.POST
    print name
    project_data = Project.objects.get(name=name)
    context={
        "project_data":project_data
    }
    
    return render(request,"project_overview.html",context)

def projectsettings(request,name):
    
   if '/' in name:
        name, rest = name.split("/")
   project_data = Project.objects.get(name=name)
   stage_data = Stage.objects.all()
   role_data = Role.objects.all()
   print 'hereeee', request.POST
   #print 'get data',request.GET
   if request.method=='POST' and 'stage' in request.POST:
        form_stage = ProjectStageForm(request.POST or None)
        if form_stage.is_valid():
            print 'form is valid - ^^^^^^^^^^^^^^^^^^'
            list = request.POST.getlist('stage_item')
            list = ast.literal_eval(json.dumps(list))
            check_list  = list
            checked_items=check_list
            print 'checked_items',checked_items
            project_completion = int(round((float(len(checked_items))/len(stage_data))*100.0))
            if project_completion == 100:
                project_status = "Completed"
            else:
                project_status = "Ongoing"
            try:
                print'in herere'
                p = StageSetting.objects.get(project_name=project_data.id)
                print 'p is ',p.checked_items
                p.checked_items = checked_items
                p.total_true_checks = len(checked_items)
                project_data.completion=project_completion
                project_data.status = project_status
                project_data.save()
                p.save()    
            except StageSetting.DoesNotExist:
                print 'in hrerer except'
                p = StageSetting(project_name=project_data,total_true_checks=len(checked_items),checked_items=checked_items)
                project_data.completion=project_completion
                project_data.status = project_status
                project_data.save()
                p.save()    
        else:
            print request.method
            print form_stage.errors
            print 'something went wrong !!!!!!!!'   
 
   if request.method=='POST' and 'save' in request.POST:
         team_add_form = TeamAddForm(request.POST or None)
         if team_add_form.is_valid():
            print 'teammmmm', request.POST
            role_id = team_add_form.cleaned_data.get("role_name")
            member_name = team_add_form.cleaned_data.get("member_name")
            print'in herere'
            role= Role.objects.get(id=role_id)
            print 'role is ', role.name
            p = Team(project_name=project_data,member_name=member_name,member_role=role)
            p.save() 
                # p = Team.objects.get(project_name=project_data.id)
                # p.member_name = member_name
                # p.role_name = role_name
                # p.project_name = 
                # p.save()    
   if request.method=='POST' and 'edit' in request.POST:
          team_edit_form = TeamEditForm(request.POST or None)
          
          if team_edit_form.is_valid():
            try:
               # list = request.POST.getlist('stage_item')
               # list = ast.literal_eval(json.dumps(list))
                id = team_edit_form.cleaned_data.get("model_instance")
                #team = Team.objects.get(pk=id)
                print'Name issss',id
                item_data = Team.objects.get(id=id)
                item_data.member_name = team_edit_form.cleaned_data.get("member_name")
                item_data.member_role = Role.objects.get(id=team_edit_form.cleaned_data.get("role_name"))
                item_data.save()
            except Team.DoesNotExist:
                print 'in hrerer except'
                p = Team(project_name=project_data,member_name=member_name,role_name=member_role)
                p.save()    

   if request.method=='POST' and 'delete' in request.POST:
                id = request.POST.get('model_instance')

                print'Name issss',id
                item_data = Team.objects.get(id=id)
                item_data.delete()
  

   form_stage = ProjectStageForm(request.POST or None)
   team_add_form = TeamAddForm(request.POST or None)
   team_edit_form = TeamEditForm(request.POST or None)
   try:
       
       project_stage_data = StageSetting.objects.get(project_name=project_data.id)
       team_data = Team.objects.filter(project_name=project_data.id)
       print 'team_data', team_data
       print 'pre checked items',project_stage_data.checked_items
       form_stage = ProjectStageForm(initial={'stage_item': project_stage_data.checked_items})
   except StageSetting.DoesNotExist:
       project_stage_data = None
   except Team.DoesNotExist:
       team_data = None
    
   context={
        "stage_form":form_stage,
        "team_add_form":team_add_form,
        "team_edit_form":team_edit_form,
        "project_data":project_data,
        "stage_data":stage_data,
        "project_stage_data":project_stage_data,
        "team_data":team_data,
        "role_data":role_data,
   }
    
   return render(request,"project_settings.html",context)

def projectdetails(request,name):
      if '/' in name:
            name, rest = name.split("/")
      project_data = Project.objects.get(name=name)
      if request.method=='POST' and 'stage' in request.POST:
        plan_form = ProjectPlanForm(request.POST or None)
        if plan_form.is_valid():
            project_plan = team_add_form.cleaned_data.get("project_plan")
            business_plan = team_add_form.cleaned_data.get("business_plan")
            wiki_link = team_add_form.cleaned_data.get("wiki_link")
            try:               
                p = Plan.objects.get(project_name=project_data.id)
                p.project_plan = project_plan
                p.business_plan = business_plan
                p.wiki_link - wiki_link
                p.save()    
            except Plan.DoesNotExist:
                p = Plan(project_name=project_data,project_plan=project_plan,business_plan=business_plan,wiki_link=wiki_link)
                p.save()
      try:
       
         project_plan_data = Plan.objects.get(project_name=project_data.id)
      except Plan.DoesNotExist:
         project_plan_data = None
      plan_form = ProjectPlanForm(request.POST or None)
      context = {
         "project_data":project_data,
         "project_plan_data":project_plan_data,
         "plan_form":plan_form,
      }
      return render(request,"project_details.html",context)