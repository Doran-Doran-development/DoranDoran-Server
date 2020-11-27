import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
from .models import Room
from .serializers import RoomSerializer



class ListRoomAPI(mixins.ListModelMixins
                  generics.GenericsAPIView):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get(self,request,*args,**kwargs):
        return self.list(reqeust,*args,**kwargs)

class GetRoomAPI(mixins.RetrieveModelMinxins
                generics.GenericsAPIView):
    
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)