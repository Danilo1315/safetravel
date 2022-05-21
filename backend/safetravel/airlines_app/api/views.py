from http.client import REQUEST_URI_TOO_LONG
from multiprocessing import context
from os import stat
from django.forms import ValidationError
from rest_framework.response import Response
from airlines_app.api.pagination import PlanePagination
from airlines_app.models import Airline, Plane, Pilot
from airlines_app.api.serializers import AirlineSerializer, PlaneSerializer, PilotSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework import viewsets
from django.shortcuts import render
from airlines_app.api.permissions import IsAdminOrReadOnly
from airlines_app.api.pagination import PlanePagination, PlaneLOPagination

# Create your views here.
class PilotCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PilotSerializer

    def get_queryset(self):
        return Pilot.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        plane = Plane.objects.get(pk=pk)
        
        pilot_queryset = Pilot.objects.filter(plane=plane)
        print("Cantidad de  pilotos: "+str(len(pilot_queryset)))
        if len(pilot_queryset) >= 2:
            raise ValidationError("El avión ya cuenta con el maximo de pilotos asignados.")
        
        serializer.save(plane=plane)


class PilotList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PilotSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Pilot.objects.filter(plane=pk)
    
class PilotDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    
    
class TraceabilityAV(APIView):
    def get(self, request):
        data = []
        pilot = Pilot.objects.all()
        print(pilot)
        serializer = PilotSerializer(pilot, many=True, context={'request': request})
        print(len(serializer.data))
        cont = 0
        while cont < len(serializer.data):
            data.append({})

            data[cont] = serializer.data[cont]
            
            # trace plane
            pk_plane = serializer.data[cont]['plane']
            print("pk_plane: "+str(pk_plane))
            plane = Plane.objects.get(pk=pk_plane)
            print("query plane: " +str(plane) )
            serializer_plane = PlaneSerializer(plane)
            print("id plane: "+str(serializer_plane.data['id']))
            data[cont]['name_plane'] = serializer_plane.data['title']
            data[cont]['code_plane'] = serializer_plane.data['code']
            
            
            # trace airline
            pk_air = serializer_plane.data['airline']
            air = Airline.objects.get(pk=pk_air)
            print(air)
            serializer_air = AirlineSerializer(air)
            data[cont]['name_air'] = serializer_air.data['title']
            data[cont]['code_air'] = serializer_air.data['code']

            cont += 1
            
        return Response(data)
    
    
class TraceabilityDetalleAV(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        data = []
        
        pilot = Pilot.objects.get(pk=pk)
        print(pilot)
        serializer = PilotSerializer(pilot)
        data.append({})
        data[0] = serializer.data
        
        # trace plane
        pk_plane = serializer.data['plane']
        plane = Plane.objects.get(pk=pk_plane)
        serializer_plane = PlaneSerializer(plane)
        data[0]['name_plane'] = serializer_plane.data['title']
        data[0]['code_plane'] = serializer_plane.data['code']
        
        
        # trace airline
        pk_air = serializer_plane.data['airline']
        air = Airline.objects.get(pk=pk_air)
        serializer_air = AirlineSerializer(air)
        data[0]['name_air'] = serializer_air.data['title']
        data[0]['code_air'] = serializer_air.data['code']

        return Response(data)
    
# ***************************************************************************************
# Classes Standars

class PilotAV(APIView, PlaneLOPagination):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    def get(self, request):
        pilot = Pilot.objects.all()
        results = self.paginate_queryset(pilot, request, view=self)
        serializer = PilotSerializer(results, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        try:
            
            plane = Plane.objects.get(pk=request.data['plane'])
        
            pilot_queryset = Pilot.objects.filter(plane=plane)
            print("Cantidad de  pilotos: "+str(len(pilot_queryset)))
            
            if len(pilot_queryset) >= 2:
                return Response({'error':'El avión ya cuenta con el maximo de pilotos asignados.'}, status=status.HTTP_404_NOT_FOUND)
            else:
                pilot = Pilot.objects.get(code=request.data['code'])
                print("Existente: "+str(pilot))
                if pilot:
                    return Response({'error': 'The pilot is already created!'}, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            pass
        
        
        serializer = PilotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class PilotDetalleAV(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
            pilot = Pilot.objects.get(pk=pk)
        except Pilot.DoesNotExist:
            return Response({'error': 'Piloto no encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PilotSerializer(pilot)
        return Response(serializer.data)
    
    
    def put(self, request, pk):
        try:
            pilot = Pilot.objects.get(pk=pk)
        except Pilot.DoesNotExist:
            return Response({'error': 'Piloto no encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PilotSerializer(pilot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status)
        
    def delete(self, request, pk):
        try:
            pilot = Pilot.objects.get(pk=pk)
        except Pilot.DoesNotExist:
            return Response({'error': 'Piloto no encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        
        pilot.delete()
        return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)
    
    



# *****************************************************************************************
class AirlineVS(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    print(serializer_class)
    


class PlaneAV(APIView, PlaneLOPagination):
    # permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    def get(self, request):
        plane = Plane.objects.all()
        results = self.paginate_queryset(plane, request, view=self)
        serializer = PlaneSerializer(results, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        try:
            plane = Plane.objects.get(code=request.data['code'])
            print("Existente: "+str(plane))
            if plane:
                return Response({'error': 'The plane is already created!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            pass
        
        serializer = PlaneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class PlaneDetalleAV(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
            print("hola get plane 1")
            plane = Plane.objects.get(pk=pk)
        except Plane.DoesNotExist:
            return Response({'error': 'Avion no encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PlaneSerializer(plane)
        return Response(serializer.data)
    
    
    def put(self, request, pk):
        try:
            plane = Plane.objects.get(pk=pk)
        except Plane.DoesNotExist:
            return Response({'error': 'Avion no encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PlaneSerializer(plane, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status)
        
    def delete(self, request, pk):
        try:
            plane = Plane.objects.get(pk=pk)
        except Plane.DoesNotExist:
            return Response({'error': 'Avion no encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        
        plane.delete()
        return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)