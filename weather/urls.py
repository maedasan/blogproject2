from django.urls import path
from .views import Weatherday,csv_download


app_name = 'weathapp'
urlpatterns = [
    path('weather/', Weatherday.as_view(), name='weather'),
    path('csv/',csv_download,name='csv'),
]