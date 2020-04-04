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
        return HttpResponseRedirect(reverse('zettelbox:login'))

    context['exists'] = request.GET.get('exists')

    return render(request, 'zettelbox/index.html', context)

def create(request):
    # standard boilerplate
    try:
        user = User.objects.get(pk=request.session.get('user_id'))
        context = { 'username': user.name }
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:login'))

    name = request.POST['name']
    try:
        existing_box = Box.objects.get(name=name)
        exists = name
        return HttpResponseRedirect('{:s}?exists={:s}'.format(reverse('zettelbox:index'), exists))
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
        return HttpResponseRedirect(reverse('zettelbox:login'))

    try:
        box = Box.objects.get(name=box_name)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:index'))

    context['box'] = box
    return render(request, 'zettelbox/box.html', context)

def login(request):
    # standard boilerplate
    try:
        user = User.objects.get(pk=request.session.get('user_id'))
        return HttpResponseRedirect(reverse('zettelbox:index'))
    except ObjectDoesNotExist:
        context = {}
        return render(request, 'zettelbox/login.html', context)

def logout(request):
    if (request.session.get('user_id') != None):
        try:
            user = User.objects.get(pk=request.session.get('user_id'))
            user.delete()
        except ObjectDoesNotExist:
            pass
        del request.session['user_id']
    return HttpResponseRedirect(reverse('zettelbox:login'))


def taufe(request):
    name = request.POST['name']
    single_use_user = User(name=name)
    single_use_user.save()
    request.session['user_id'] = single_use_user.id
    return HttpResponseRedirect(reverse('zettelbox:index'))

def rename(request):
    name = request.POST['username']
    source = request.POST['source']
    try:
        user = User.objects.get(pk=request.session.get('user_id'))
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:login'))

    user.name = name
    user.save()
    return HttpResponseRedirect(source)
