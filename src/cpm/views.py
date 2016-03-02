from django.shortcuts import render, render_to_response,redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import ContactForm, SignUpForm,AddNewProjectForm
from django.core.mail import send_mail
from django.conf import settings
from .models import CreateNewProject

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
    project_data = CreateNewProject.objects.all()
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
        form_prj_name = form.cleaned_data.get("project_name")
        form_prj_status = form.cleaned_data.get("project_status")
        form_prj_completion = form.cleaned_data.get("project_completion")
        form.save()
        project_data = CreateNewProject.objects.all()
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
