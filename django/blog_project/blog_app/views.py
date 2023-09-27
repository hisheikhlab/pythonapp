from django.shortcuts import render, HttpResponse, redirect
from .models import BlogPost
import datetime


# Create your views here.


def add(request):
    if request.method == 'POST':
        # if 'submit' in request:
        titl = request.POST['tt']
        desc = request.POST['ds']
        cont = request.POST['cn']
        image = request.FILES['im']
        BlogPost.objects.create(title=titl, desc=desc, Content=cont, pic=image)
        # new_blog = BlogPost.objects.create(title=title, desc= desc, content=content, pic=img)
        # new_blog.save()
        return redirect("blog")

    return render(request, 'Add blog.html')


def blog(request, blog_id):
    blog_this = BlogPost.objects.get(id=blog_id)
    return render(request, 'blog.html', {'blog': blog_this})


def home(request):
    blogs = BlogPost.objects.order_by('-date')
    return render(request, 'home.html', {'blogs': blogs})


def search(request):
    if "query" in request.GET:
        query = request.GET['query']
        results = BlogPost.objects.filter(title__icontains=query) | BlogPost.objects.filter(title__icontains=query)
        print(query)
        print(results)
        return render(request, 'searchedblogs.html', {'results': results, 'query': query})
