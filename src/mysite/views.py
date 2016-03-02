from django.shortcuts import render
from cpm.models import CreateNewProject


# Create your views here.
def about(request):


    return render(request, "about.html",{})

def profile(request):
    project_data = CreateNewProject.objects.all()
    context={
            "form":project_data
        }

    return render(request, "profile.html",context)    