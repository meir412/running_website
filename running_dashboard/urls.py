from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('runs/', views.RunListView.as_view(), name='runs'),
    path('run/<int:pk>', views.RunDetailView.as_view(), name='run-detail'),
]
