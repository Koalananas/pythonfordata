from App.views import Predict
from django.conf.urls import url

app_name = 'App'

urlpatterns = [
    url('predict/$', Predict.as_view(), name="predict"),
]