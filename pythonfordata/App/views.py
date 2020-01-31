from django.shortcuts import render
import os
import pickle
import numpy as np
import pandas as pd
from sklearn import datasets
from django.conf import settings
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
import json

class Predict(views.APIView):
    def post(self, request):
        result = 0
        self.request.POST._mutable = True
        rpd = pd.read_json(request.data.pop('demande')[0])
        print("Requette de " + str(rpd.shape[0]) + " observations")
        model_name = "model"
        path = os.path.join(settings.MODEL_ROOT, model_name)
        with open(path, 'rb') as file:
            model = pickle.load(file)
        try:
            result = model.predict(rpd)
        except Exception as err:
            return Response(str(err), status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_200_OK)