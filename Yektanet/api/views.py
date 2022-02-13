from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from advertiser_management.models import Advertiser, Ad
from .serializers import AdSerializer, AdvertiserSerializer, AdCreateSerializer
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny,IsAdminUser
from rest_framework.decorators import action
from .permissions import IsAuthorOrReadOnly 

class AdvertiserViewset(viewsets.ModelViewSet):
    

    def get_queryset(self):
        if self.action == 'add_ad':
            return Ad.objects.all() 
        return Advertiser.objects.all() 

    def get_serializer_class(self):
        if self.action == 'add_ad':
            return AdCreateSerializer
        return AdvertiserSerializer

    @action(detail=True, methods=['post'])
    def add_ad(self, request, pk=None):
        adv = get_object_or_404(Advertiser, id=pk)
        serializer = AdCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            Ad.objects.create(name = serializer.validated_data['name'], advertiser = adv, link = serializer.validated_data['link'], img = serializer.validated_data['img'])

            return Response({'status': 'Added Ad'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    
    def get_permissions(self):

        if self.action in ['create', 'update', 'destroy', 'partial_update']:
            permission_classes = [IsAdminUser]
        
        elif self.action == 'add_ad':
            permission_classes = [IsAdminUser, IsAuthorOrReadOnly]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]