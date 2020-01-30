from App.views import Train, Predict
from django.conf.urls import url

app_name = 'App'

urlpatterns = [
    url('train/$', Train.as_view(), name="train"),
    url('predict/$', Predict.as_view(), name="predict"),
]