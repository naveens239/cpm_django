from django.shortcuts import render



# Create your views here.
def about(request):


    return render(request, "about.html",{})

def profile(request):


    return render(request, "profile.html",{})    