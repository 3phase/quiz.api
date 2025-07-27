import json
from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.

@api_view(['POST'])
def api_home(request, *args, **kwargs):
    data = {}
    return Response(data)
