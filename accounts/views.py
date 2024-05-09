from django.contrib.auth.models import User 
from django.shortcuts import render
from rest_framework import generics
from .serializers import GitHubUserSerializer
import requests

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = GitHubUserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return render(request, 'users_list.html', {'users': serializer.data})

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = GitHubUserSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return render(request, 'user_detail.html', {'user': serializer.data})

    def github_repositories(request, username):
        url = f'https://api.github.com/users/{username}/repos'
        response = requests.get(url)
        
        if response.status_code == 200:
            repositories = response.json()
            return render(request, 'github_repositories.html', {'repositories': repositories})
        else:
            error_message = 'Failed to fetch repositories.'
            return render(request, 'github_repositories_error.html', {'error': error_message})
