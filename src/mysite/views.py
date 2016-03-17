from django.shortcuts import render
from cpm.models import CreateNewProject


# Create your views here.
def about(request):


    return render(request, "about.html",{})
