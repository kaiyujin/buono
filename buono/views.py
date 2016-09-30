from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from .models import AppealPoint,Comment,Vote
import logging
from datetime import date

logger = logging.getLogger('model')
#isVoteTerm = date(2016, 10, 4) <= date.today()
isVoteTerm = True #test
#isVoteTerm = False #test

@login_required
def index(request):
    appealPoints = AppealPoint.objects.order_by('-id').select_related()
    commitedBuono = True
    commitedSemiBuono = True
    try:
        Vote.objects.get(typeCd='1' ,user_id=request.user.id)
    except ObjectDoesNotExist:
        commitedBuono = False
    try:
        Vote.objects.get(typeCd='2' ,user_id=request.user.id)
    except ObjectDoesNotExist:
        commitedSemiBuono = False
    commnetCount = Comment.objects.filter(user_id=request.user.id).count()
    context = {
        'appealPoints' : appealPoints,
        'isVoteTerm' : isVoteTerm,
        'commitedBuono' : commitedBuono,
        'commitedSemiBuono' : commitedSemiBuono,
        'commnetCount' : commnetCount,
    }
    return render(request, 'buono/index.html', context)

@login_required
def detail(request, appealPointId):
    if not isVoteTerm :
        return HttpResponseRedirect("/buono/")
    appealPoint = get_object_or_404(AppealPoint, pk=appealPointId)
    comment, buono, semiBuono, nextAp, prevAp = (None,None,None,None,None)
    comments, buonoList, semiBuonoList = (None,None,None)
    alreadyBuono, alreadySemiBuono = (None, None)
    try:
        prevAp = AppealPoint.objects.get(user_id=appealPoint.id+1)
    except ObjectDoesNotExist:
        pass;
    try:
        nextAp = AppealPoint.objects.get(user_id=appealPoint.id-1)
    except ObjectDoesNotExist:
        pass
    if request.user.id == appealPoint.id:
        comments = Comment.objects.filter(appealPoint=appealPoint).order_by('-updTm')
        buonoList = Vote.objects.filter(appealPoint_id=appealPoint.id,typeCd='1')
        semiBuonoList = Vote.objects.filter(appealPoint_id=appealPoint.id,typeCd='2')
    else:
        try:
            comment = Comment.objects.get(appealPoint_id=appealPoint.id,user_id=request.user.id)
        except ObjectDoesNotExist:
            pass;
        try:
            buono = Vote.objects.get(appealPoint_id=appealPoint.id,user_id=request.user.id,typeCd='1')
            alreadyBuono = Vote.objects.get(user_id=request.user.id,typeCd='1')
        except ObjectDoesNotExist:
            pass;
        try:
            semiBuono = Vote.objects.get(appealPoint_id=appealPoint.id,user_id=request.user.id,typeCd='2')
            alreadySemiBuono = Vote.objects.get(appealPoint_id=appealPoint.id,user_id=request.user.id,typeCd='2')
        except ObjectDoesNotExist:
            pass;
    context = {
        'appealPoint'  : appealPoint,
        'comments'     : comments,
        'nextAp'     : nextAp,
        'prevAp'     : prevAp,
        'isVoteTerm' : isVoteTerm,
        'isMine' : request.user.id == appealPoint.id,
        'buonoList' : buonoList,
        'semiBuonoList' : semiBuonoList,
        'comment' : comment,
        'buono' : buono,
        'semiBuono' : semiBuono,
        'alreadyBuono' : alreadyBuono,
        'alreadySemiBuono' : alreadySemiBuono,
    }
    return render(request, 'buono/detail.html', context)

@login_required
def update(request):
    if isVoteTerm :
        return HttpResponseRedirect("/buono/")
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
        'isVoteTerm' : isVoteTerm,
    }
    return render(request, 'buono/update.html', context)

@login_required
def vote(request):
    if not isVoteTerm :
        return HttpResponseRedirect("/buono/")
    if request.method == 'GET':
        return HttpResponseRedirect("/buono/")
    appealPoint = get_object_or_404(AppealPoint, pk=request.POST['appealPointId'])
    vote = Vote()
    vote.appealPoint = appealPoint
    vote.user = request.user
    vote.typeCd = request.POST['typeCd']
    vote.detail = request.POST['comment']
    vote.save()
    return HttpResponseRedirect("/buono/"+request.POST['appealPointId']+"/")

@login_required
def addComment(request):
    if not isVoteTerm :
        return HttpResponseRedirect("/buono/")
    if request.method == 'GET':
        return HttpResponseRedirect("/buono/")
    appealPoint = get_object_or_404(AppealPoint, pk=request.POST['appealPointId'])
    comment = None
    try:
        comment = Comment.objects.get(appealPoint_id=appealPoint.id,user_id=request.user.id)
    except ObjectDoesNotExist:
        comment = Comment()
        comment.appealPoint = appealPoint
        comment.user   = request.user
    comment.detail = request.POST['comment']
    comment.save()
    return HttpResponseRedirect("/buono/"+request.POST['appealPointId']+"/")
