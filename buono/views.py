from django.shortcuts import render
from .models import Generation

# Create your views here.
def index(request):
    generations = Generation.objects.order_by('-sortNo')
    context = {'generations' : generations}
    return render(request, 'buono/index.html', context)

def listForGeneration(request, generation_id):
    generations = Generation.objects.order_by('-sortNo')
    context = {'generations' : generations}
    return render(request, 'buono/index.html', context)
