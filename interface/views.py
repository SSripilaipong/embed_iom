from django.http import HttpResponse
from django.template import loader

from django.shortcuts import render

# Create your views here.
def dashboard(request):
    template = loader.get_template('interface/monitor2.html')
    return HttpResponse(template.render({}, request))

def reporter(request):
    template = loader.get_template('interface/reporter2.html')
    return HttpResponse(template.render({}, request))

