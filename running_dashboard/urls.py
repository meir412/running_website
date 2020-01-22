from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('runs/', views.RunListView.as_view(), name='runs')
]