from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from .models import AppealPoint,Comment,Vote
import logging
from datetime import date

logger = logging.getLogger('model')
isVoteTerm = date(2017, 10, 4) <= date.today()
#isVoteTerm = True #test
#isVoteTerm = False #test

@login_required
def index(request):
    appealPoints = AppealPoint.objects.order_by('-id').select_related()
    commitedBuono = True
    commitedSemiBuono = True
    mineId = None
    try:
        mineId = AppealPoint.objects.get(user_id=request.user.id).id
    except ObjectDoesNotExist:
        pass
    try:
        Vote.objects.get(typeCd='1' ,user_id=request.user.id)
    except ObjectDoesNotExist:
        commitedBuono = False
    try:
        Vote.objects.get(typeCd='2' ,user_id=request.user.id)
    except ObjectDoesNotExist:
        commitedSemiBuono = False
    commnetCount = Comment.objects.filter(user_id=request.user.id).count()
    part_timer = True if request.user.groups.filter(name='part_timer').exists() else False
    isDmm = True if request.user.groups.filter(name='dmm').exists() else False
    context = {
        'appealPoints' : appealPoints,
        'isVoteTerm' : isVoteTerm,
        'commitedBuono' : commitedBuono,
        'commitedSemiBuono' : commitedSemiBuono,
        'commnetCount' : commnetCount,
        'mineId' : mineId,
        'part_timer' : part_timer,
        'dmm' : isDmm,
    }
    return render(request, 'buono/index.html', context)

@login_required
def detail(request, appealPointId):
    isDmm = True if request.user.groups.filter(name='dmm').exists() else False
    if not isVoteTerm and not isDmm:
        return HttpResponseRedirect("/buono/")
    appealPoint = get_object_or_404(AppealPoint, pk=appealPointId)
    comment, buono, semiBuono, nextAp, prevAp = ('',None,None,None,None)
    comments, buonoList, semiBuonoList = (None,None,None)
    alreadyBuono, alreadySemiBuono = (None, None)
    part_timer = True if request.user.groups.filter(name='part_timer').exists() else False
    try:
        prevAp = AppealPoint.objects.get(pk=appealPoint.id+1)
    except ObjectDoesNotExist:
        pass;
    try:
        nextAp = AppealPoint.objects.get(pk=appealPoint.id-1)
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
        except ObjectDoesNotExist:
            pass;
        try:
            alreadyBuono = Vote.objects.get(user_id=request.user.id,typeCd='1')
        except ObjectDoesNotExist:
            pass;
        try:
            semiBuono = Vote.objects.get(appealPoint_id=appealPoint.id,user_id=request.user.id,typeCd='2')
        except ObjectDoesNotExist:
            pass;
        try:
            alreadySemiBuono = Vote.objects.get(user_id=request.user.id,typeCd='2')
        except ObjectDoesNotExist:
            pass;
    mineId = None
    try:
        mineId = AppealPoint.objects.get(user_id=request.user.id).id
    except ObjectDoesNotExist:
        pass
    context = {
        'appealPoint'  : appealPoint,
        'comments'     : comments,
        'nextAp'     : nextAp,
        'prevAp'     : prevAp,
        'isVoteTerm' : isVoteTerm,
        'isMine' : mineId == appealPoint.id,
        'buonoList' : buonoList,
        'semiBuonoList' : semiBuonoList,
        'comment' : comment,
        'buono' : buono,
        'semiBuono' : semiBuono,
        'alreadyBuono' : alreadyBuono,
        'alreadySemiBuono' : alreadySemiBuono,
        'part_timer' : part_timer,
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

@login_required
def showComment(request):
    isDmm = True if request.user.groups.filter(name='dmm').exists() else False
    if not isDmm:
        return HttpResponseRedirect("/buono/")
    raw = my_custom_sql("""
select
 vt."typeCd" as type,
 concat(us.last_name,us.first_name) as to_name,
 concat(
 (select inus.last_name from auth_user inus where vt.user_id = inus.id),
 (select inus.first_name from auth_user inus where vt.user_id = inus.id)) as from_name,
 vt.detail
from
 buono_vote vt
inner join
 buono_appealpoint ap
on vt."appealPoint_id" = ap.id
inner join
  auth_user us
on
us.id = ap.user_id
union
select
'-' as type,
concat(us.last_name,us.first_name) as to_name,
concat(
(select inus.last_name from auth_user inus where cm.user_id = inus.id),
(select inus.first_name from auth_user inus where cm.user_id = inus.id)),
cm.detail
from
  buono_appealpoint ap
inner join
  buono_comment cm
on cm."appealPoint_id" = ap.id
inner join
  auth_user us
on ap.user_id = us.id
    order by type, to_name
""")
    resultList = []
    tpl = list(raw)
    for val in tpl:
        resultList.append({'typecd':val[0],'to':val[1],'from':val[2],'detail':val[3],})
    context = {
        'raw' : resultList,
    }
    return render(request, 'buono/show_comment.html', context)

@login_required
def countBuono(request):
    isDmm = True if request.user.groups.filter(name='dmm').exists() else False
    if not isDmm:
        return HttpResponseRedirect("/buono/")
    raw = my_custom_sql("""
SELECT
    typecd,name,cnt
FROM (
SELECT
 CASE v."typeCd"
  WHEN '1' THEN 'buono'
  WHEN '2' THEN '準buono' 
  ELSE 'コメント'
 END AS typecd
 ,u.first_name || u.last_name AS name, COUNT(1) cnt
FROM
 buono_vote v INNER JOIN buono_appealpoint ba
 ON v."appealPoint_id" = ba.id
 INNER JOIN auth_user u
 ON ba.user_id = u.id
GROUP BY
 v."typeCd",u.first_name || u.last_name
) AS tmp
ORDER BY typecd,cnt desc
""")
    resultList = []
    tpl = list(raw)
    for val in tpl:
        resultList.append({'typecd':val[0],'name':val[1],'cnt':val[2],})
    context = {
        'raw' : resultList,
    }
    return render(request, 'buono/count_buono.html', context)


def my_custom_sql(sql):
    from django.db import connection, transaction
    cursor = connection.cursor()
    cursor.execute(sql)
    return cursor.fetchall()
