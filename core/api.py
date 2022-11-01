from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import *
from core.serializers import *


class HistoriaClinicaView(ListCreateAPIView):
    serializer_class = HistoriaClinicaSerializer
    queryset = HistoriaClinica.objects.all()


class HistoriaClinicaDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = HistoriaClinicaSerializer
    queryset = HistoriaClinica.objects.all()