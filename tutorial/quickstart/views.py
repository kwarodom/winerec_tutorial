from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from quickstart.serializers import UserSerializer, GroupSerializer
from rest_framework.response import Response
import pandas as pd
import numpy as np
import joblib

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PredictViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response('Hi')
    def create(self, request):
        corr_matrix = joblib.load('./quickstart/corr_matrix')
        rating_crosstab = joblib.load('./quickstart/rating_crosstab')
        movie_name = request.data['movie_name']
        movie_names = rating_crosstab.columns
        movies_list = list(movie_names)
        movie_id = movies_list.index(movie_name)
        corr_movie = corr_matrix[movie_id]
        suggested_movies = list(movie_names[(corr_movie < 1.0) & (corr_movie > 0.9)])
        return Response(suggested_movies[0:5])
