from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Box, User, Paper
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
        context['box'] = box
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:index'))

    context['papers'] = [ paper for paper in box.paper_set.filter(holder=user) ]

    context['message'] = request.GET.get('message')

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

def addPaper(request, box_name):
    # standard boilerplate
    try:
        user = User.objects.get(pk=request.session.get('user_id'))
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:login'))

    try:
        box = Box.objects.get(name=box_name)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:index'))

    if not box.open:
        return HttpResponseRedirect('{:s}?message=Es dürfen keine Zettel mehr geschrieben werden!'.format(reverse('zettelbox:box', args=(box_name,))))

    content = request.POST['content']
    paper = Paper(box = box, content = content, holder = user)
    paper.save()
    return HttpResponseRedirect('{:s}?message=Zettel gespeichert!'.format(reverse('zettelbox:box', args=(box_name,))))

def deletePaper(request, box_name, paper_id):
    # standard boilerplate
    try:
        user = User.objects.get(pk=request.session.get('user_id'))
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:login'))

    try:
        box = Box.objects.get(name=box_name)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:index'))

    try:
        paper = Paper.objects.get(pk=paper_id)
        paper.delete()
    except ObjectDoesNotExist:
        pass

    return HttpResponseRedirect('{:s}?message=Zettel vernichtet!'.format(reverse('zettelbox:box', args=(box_name,))))

def insertPaper(request, box_name, paper_id):
    # standard boilerplate
    try:
        user = User.objects.get(pk=request.session.get('user_id'))
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:login'))

    try:
        box = Box.objects.get(name=box_name)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:index'))

    try:
        paper = Paper.objects.get(pk=paper_id)
        paper.holder = None
        paper.save()
        return HttpResponseRedirect('{:s}?message=Zettel in die Box gelegt!'.format(reverse('zettelbox:box', args=(box_name,))))
    except ObjectDoesNotExist:
        return HttpResponseRedirect('{:s}?message=Zettel scheint verloren gegangen zu sein :/'.format(reverse('zettelbox:box', args=(box_name,))))

def insertAll(request, box_name):
    # standard boilerplate
    try:
        user = User.objects.get(pk=request.session.get('user_id'))
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:login'))

    try:
        box = Box.objects.get(name=box_name)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:index'))

    for paper in box.paper_set.filter(holder=user):
        paper.holder = None
        paper.save()

    return HttpResponseRedirect('{:s}?message=Alle Zettel zurückgelegt!'.format(reverse('zettelbox:box', args=(box_name,))))

def forceInsertAll(request, box_name):
    # standard boilerplate
    try:
        user = User.objects.get(pk=request.session.get('user_id'))
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:login'))

    try:
        box = Box.objects.get(name=box_name)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:index'))

    for paper in box.paper_set.all():
        paper.holder = None
        paper.save()

    return HttpResponseRedirect('{:s}?message=Zettel von allen in die Box zurückgesaugt!'.format(reverse('zettelbox:box', args=(box_name,))))

def close(request, box_name):
    # standard boilerplate
    try:
        user = User.objects.get(pk=request.session.get('user_id'))
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:login'))

    try:
        box = Box.objects.get(name=box_name)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:index'))

    box.open = False
    box.save()

    return HttpResponseRedirect('{:s}?message=Ok, niemand darf mehr neue Zettel schreiben!'.format(reverse('zettelbox:box', args=(box_name,))))

def open(request, box_name):
    # standard boilerplate
    try:
        user = User.objects.get(pk=request.session.get('user_id'))
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:login'))

    try:
        box = Box.objects.get(name=box_name)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:index'))

    box.open = True
    box.save()

    return HttpResponseRedirect('{:s}?message=Man darf jetzt wieder Zettel schreiben!'.format(reverse('zettelbox:box', args=(box_name,))))
