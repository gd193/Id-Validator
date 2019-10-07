from django.shortcuts import render
from rest_framework import generics,mixins, permissions, exceptions
from .models.Generator import id,id_generator
from .serializers import id_serializer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class id_view(mixins.ListModelMixin,
              mixins.UpdateModelMixin,
              generics.GenericAPIView):
    queryset = id.objects.all()
    serializer_class = id_serializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'Kombination'



    def get(self, request, *args, **kwargs):
        serializer = id_serializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        serializer = id_serializer(data=request.data)
        serializer.update(request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.error_messages)
        



