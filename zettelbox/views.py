from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Box, User

# Create your views here.
def index(request):
    # standard boilerplate
    try:
        user = User.objects.get(pk=request.session.get('user_id'))
        context = { 'username': user.name }
    except ObjectDoesNotExist:
        context = { 'error_message': 'please go to login to set name'}

    return render(request, 'zettelbox/index.html', context)

def create(request):
    # standard boilerplate
    try:
        user = User.objects.get(pk=request.session.get('user_id'))
        context = { 'username': user.name }
    except ObjectDoesNotExist:
        context = { 'error_message': 'please go to login to set name'}

    name = request.POST['name']
    try:
        existing_box = Box.objects.get(name=name)
    except ObjectDoesNotExist:
        yourbox = Box(name=name)
        yourbox.save()
    return HttpResponseRedirect(reverse('zettelbox:box', args=(name,)))

def box(request, box_name):
    # standard boilerplate
    try:
        user = User.objects.get(pk=request.session.get('user_id'))
        context = { 'username': user.name }
    except ObjectDoesNotExist:
        context = { 'error_message': 'please go to login to set name'}

    try:
        box = Box.objects.get(name=box_name)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:index'))

    context['box'] = box
    return render(request, 'zettelbox/box.html', context)

def login(request):
    context = {}
    return render(request, 'zettelbox/login.html', context)

def taufe(request):
    name = request.POST['name']
    single_use_user = User(name=name)
    single_use_user.save()
    request.session['user_id'] = single_use_user.id
    return HttpResponseRedirect(reverse('zettelbox:index'))
