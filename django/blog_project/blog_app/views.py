from django.shortcuts import render, HttpResponse

# Create your views here.


def add(request):
    return render(request, 'Add blog.html')

def home(request):
    return render(request, 'main.html')