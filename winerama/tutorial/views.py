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


@csrf_exempt
def clf_predict(request):
    body = json.loads(request.body.decode("utf-8"))

    data = body['features']
    clf = joblib.load('./tutorial/model.pkl') 

    result = clf.predict(data)
    result = pd.Series(result).to_json(orient='values')

    return JsonResponse({'result': result})