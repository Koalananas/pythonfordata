from django.shortcuts import render

# Create your views here.
import os
import pickle
import numpy as np
import pandas as pd
from sklearn import datasets
from django.conf import settings
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
import json


class Train(views.APIView):
    def post(self, request):
        iris = datasets.load_iris()
        mapping = dict(zip(np.unique(iris.target), iris.target_names))

        X = pd.DataFrame(iris.data, columns=iris.feature_names)
        y = pd.DataFrame(iris.target).replace(mapping)
        model_name = request.data.pop('model_name')

        try:
            clf = RandomForestClassifier(**request.data)
            clf.fit(X, y)
        except Exception as err:
            return Response(str(err), status=status.HTTP_400_BAD_REQUEST)

        path = os.path.join(settings.MODEL_ROOT, model_name)
        with open(path, 'wb') as file:
            pickle.dump(clf, file)
        return Response(status=status.HTTP_200_OK)


class Predict(views.APIView):
    def post(self, request):
        result = 0
        #requettePD = pd.read_json(json.loads(request.data['json']))
        self.request.POST._mutable = True

        #r = json.loads(request.data.pop('demande')[0])
        rpd = pd.read_json(request.data.pop('demande')[0])

        model_name = "model"
        path = os.path.join(settings.MODEL_ROOT, model_name)
        with open(path, 'rb') as file:
            model = pickle.load(file)
        try:
            result = model.predict(rpd)

        except Exception as err:
            return Response(str(err), status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_200_OK)