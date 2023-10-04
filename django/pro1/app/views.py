import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
import os
from django.conf import settings
from app.models import NewData, UserTable
import jwt
from datetime import date
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView


def default(request):
    if request.user.is_authenticated:
        return redirect('users', user_id=jwt.encode({'id': request.user.id}, "secret", algorithm="HS256"))
    else:
        return render(request, 'login.html')


def log(request):
    if request.user.is_authenticated:
        return redirect('users', user_id=jwt.encode({'id': request.user.id}, "secret", algorithm="HS256"))
    if request.method == 'POST':
        if 'log' in request.POST:
            usr = request.POST['user']
            pas = request.POST['pas']
            user = authenticate(request, username=usr, password=pas)
            if user is not None:
                login(request, user)
                return redirect('users', user_id=jwt.encode({'id': request.user.id}, "secret", algorithm="HS256"))
            elif user is None:
                # return HttpResponse("No user found")
                return render(request, 'login.html', {'no_u': f"Username or password incorrect"})
    return render(request, 'login.html')


def is_valid_password(password):
    pattern = r'(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}'
    return bool(re.match(pattern, password))

def reg(request):
    if request.user.is_authenticated:
        return redirect('users', user_id=jwt.encode({'id': request.user.id}, "secret", algorithm="HS256"))
    if request.method == 'POST':
        if 'signup' in request.POST:
            fr = request.POST['first']
            ls = request.POST['last']
            usr = request.POST['user']
            pas = request.POST['pas']
            em = request.POST['em']
            checkem = User.objects.filter(email=em).first()
            if checkem is not None:
                pass
                return render(request, 'signup.html', {'checkem': f'Email {em} is already registered'})
            elif not is_valid_password(pas):
                return render(request, 'signup.html', {
                    'checku': 'Invalid password. Password must be at least 8 characters long and contain at least one uppercase letter and one special character.'})
            else:
                try:
                    u = User.objects.create_user(first_name=fr,
                                                 last_name=ls,
                                                 username=usr,
                                                 password=pas,
                                                 email=em,
                                                 is_active=False)
                    u.save()
                    enc = jwt.encode({"id": str(u.pk)}, "secret", algorithm="HS256")
                    # print(request.META['HTTP_HOST'])
                    # actvation_link = request.scheme + '://' + request.META['HTT_HOST'] + activate + '/' + str(u.pk) + '/'
                    activation_link = 'http://127.0.0.1:8000/activate/' + enc + '/ '
                    activation_msg = EmailMessage("Account Creation",
                                                  f"Hi {fr},\n"
                                                  f"Thanks for signing up onto TODO LIST."
                                                  f" Your account has been successfully created.\n"
                                                  f"Click this link to activate your account:\n"
                                                  f"{activation_link}",
                                                  'zunair323@gmail.com',
                                                  [em], )
                    activation_msg.send()
                    return render(request, 'login.html', {'no_u': f'Activation link sent to your email'})
                    # user = authenticate(request, username=usr, password=pas)
                    # if user is not None:
                    #     login(request, user)
                    #     return redirect('users', user_id=user.id)
                except:
                    return render(request, 'signup.html', {'checku': f'Username {usr} is already taken'})
    return render(request, 'signup.html')


def logo(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/login/')
def todo(request, user_id):
    try:
        dec_id = jwt.decode(user_id, "secret", algorithms=["HS256"])
        if dec_id['id'] == request.user.id:
            date_today = date.today()
            if request.method == 'POST':
                if 'add task' in request.POST:
                    pr = request.POST['pr']
                    tk = request.POST['tk']
                    dt = request.POST['dt']
                    print(dt)
                    NewData.objects.create(priority=pr, task=tk, due=dt, user=request.user)
                    print("created")
                elif 'delete' in request.POST:
                    todo_del_id = request.POST['s_id']
                    todo_del = NewData.objects.get(pk=todo_del_id)
                    todo_del.delete()
                elif 'task_id' in request.POST:
                    comp_id = request.POST['task_id']
                    comp = NewData.objects.get(pk=comp_id)
                    comp.completed = not comp.completed
                    comp.save()
                return redirect('users', user_id=jwt.encode({'id': request.user.id}, "secret", algorithm="HS256"))
            todos = NewData.objects.filter(user=request.user)
            sort_by = request.GET.get('sort', 'due')
            if sort_by == 'completed':
                sorted_todos = todos.order_by('completed')
            elif sort_by == 'task':
                sorted_todos = todos.order_by('task')
            elif sort_by == 'priority':
                sorted_todos = todos.order_by('priority')
            elif sort_by == 'due':
                sorted_todos = todos.order_by('due')
            else:
                sorted_todos = todos.order_by('completed')
            return render(request, "tem.html", {'todos': sorted_todos, 'date_today': date_today, })
        else:
            return redirect("logout")
    except:  # return HttpResponse("Error")
        return redirect("logout")


def activate(request, new_id):
    dec = jwt.decode(new_id, "secret", algorithms=["HS256"])
    new_user = User.objects.get(pk=int(dec['id']))
    new_user.is_active = True
    new_user.save()
    return render(request, 'login.html', {'no_u': f'Welcome, New account activated for {new_user.email}'})
    # return redirect('users', user_id=new_id)


# def customPasswordResetView(PasswordResetView):
