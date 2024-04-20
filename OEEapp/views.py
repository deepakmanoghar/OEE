from django.shortcuts import render
from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Machine, ProductionLog
from .serializers import MachineSerializer, ProductionLogSerializer
from .utils import calculate_availability, calculate_performance, calculate_quality, calculate_oee

class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

    @action(detail=True, methods=['get'])
    def calculate_oee(self, request, pk=None):
        machine = self.get_object()
        
        # Calculate Availability
        production_logs = ProductionLog.objects.filter(machine=machine)
        available_time = (machine.time - production_logs.earliest('start_time').start_time).total_seconds() / 3600
        unplanned_downtime = production_logs.aggregate(total_downtime=Sum('duration'))['total_downtime'] or 0
        availability = calculate_availability(available_time, unplanned_downtime)
        
        # Calculate Performance
        ideal_cycle_time = 1
        actual_output = production_logs.count()
        available_operating_time = available_time - unplanned_downtime
        performance = calculate_performance(ideal_cycle_time, actual_output, available_operating_time)
        
        # Calculate Quality
        good_product_count = 480
        total_product_count = production_logs.count()
        quality = calculate_quality(good_product_count, total_product_count)
        
        # Calculate OEE
        oee = calculate_oee(availability, performance, quality)
        
        return Response({'OEE': oee})