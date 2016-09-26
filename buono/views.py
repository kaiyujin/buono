from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from .models import AppealPoint
from .models import Comment
import logging

logger = logging.getLogger('model')

@login_required
def index(request):
    appealPoints = AppealPoint.objects.order_by('-id').select_related()
    context = {
        'appealPoints' : appealPoints,
    }
    return render(request, 'buono/index.html', context)

@login_required
def detail(request, appealPointId):
    return HttpResponseRedirect("/buono/")
    appealPoint = get_object_or_404(AppealPoint, pk=appealPointId)
    nextAp = None
    prevAp = None
    try:
        prevAp = AppealPoint.objects.get(user_id=appealPoint.id+1)
    except ObjectDoesNotExist:
        pass
    try:
        nextAp = AppealPoint.objects.get(user_id=appealPoint.id-1)
    except ObjectDoesNotExist:
        pass
    comments = Comment.objects.filter(appealPoint=appealPoint).order_by('-updTm')
    context = {
        'appealPoint'  : appealPoint,
        'comments'     : comments,
        'nextAp'     : nextAp,
        'prevAp'     : prevAp,
    }
    return render(request, 'buono/detail.html', context)

@login_required
def update(request):
    appealPoint = None
    message = ''
    try:
        appealPoint = AppealPoint.objects.get(user_id=request.user.id)
    except ObjectDoesNotExist:
        appealPoint = AppealPoint()
    if request.method == 'POST':
        appealPoint.task    = request.POST['task']
        appealPoint.process = request.POST['process']
        appealPoint.result  = request.POST['result']
        appealPoint.force   = request.POST['force']
        appealPoint.user    = request.user
        appealPoint.save()
        message = '更新しました。'
    context = {
        'message':message,
        'appealPoint' : appealPoint,
    }
    return render(request, 'buono/update.html', context)

@login_required
def vote(request):

    return render(request, 'buono/update.html', context)

@login_required
def addComment(request):
    if request.method == 'GET':
        return HttpResponseRedirect("/buono/")
    appealPoint = get_object_or_404(AppealPoint, pk=request.POST['appealPointId'])
    comment = Comment()
    comment.appealPoint = appealPoint
    comment.detail = request.POST['comment']
    comment.user   = request.user
    comment.save()
    return HttpResponseRedirect("/buono/"+request.POST['appealPointId']+"/")
