from django.shortcuts import render, render_to_response,redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import ContactForm, SignUpForm,AddNewProjectForm,ProjectStageForm,TeamAddForm,TeamEditForm, TrackingForm
from .forms import ProjectPlanForm,ScheduleForm,ScheduleEditForm, MaterialForm, PrototypeForm, ScheduleCommentForm, MaterialCommentForm, ProcessURLForm,ExcelForm
from django.core.mail import send_mail
from django.conf import settings
from .models import Project, Stage, StageSetting, Team, Role,Plan, Schedule, Material, OrderStatus, Prototype, ScheduleComment, MaterialComment
from .models import TrackingInfo, Courier
from product_details_scraper import ReadAsin
import json, ast, datetime,re
import openpyxl
import aftership as aftership

api = aftership.APIv4("8a4aab03-8132-4fae-aca8-48c054964e14")
def excel_courier_loader():
    wb = openpyxl.load_workbook("C:\Users\acer-pc\Documents\ET\my_project_folder\couriers.xlsx")
    sheet = wb.get_sheet_by_name('Sheet1')
    for row in range(2, sheet.max_row + 1):
       name = sheet['A'+str(row)].value
       slug = sheet['B'+str(row)].value
       try:
          p = Courier(name=name,slug=slug)
          p.save() 
       except Exception as e:
        print str(e)
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

def netproject(request):
    print request.POST
    try:
         material_data = None
         material_data = Material.objects.all()
    except:
         material_data = None
    context={
        "material_data":material_data,
    }
    
    return render(request,"net_project_view.html",context)

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
   try:
       team_data = None
       team_data = Team.objects.filter(project_name=project_data.id)
   except Team.DoesNotExist:
       team_data = None
   try:
       project_stage_data = None
       project_stage_data = StageSetting.objects.get(project_name=project_data.id)      
       form_stage = ProjectStageForm(initial={'stage_item': project_stage_data.checked_items})
   except StageSetting.DoesNotExist:
       project_stage_data = None

    
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
      process_message = ""
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
      
      if request.method=='POST' and 'excel_data' in request.POST:
         print 'hereeeeee'
         excel_form = ExcelForm(request.POST, request.FILES)
         
         
         print request.POST
         if excel_form.is_valid():
           print 'vaaalidddd'
           excel = request.FILES['excel_file']
           print excel
           name = excel.name
           extension=[]
           extension = name.split('.')
           print extension
           if extension[1] in ('xlsx','xls'):
             print "right extension"
             wb = openpyxl.load_workbook(excel)
             sheet = wb.get_sheet_by_name('Sheet1')
             for row in range(2, sheet.max_row + 1):
               category = sheet['A'+str(row)].value
               subcategory = sheet['B'+str(row)].value
               item = sheet['C'+str(row)].value
               vendor = sheet['D'+str(row)].value
               url = sheet['E'+str(row)].value
               quantity = sheet['F'+str(row)].value
               price = sheet['G'+str(row)].value
               status = OrderStatus.objects.get(status_id=50)
               currency = sheet['H'+str(row)].value
               print category, subcategory, item, vendor, url, quantity, price, status, currency
               try:
                  p = Material(project_name=project_data,order_category=category,\
                                order_sub_category=subcategory,order_item=item,order_vendor=vendor,\
                                order_item_url=url,order_quantity=quantity,\
                                order_currency=currency,order_unit_price=price, order_status=status)
                  p.save() 
                  order_message =  "Excel sheet successfully processed."
               except Exception as e:
                print str(e)
                order_message =  "Order number "+ str(row)+" could not be saved."

         else:
           print 'form INVALID'
           order_message = "Please upload .xls or .xlsx file only"
           print excel_form.errors


      if request.method=='POST' and 'process_url' in request.POST:
         process_url_form = ProcessURLForm(request.POST or None)
         extracted_data=[]
         print request.POST
         if process_url_form.is_valid():
            url = process_url_form.cleaned_data.get('process_link')
            extracted_data = ReadAsin(url)
            if len(extracted_data)==0:
              order_message ="Oops there has been an error. Please add order manually"
              print 'Please add order manually'
            else:
              print 'Found dataaaaaaaaaaaaa'
              try:
                  order_category = extracted_data[0]['CATEGORY']
                  order_sub_category = extracted_data[0]['SUBCATEGORY']
                  order_item = extracted_data[0]['ITEM']
                  order_vendor = extracted_data[0]['VENDOR']
                  order_item_url = extracted_data[0]['URL']
                  order_quantity = 1
                  order_unit_price = extracted_data[0]['ORIGINAL_PRICE']
                  # print 'string is',price_string
                  # match = re.search(r'([\D]+)([\d,.]+)', price_string)
                  # output = (match.group(1), match.group(2).replace(',',''))
                  # print 'output is',output[1]
                  # order_unit_price = output[1]
                  order_currency = extracted_data[0]['CURRENCY']
                  order_status = OrderStatus.objects.get(status_id=50)
                  p = Material(project_name=project_data,order_category=order_category,\
                                order_sub_category=order_sub_category,order_item=order_item,order_vendor=order_vendor,\
                                order_item_url=order_item_url,order_quantity=order_quantity,\
                                order_currency=order_currency,order_unit_price=order_unit_price, order_status=order_status)
                  p.save(),
                  order_message="Order Placed Successfully"
              except:
                order_message="Oops there has been an error. Please add order manually"

               
      if request.method=='POST' and 'material_save' in request.POST:
             material_form = MaterialForm(request.POST or None)
             print request.POST
             print 'hererere in order 11111'
             if material_form.is_valid():   
                print 'hererere in order 2222'
                order_category = material_form.cleaned_data.get('order_category')
                order_sub_category = material_form.cleaned_data.get('order_sub_category')
                order_item = material_form.cleaned_data.get('order_item')
                order_vendor = material_form.cleaned_data.get('order_vendor')
                order_item_url = material_form.cleaned_data.get('order_item_url')
                order_quantity = material_form.cleaned_data.get('order_quantity')
                order_currency = material_form.cleaned_data.get('order_currency')
                order_unit_price = material_form.cleaned_data.get('order_unit_price')
                order_status = OrderStatus.objects.get(status_id=50)
                author = request.user
                est_lead_time = str(material_form.cleaned_data.get('est_lead_num'))+material_form.cleaned_data.get('est_lead_days')
                p = Material(project_name=project_data,order_category=order_category,\
                              order_sub_category=order_sub_category,order_item=order_item,order_vendor=order_vendor,\
                              order_item_url=order_item_url,order_quantity=order_quantity,\
                              order_currency=order_currency,order_unit_price=order_unit_price,\
                              order_status=order_status,author=author,est_lead_time=est_lead_time)
                p.save()
                if order_message=="":
                    order_message="Order Placed Successfully"
             else:
                print 'errror in herereeeee'
                print request.method
                if order_message=="":
                  order_message="Order could not be placed"
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
            currency = material_form.cleaned_data.get('order_currency')
            price = material_form.cleaned_data.get('order_unit_price')
            vendor = material_form.cleaned_data.get('order_vendor')
            url = material_form.cleaned_data.get('order_item_url')
            id_ = request.POST.get("model_instance")
            status_id = request.POST.get('order_status')

            print 'status_id is ',status_id
            print 'model  is ',id_
            print 'before try !!!!!!!'
            print 'currency is', currency
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
                if currency:
                  p.order_currency = currency
                if price:
                  p.order_unit_price = price
                if url:
                  p.order_item_url = url
                if vendor:
                  p.order_vendor = vendor

                p.save(update_fields=['order_item','order_category','order_sub_category','order_quantity','order_currency','order_unit_price','order_item_url','order_vendor'])
                order_message="Order Updated Successfully"
            except Material.DoesNotExist:
                print 'in exception blck'
                status = OrderStatus.objects.filter(status_id = int(status_id))
                p = Material(project_name=project_data,order_category=category,\
                          order_sub_category=sub_category,order_item=item,\
                          order_item_url=url,order_vendor = vendor,order_quantity=int(quantity),\
                          order_currency = currency,order_unit_price=float(price), order_status=status)
                p.save()
                order_message="Order Updated Successfully"
         else:
            print 'errror in herereeeee'
            print request.method
            order_message="Order Update Not Successful"
            print material_form.errors
            print 'something went wrong !!!!!!!!'   

      if request.method=='POST' and 'order_delete' in request.POST:
          id_ = request.POST.get('model_instance')
          print'Name issss',id_
          material_data = Material.objects.get(id=id_)
          material_data.delete()
          order_message="Order Deleted Successfully"


      if request.method=='POST' and 'tracking_save' in request.POST:
          tracking_form = TrackingForm(request.POST)
          if tracking_form.is_valid():
            id_ = request.POST.get("model_instance")
            tracking_num = tracking_form.cleaned_data.get('tracking_number')
            slug_id = tracking_form.cleaned_data.get('slug')
            courier = Courier.objects.get(id=slug_id)
          print 'data is', courier.slug
          try:
             api = aftership.APIv4("8a4aab03-8132-4fae-aca8-48c054964e14")
             try:
               print api.trackings.post(tracking=dict(slug=courier.slug, tracking_number=tracking_num, title="Title"))
             except:
               print 'Tracking number already exists in API'
             print api.trackings.get(courier.slug, tracking_num)
             print api.trackings.get(courier.slug, tracking_num, fields=['tag','last_updated_at','location','updated_at','checkpoint_time','shipment_delivery_date','expected_delivery'])
             material_data = Material.objects.get(id=id_)
             track_data = TrackingInfo.objects.filter(material=material_data.id)
             print track_data
             
             # recording the tracking to database
             if track_data:
                 print "Tracking for material present"
                 track_data = TrackingInfo.objects.get(material=material_data.id)
                 track_data.tracking_no = tracking_num
                 track_data.courier_id = courier
                 track_data.save()
                 order_message="Tracking Updated Successfully"
 
             else:

                 p = TrackingInfo(tracking_no = tracking_num, courier_id = courier, material = material_data)
                 p.save()
                 order_message="Tracking Recorded Successfully"
          except Exception as e:
             print 'tracking for material doesnt exist'
             print tracking_form.errors
             print str(e) 
             order_message = "Tracking Not Found"
          #material_data = Material.objects.get(id=id_)
          #material_data.delete()
          
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
      process_url_form = ProcessURLForm(request.POST or None)
      excel_form = ExcelForm(request.POST or None)
      tracking_form = TrackingForm(request.POST or None)
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
         "process_url_form": process_url_form,
         "excel_form":excel_form,
         "tracking_form":tracking_form,
      }
      return render(request,"project/details/base.html",context)
      