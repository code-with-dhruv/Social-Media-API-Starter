from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = User.objects.all()

       
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Number of records per page
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = UserSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
from rest_framework.parsers import JSONParser

class UserSearchViewSet(viewsets.ViewSet):
    parser_classes = [JSONParser]

    def list(self, request):
        data = request.data

        if 'prompt' not in data:
            return Response({'error': 'Please provide a search query'}, status=status.HTTP_400_BAD_REQUEST)

        search_query = data['prompt']

        queryset = User.objects.filter(
            Q(username=search_query) |
            Q(email__icontains=search_query)
        )

        serializer = UserSerializer(queryset, many=True)
        if serializer.data!=[]:
            return Response(serializer.data)
        else:
             return Response({'error': 'Didnt match any Email or Username'})