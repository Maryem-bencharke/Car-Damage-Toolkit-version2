from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView

from .models import Car
from .serializers import CarSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser

from .detection_module import *

class CarCreate(APIView):
    """
    create a new Car.
    """
    def post(self, request, format=None):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CarDetail(APIView):
    """
    Retrieve, Update a Car.
    """
    def get_object(self, id):
        try:
            return Car.objects.get(id=id)

        except Car.DoesNotExist:
            raise Http404

    def get(self, request,id, format=None):
        car= self.get_object(id)
        serializer = CarSerializer(car)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        car = self.get_object(id)

        car = engine(car)
        
        serializer = CarSerializer(car, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





