from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import AppealPoint
from .forms import AppealPointForm
import logging

logger = logging.getLogger('model')

@login_required
def index(request):
    appealPoints = AppealPoint.objects.order_by('-updTm').select_related()
    context = {
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
def update(request):
    appealPoint = None
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
    message = '更新しました。'
    context = {
        'message':message,
        'appealPoint' : appealPoint,
    }
    appealPoint.save()
    return render(request, 'buono/update.html', context)
