from django.shortcuts import render, HttpResponse, redirect
from .models import BlogPost, BlogImage
import random
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
import jwt


# Create your views here.


def default(request):
    if request.user.is_authenticated:
        return redirect('home', user_id=jwt.encode({'id': request.user.id}, "secret", algorithm="HS256"))
    else:
        return render(request, 'login.html')


def log(request):
    print(request.method)
    if request.user.is_authenticated:
        return redirect('home', user_id=jwt.encode({'id': request.user.id}, "secret", algorithm="HS256"))
    if request.method == 'POST':
        usr = request.POST['user']
        pas = request.POST['pas']
        user = authenticate(request, username=usr, password=pas)
        print(usr)
        if user is not None:
            login(request, user)
            return redirect('home', user_id=jwt.encode({'id': request.user.id}, "secret", algorithm="HS256"))
        elif user is None:
            return render(request, 'login.html', {"mess": "Username or password incorrect"})
    return render(request, 'login.html')


def logou(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def add(request):
    if request.method == 'POST':
        titl = request.POST['tt']
        desc = request.POST['ds']
        cont = request.POST['cn']
        new_blog = BlogPost.objects.create(title=titl, desc=desc, Content=cont, author=request.user)
        for image in request.FILES.getlist('im'):
            BlogImage.objects.create(blog=new_blog, pic=image)
        return redirect("blog", blog_id=new_blog.id)
    return render(request, 'Add blog.html')


@login_required(login_url='login')
def delete(request):
    print(request.method)
    if request.method == 'POST':
        if 'confirm_delete' in request.POST:
            # print(request.POST['confirm_delete'])
            to_delete = BlogPost.objects.get(id=request.POST['confirm_delete'])
            to_delete.delete()
            return redirect("home", user_id=jwt.encode({'id': request.user.id}, "secret", algorithm="HS256"))
    return render(request, 'Add blog.html')


@login_required(login_url='login')
def blog(request, blog_id):
    blog_this = BlogPost.objects.get(id=blog_id)
    if request.method == 'POST':
        if 'delete' in request.POST:
            return render(request, 'blog.html', {'blog': blog_this, 'deleteme': 'Yes'})
    return render(request, 'blog.html', {'blog': blog_this})


@login_required(login_url='login')
def home(request, user_id):
    dec_id = jwt.decode(user_id, "secret", algorithms=["HS256"])
    if dec_id['id'] == request.user.id:
        blogs = BlogPost.objects.order_by('-date')
        random_integer = random.randint(1, len(blogs))
        featured_blog = random.choice(blogs)
        return render(request, 'home.html', {'blogs': blogs,
                                             'featured': featured_blog,
                                             'random_integer': random_integer})
    else:
        return redirect("logout")


def signup(request):
    if request.user.is_authenticated:
        return redirect('home', user_id=jwt.encode({'id': request.user.id}, "secret", algorithm="HS256"))
    if request.method == 'POST':
        user = request.POST['user']
        em = request.POST['em']
        pas = request.POST['pas']
        try:
            new_user = User.objects.create_user(email=em, username=user, password=pas)
            new_user.save()
        except:
            return render(request, 'signup.html', {'mess':'Username already taken'})
        return redirect('login')
    return render(request, 'signup.html')


@login_required(login_url='login')
def search(request):
    if "query" in request.GET:
        query = request.GET['query']
        results = BlogPost.objects.filter(title__icontains=query) | BlogPost.objects.filter(desc__icontains=query) | BlogPost.objects.filter(Content__icontains=query)
        return render(request, 'searchedblogs.html', {'results': results, 'query': query})
    return render(request, 'searchedblogs.html')