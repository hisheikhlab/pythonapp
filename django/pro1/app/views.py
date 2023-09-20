from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
import time

import os
from django.conf import settings
from app.models import NewData, UserTable


def log(request):
    if request.user.is_authenticated:
        return redirect('users', user_id=request.user.id)
    if request.method == 'POST':
        if 'log' in request.POST:
            usr = request.POST['user']
            pas = request.POST['pas']
            user = authenticate(request, username=usr, password=pas)
            if user is not None:
                login(request, user)
                return redirect('users', user_id=user.id)
            elif user is None:
                # return HttpResponse("No user found")
                return render(request, 'login.html', {'no_u': f"Username or password incorrect"})
    return render(request, 'login.html')


def reg(request):
    if request.user.is_authenticated:
        return redirect('users', user_id=request.user.id)
    if request.method == 'POST':
        if 'signup' in request.POST:
            fr = request.POST['first']
            ls = request.POST['last']
            usr = request.POST['user']
            pas = request.POST['pas']
            em = request.POST['em']
            checkem = User.objects.filter(email=em).first()
            if checkem is not None:
                return render(request, 'signup.html', {'checkem': f'Email {em} is already registered'})
            else:
                try:
                    u = User.objects.create_user(first_name=fr,
                                                 last_name=ls,
                                                 username=usr,
                                                 password=pas,
                                                 email=em,
                                                 is_active=True)
                    u.save()
                    user = authenticate(request, username=usr, password=pas)
                    if user is not None:
                        login(request, user)
                        return redirect('users', user_id=user.id)
                except:
                    return render(request, 'signup.html', {'checku': f'Username {usr} is already taken'})
    return render(request, 'signup.html')


def logo(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/login/')
def todo(request, user_id):
    if request.method == 'POST':
        if 'add' in request.POST:
            pr = request.POST['pr']
            tk = request.POST['tk']
            dt = request.POST['dt']
            NewData.objects.create(priority=pr, task=tk, due=dt, user=request.user)
        elif 'delete' in request.POST:
            todo_del_id = request.POST['s_id']
            todo_del = NewData.objects.get(pk=todo_del_id)
            todo_del.delete()
        elif 'task_id' in request.POST:
            comp_id = request.POST['task_id']
            comp = NewData.objects.get(pk=comp_id)
            comp.completed = not comp.completed
            comp.save()
        return redirect('users', user_id=request.user.id)
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
    return render(request, "tem.html", {'todos': sorted_todos})
