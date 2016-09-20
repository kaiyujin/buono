from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import Generation
from .models import AppealPoint
from .forms import AppealPointForm
import logging

logger = logging.getLogger('model')

@login_required
def index(request):
    generations = Generation.objects.order_by('-sortNo')
    generation = generations[0]
    appealPoints = AppealPoint.objects.filter(generation_id=generation.id).order_by('-updTm').select_related()
    context = {
        'generations'  : generations,
        'generation'   : generation,
        'appealPoints' : appealPoints,
    }
    return render(request, 'buono/index.html', context)

@login_required
def listForGeneration(request, generation_id):
    generations = Generation.objects.order_by('-sortNo')
    generation = get_object_or_404(Generation, pk=generation_id)
    appealPoints = AppealPoint.objects.filter(generation_id=generation_id).order_by('-updTm').select_related()
    context = {
        'generations'  : generations,
        'generation'   : generation,
        'appealPoints' : appealPoints,
    }
    return render(request, 'buono/index.html', context)

@login_required
def detail(request, appealPointId):
    appealPoint = get_object_or_404(AppealPoint, pk=appealPointId)
    context = {
        'appealPoint'  : appealPoint,
    }
    return render(request, 'buono/detail.html', context)

@login_required
def update(request,generation_id):
    appealPoint = AppealPoint.objects.filter(generation_id=generation_id).filter(user_id=request.user.id)
    context = {
        'appealPoint' : appealPoint,
        'generationId' : generation_id,
    }
    return render(request, 'buono/update.html', context)

@login_required
def updated(request):
    appealPoint = NULL
    try:
        appealPoint = AppealPoint.objects.filter(generation_id=request.POST['generationId']).get(user_id=request.user.id)
    except ObjectDoesNotExist:
        appealPoint
        logger.debug('新規作成')
    appealPoint.task    = request.POST['task']
    appealPoint.process = request.POST['process']
    appealPoint.result  = request.POST['result']
    appealPoint.force   = request.POST['force']
    appealPoint.user    = request.user.id
    appealPoint.generation = request.POST['generationId']
    message = '更新しました。'
    context = {
        'message':message,
        'appealPoint' : appealPoint,
        'generationId':appealPoint.generation,
    }
    appealPoint.save()
    return render(request, 'buono/update.html', context)
