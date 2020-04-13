from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Box, User, Paper
import random

############# VIEWS ###############
# Page for creating boxes
def index(request):
    # standard boilerplate
    try:
        user = User.objects.get(pk=request.session.get('user_id'))
    except ObjectDoesNotExist:
        single_use_user = User()
        single_use_user.save()
        request.session['user_id'] = single_use_user.id

    return render(request, 'zettelbox/index.html', {})

# show player interface or interface for adding papers
def box(request, box_name):
    # standard boilerplate
    try:
        user = User.objects.get(pk=request.session.get('user_id'))
    except ObjectDoesNotExist:
        single_use_user = User()
        single_use_user.save()
        request.session['user_id'] = single_use_user.id

    try:
        box = Box.objects.get(name=box_name)
        context = { 'box': box }
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:index'))

    if box.paper_set.filter(creator=user).count() > 0:

        context['papers'] = [ paper for paper in box.paper_set.filter(holder=user).filter(current=False) ]
        context['paper_count_inside'] = box.paper_set.filter(holder=None).count()
        context['paper_count'] = box.paper_set.count()

        for p in box.paper_set.filter(holder=user).filter(current=True):
            context['current'] = p

        return render(request, 'zettelbox/box.html', context)

    else:
        return render(request, 'zettelbox/signup.html', context)

############ ACTIONS ################

# create box or redirect if it exists
def create(request):
    # standard boilerplate
    try:
        user = User.objects.get(pk=request.session.get('user_id'))
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:box', args=(box_name,)))

    name = request.POST['name']
    try:
        existing_box = Box.objects.get(name=name)
    except ObjectDoesNotExist:
        yourbox = Box(name=name)
        yourbox.save()
    return HttpResponseRedirect(reverse('zettelbox:box', args=(name,)))

# enter 5 papers to play with
def signUp(request, box_name):
    try:
        box = Box.objects.get(name=box_name)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:index'))
    # standard boilerplate
    try:
        user = User.objects.get(pk=request.session.get('user_id'))
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:box', args=(box_name,)))

    if box.paper_set.filter(creator=user).count() > 0:
        return HttpResponseRedirect(reverse('zettelbox:box', args=(box_name,)))

    for i in [1,2,3,4,5]:
        p = Paper(content=request.POST['paper{:s}'.format(str(i))], holder=None, creator=user, box=box)
        p.save()

    return HttpResponseRedirect(reverse('zettelbox:box', args=(box_name,)))



# Put paper back in the box
def insertPaper(request, box_name, paper_id):
    # standard boilerplate
    try:
        user = User.objects.get(pk=request.session.get('user_id'))
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:box', args=(box_name,)))

    try:
        box = Box.objects.get(name=box_name)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:index'))

    try:
        paper = Paper.objects.get(pk=paper_id)
        paper.holder = None
        paper.current = False
        paper.save()
    except ObjectDoesNotExist:
        pass

    return HttpResponseRedirect(reverse('zettelbox:box', args=(box_name,)))

# Paper is explained and not current anymore
def confirmPaper(request, box_name, paper_id):
    # standard boilerplate
    try:
        user = User.objects.get(pk=request.session.get('user_id'))
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:box', args=(box_name,)))

    try:
        box = Box.objects.get(name=box_name)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:index'))

    try:
        paper = Paper.objects.get(pk=paper_id)
        paper.current = False
        paper.save()
    except ObjectDoesNotExist:
        pass

    return HttpResponseRedirect(reverse('zettelbox:box', args=(box_name,)))

# put all papers back in the box
def forceInsertAll(request, box_name):
    # standard boilerplate
    try:
        user = User.objects.get(pk=request.session.get('user_id'))
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:box', args=(box_name,)))

    try:
        box = Box.objects.get(name=box_name)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:index'))

    for paper in box.paper_set.all():
        paper.holder = None
        paper.current = False
        paper.save()

    return HttpResponseRedirect(reverse('zettelbox:box', args=(box_name,)))

def getRandom(request, box_name):
    # standard boilerplate
    try:
        user = User.objects.get(pk=request.session.get('user_id'))
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:box', args=(box_name,)))

    try:
        box = Box.objects.get(name=box_name)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('zettelbox:index'))

    for p in box.paper_set.filter(current=True).all():
        p.current = False
        p.save()

    papers_in_box = box.paper_set.filter(holder=None)

    if papers_in_box.count() < 1:
        return HttpResponseRedirect(reverse('zettelbox:box', args=(box_name,)))

    paper = random.choice(papers_in_box)
    paper.holder = user
    paper.current = True
    paper.save()

    return HttpResponseRedirect(reverse('zettelbox:box', args=(box_name,)))
