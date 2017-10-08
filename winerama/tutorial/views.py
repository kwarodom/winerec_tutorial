from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework.response import Response
from sklearn.externals import joblib
import json
import pandas as pd

from tutorial.serializers import UserSerializer, GroupSerializer


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
    def create(self, request):
        data = request.data['features']
        clf = joblib.load('./tutorial/model.pkl') 

        result = clf.predict(data)

        return Response({'result': result})


class RecommendViewSet(viewsets.ViewSet):
    def create(self, request):
        target_movie_name = request.data['movie_name']

        corr_mat = joblib.load('./tutorial/rec_model.pkl') 
        movie_names = joblib.load('./tutorial/movie_names.pkl')
        pop_movies = joblib.load('./tutorial/pop_movies.pkl')

        movies_list = list(movie_names)

        try:
            target_movie_index = movies_list.index(target_movie_name)
        except ValueError:
            top_movies = pop_movies.sort_values(by='rating', ascending=False)

            return Response({
                'message': "'{}' is not in the list".format(target_movie_name),
                'result':  top_movies['movie title'].head(5)
            })

        corr_target = corr_mat[target_movie_index]

        criteria = (corr_target < 1.0) & (corr_target > 0.9)
        recommended = list(movie_names[criteria])

        # result = clf.predict(data)
        # return Response({'result': result})
        return Response({'result': recommended})


# @csrf_exempt
# def clf_predict(request):
#     body = json.loads(request.body.decode("utf-8"))

#     data = body['features']
#     clf = joblib.load('./tutorial/model.pkl') 

#     result = clf.predict(data)
#     result = pd.Series(result).to_json(orient='values')

#     return JsonResponse({'result': result})