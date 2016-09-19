from django.shortcuts import get_object_or_404, render
from .models import Generation
from .models import AppealPoint

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

def detail(request, appealPointId):
    appealPoint = get_object_or_404(AppealPoint, pk=appealPointId)
    context = {
        'appealPoint'  : appealPoint,
    }
    return render(request, 'buono/detail.html', context)
