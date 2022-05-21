from posixpath import basename
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from airlines_app.api.views import (AirlineVS, PlaneAV, PlaneDetalleAV, PilotCreate, PilotList, PilotDetail, PilotAV, PilotDetalleAV, TraceabilityAV, TraceabilityDetalleAV)


router = DefaultRouter()
router.register('airline', AirlineVS, basename="airline")

urlpatterns = [
    path('', include(router.urls)),
    
    # Paths Plane
    path('plane/', PlaneAV.as_view(), name='plane'),
    path('plane/<int:pk>', PlaneDetalleAV.as_view(), name='plane-detail'),
    
    # Paths Pilots
    path('pilot/', PilotAV.as_view(), name='pilot'),
    path('pilot/<int:pk>', PilotDetalleAV.as_view(), name='pilot-detail'),
    
    
    path('plane/<int:pk>/pilot-create', PilotCreate.as_view(), name='pilot-create'),
    path('plane/<int:pk>/pilot', PilotList.as_view(), name='pilot-list'),
    path('plane/pilot/<int:pk>', PilotDetail.as_view(), name='pilot-detail'),
    
    # Paths Custrom Traceability
    path('traceability/', TraceabilityAV.as_view(), name='traceability'),
    path('traceability/<int:pk>', TraceabilityDetalleAV.as_view(), name='traceability-detail')
]
