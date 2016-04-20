from django.shortcuts import render, render_to_response,redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import ContactForm, SignUpForm,AddNewProjectForm,ProjectStageForm,TeamAddForm,TeamEditForm
from .forms import ProjectPlanForm,ScheduleForm,ScheduleEditForm, MaterialForm, PrototypeForm, ScheduleCommentForm, MaterialCommentForm
from django.core.mail import send_mail
from django.conf import settings
from .models import Project, Stage, StageSetting, Team, Role,Plan, Schedule, Material, OrderStatus, Prototype, ScheduleComment, MaterialComment
import json, ast, datetime



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
    message=""
    if form.is_valid():
        name = form.cleaned_data.get("name")
        start_date = form.cleaned_data.get("start_date")
        end_date = form.cleaned_data.get("end_date")
        # for key in form.cleaned_data:
        #     print key
        #     print form.cleaned_data.get(key)
        # form_prj_name = form.cleaned_data.get("name")
        # form_prj_status = form.cleaned_data.get("status")
        # form_prj_completion = form.cleaned_data.get("completion")
        # form.save()
        project_data = Project.objects.all()
      
        p = Project(name=name,status="Ongoing",completion = 0,start_date=start_date,end_date=end_date)
        if start_date > end_date:
            message = "Project End date cannot be earlier than Start date"
        else:
            message = "Project Added Successfully"
            p.save()
        context={
            "form":project_data,
            "message":message,               
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
    try:
      team_data = None
      team_data = Team.objects.filter(project_name=project_data.id)
    except Team.DoesNotExist:
       team_data = None
    context={
        "project_data":project_data,
        "team_data":team_data,
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
                id_ = team_edit_form.cleaned_data.get("model_instance")
                #team = Team.objects.get(pk=id)
                print'Name issss',id_
                item_data = Team.objects.get(id=id_)
                item_data.member_name = team_edit_form.cleaned_data.get("member_name")
                item_data.member_role = Role.objects.get(id=team_edit_form.cleaned_data.get("role_name"))
                item_data.save()
            except Team.DoesNotExist:
                print 'in hrerer except'
                p = Team(project_name=project_data,member_name=member_name,role_name=member_role)
                p.save()    

   if request.method=='POST' and 'delete' in request.POST:
                id_ = request.POST.get('model_instance')

                print'Name issss',id_
                item_data = Team.objects.get(id=id_)
                item_data.delete()
  

   form_stage = ProjectStageForm(request.POST or None)
   team_add_form = TeamAddForm(request.POST or None)
   team_edit_form = TeamEditForm(request.POST or None)
   print 'here before try'
   try:
       print 'here inside try'
       team_data = None
       project_stage_data = None
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
      print request.POST
      project_data = Project.objects.get(name=name)
      role_data = Role.objects.all()
      order_status_data = OrderStatus.objects.all()
      task_message = ""
      plan_message = ""
      order_message = ""
      prototype_message =""
      if request.method=='POST' and 'plan' in request.POST:
        plan_form = ProjectPlanForm(request.POST or None)
        if plan_form.is_valid():
            project_plan = plan_form.cleaned_data.get("project_plan")
            business_plan = plan_form.cleaned_data.get("business_plan")
            wiki_link = plan_form.cleaned_data.get("wiki_link")
            prototype_url = plan_form.cleaned_data.get("prototype_url")
            weblink_url = plan_form.cleaned_data.get("weblink_url")
            try:               
                p = Plan.objects.get(project_name=project_data.id)
                p.project_plan = project_plan
                p.business_plan = business_plan
                p.wiki_link = wiki_link
                p.prototype_url = prototype_url
                p.weblink_url = weblink_url
                p.save()    
                if not project_plan and not business_plan and not wiki_link:
                  p.delete()
                plan_message="Plan Updated Successfully"
            except Plan.DoesNotExist:
                p = Plan(project_name=project_data,project_plan=project_plan,
                  business_plan=business_plan,wiki_link=wiki_link,prototype_url=prototype_url,weblink_url=weblink_url)
                p.save()
                plan_message="Plan Added Successfully"
       
      if request.method=='POST' and 'schedule_save' in request.POST:
         schedule_form = ScheduleForm(request.POST or None)
         print request.POST
         print 'hererere in task 11111'

         if schedule_form.is_valid():   
            print 'hererere in task 2222'
            task_name = schedule_form.cleaned_data.get('task_name')
            assigned_id = schedule_form.cleaned_data.get('assigned_to')
            start_date = schedule_form.cleaned_data.get('start_date')
            end_date = schedule_form.cleaned_data.get('end_date')
            role_assigned_to = Role.objects.get(id=assigned_id)     
            p = Schedule(project_name=project_data,assigned_to=role_assigned_to,start_date=start_date,end_date=end_date,task_name=task_name)
            if p.end_date < p.start_date:
               task_message="Task End date cannot be earlier than Start date"   
            else:
               p.save()
               task_message="Task Added Successfully"
         else:
            print 'errror in herereeeee'
            print request.method
            task_message="Task could not be added"
            print schedule_form.errors
      
      if request.method=='POST' and 'schedule_edit' in request.POST:
         schedule_edit_form = ScheduleEditForm(request.POST or None)
         print request.POST

         if schedule_edit_form.is_valid():   

            task_name = schedule_edit_form.cleaned_data.get('task_name')
            assigned_id = schedule_edit_form.cleaned_data.get('assigned_to')
            start_date = schedule_edit_form.cleaned_data.get('start_date')
            end_date = schedule_edit_form.cleaned_data.get('end_date')
            id_ = schedule_edit_form.cleaned_data.get("model_instance")
            print 'before try !!!!!!!'
            try:
               p = Schedule.objects.get(id=id_)
               if task_name:
                  p.task_name = task_name
               if assigned_id:
                  p.assigned_to = Role.objects.get(id=assigned_id)
               if start_date:
                  p.start_date = start_date
               else:
                  p.start_date = p.start_date.date()   
               if end_date:
                  p.end_date = end_date
               else:
                  p.end_date = p.end_date.date()   
               if p.end_date < p.start_date:
                  task_message="Task End date cannot be earlier than Start date"   
               else:
                  p.save()
                  task_message="Task Updated Successfully"
            except Schedule.DoesNotExist:
               role_assigned_to = Role.objects.get(id=assigned_id)     
               p = Schedule(project_name=project_data,assigned_to=role_assigned_to,start_date=start_date,end_date=end_date,task_name=task_name)
               p.save()
               task_message="Task Updated Successfully"
         else:
            print 'errror in herereeeee'
            print request.method
            task_message="Task Update Not Successful"
            print 'something went wrong !!!!!!!!'   
      
      if request.method=='POST' and 'schedule_comment' in request.POST:
         schedule_comment_form = ScheduleCommentForm(request.POST or None)
         print request.POST

         if schedule_comment_form.is_valid():   

            author = schedule_comment_form.cleaned_data.get('author')
            print 'author is',author
            comment = request.POST.get('comment_detail')
            print 'comment is',comment
            id_ = schedule_comment_form.cleaned_data.get("model_instance")

            schedule = Schedule.objects.get(id=id_)     
            p = ScheduleComment(schedule=schedule,comment=comment,author=author)
            if comment :
                p.save()
            else:
               task_message="Comment could not be added"
         else:
            print 'errror in herereeeee'
            print request.method
            task_message="Comment could not be added"
            print schedule_comment_form.errors

      if request.method=='POST' and 'order_comment' in request.POST:
         material_comment_form = MaterialCommentForm(request.POST or None)
         print request.POST

         if material_comment_form.is_valid():   

            author = material_comment_form.cleaned_data.get('author')
            print 'author is',author
            comment = request.POST.get('comment_detail')
            print 'comment is',comment
            id_ = material_comment_form.cleaned_data.get("model_instance")

            material = Material.objects.get(id=id_)     
            p = MaterialComment(material=material,comment=comment,author=author)
            if comment :
                p.save()
            else:
               order_message="Comment could not be added"
         else:
            print 'errror in herereeeee'
            print request.method
            order_message="Comment could not be added"
            print material_comment_form.errors

      if request.method=='POST' and 'schedule_delete' in request.POST:
                id_ = request.POST.get('model_instance')
                print'Name issss',id_
                schedule_data = Schedule.objects.get(id=id_)
                schedule_data.delete()
                task_message="Task Deleted Successfully"
      
      if request.method=='POST' and 'material_save' in request.POST:
         material_form = MaterialForm(request.POST or None)
         print request.POST
         print 'hererere in order 11111'
         if material_form.is_valid():   
            print 'hererere in order 2222'
            order_category = material_form.cleaned_data.get('order_category')
            order_sub_category = material_form.cleaned_data.get('order_sub_category')
            order_item = material_form.cleaned_data.get('order_item')
            order_item_url = material_form.cleaned_data.get('order_item_url')
            order_quantity = material_form.cleaned_data.get('order_quantity')
            order_unit_price = material_form.cleaned_data.get('order_unit_price')
            order_status = OrderStatus.objects.get(status_id=100)
            p = Material(project_name=project_data,order_category=order_category,\
                          order_sub_category=order_sub_category,order_item=order_item,\
                          order_item_url=order_item_url,order_quantity=order_quantity,\
                          order_unit_price=order_unit_price, order_status=order_status)
            p.save()
            order_message="Order Placed Successfully"
         else:
            print 'errror in herereeeee'
            print request.method
            oder_message="Order could not be placed"
            print material_form.errors
     
      if request.method=='POST' and 'order_edit' in request.POST:
         material_form = MaterialForm(request.POST or None)
         print request.POST

         if material_form.is_valid():   

            item = material_form.cleaned_data.get('order_item')
            print 'item is', item 
            category = material_form.cleaned_data.get('order_category')
            sub_category = material_form.cleaned_data.get('order_sub_category')
            quantity = material_form.cleaned_data.get('order_quantity')
            price = material_form.cleaned_data.get('order_unit_price')
            url = material_form.cleaned_data.get('order_item_url')
            id_ = request.POST.get("model_instance")
            status_id = request.POST.get('order_status')
            print 'status_id is ',status_id
            print 'model  is ',id_
            print 'before try !!!!!!!'
            try:
                p = Material.objects.get(id=id_)
                if item:
                  p.order_item = item
                if category:
                  p.order_category = category
                if sub_category:
                  p.order_sub_category = sub_category
                if quantity:
                  p.order_quantity = quantity
                if price:
                  p.order_unit_price = price
                if url:
                  p.order_item_url = url

                p.save()
                order_message="Order Updated Successfully"
            except Material.DoesNotExist:
                status = OrderStatus.objects.filter(status_id = int(status_id))
                p = Material(project_name=project_data,order_category=category,\
                          order_sub_category=sub_category,order_item=item,\
                          order_item_url=url,order_quantity=int(quantity),\
                          order_unit_price=float(price), order_status=status)
                p.save()
                order_message="Order Updated Successfully"
         else:
            print 'errror in herereeeee'
            print request.method
            order_message="Order Update Not Successful"
            print 'something went wrong !!!!!!!!'   

      if request.method=='POST' and 'order_delete' in request.POST:
          id_ = request.POST.get('model_instance')
          print'Name issss',id_
          material_data = Material.objects.get(id=id_)
          material_data.delete()
          order_message="Order Deleted Successfully"
      
      if request.method=='POST' and 'prototype_save' in request.POST:
          prototype_form = PrototypeForm(request.POST, request.FILES)
          print 'method is post',request.POST
          print 'these are the files', request.FILES

          if prototype_form.is_valid():   
            print' this form is valid'
            pname = prototype_form.cleaned_data.get('pname')
            photo = request.FILES['photo']
            description = prototype_form.cleaned_data.get('description')
            print 'photo is ', photo
            p = Prototype(project_name=project_data,pname=pname,photo=photo,description=description)     
            print 'image is ', p.photo
            p.save()
            prototype_message="Photo Uploaded Successfully"      
          else:
            print 'errror in herereeeee'
            print request.method
            prototype_message="Photo could not be uploaded"
            print prototype_form.errors
      if request.method=='POST' and 'delete_photo' in request.POST:
          id_ = request.POST.get('model_instance')
          print'photo issss',id_
          prototype_data = Prototype.objects.get(id=id_)
          prototype_data.delete()
          #message="Order Deleted Successfully"
      try:
         project_plan_data = None
         project_plan_data = Plan.objects.get(project_name=project_data.id)
      except Plan.DoesNotExist:
         project_plan_data = None   
      try:
         order_data = None
         order_data = Material.objects.filter(project_name=project_data.id)
      except Material.DoesNotExist:
         order_data = None
      try:
         schedule_data = None
         schedule_data = Schedule.objects.filter(project_name=project_data.id)
      except Schedule.DoesNotExist:
         schedule_data = None
      try:   
         prototype_data = None
         prototype_data = Prototype.objects.filter(project_name=project_data.id)
      except Prototype.DoesNotExist:
         prototype_data = None

      plan_form = ProjectPlanForm(request.POST or None)
      schedule_form = ScheduleForm(request.POST or None)
      schedule_edit_form = ScheduleEditForm(request.POST or None)
      schedule_comment_form = ScheduleCommentForm(request.POST or None)
      material_comment_form = MaterialCommentForm(request.POST or None)
      material_form = MaterialForm(request.POST or None)
      prototype_form = PrototypeForm(request.POST or None)
      context = {
         "project_data":project_data,
         "project_plan_data":project_plan_data,
         "plan_form":plan_form,
         "schedule_form":schedule_form,
         "schedule_edit_form":schedule_edit_form,
         "material_form":material_form,
         "schedule_data":schedule_data,
         "task_message":task_message,
         "plan_message":plan_message,
         "order_message":order_message,
         "order_data":order_data,
         "order_status_data":order_status_data,
         "prototype_form":prototype_form,
         "prototype_message":prototype_message,
         "prototype_data":prototype_data,
         "schedule_comment_form":schedule_comment_form,
         "material_comment_form":material_comment_form,
      }
      return render(request,"project/details/base.html",context)
      