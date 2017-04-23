from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import logging

@login_required
def index(request):
    context = {
        'dmm' : '',
    }
    return render(request, 'index.html', context)
