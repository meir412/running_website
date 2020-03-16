from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('runs/', views.RunListView.as_view(), name='runs'),
    path('run/<int:pk>', views.RunDetailView.as_view(), name='run-detail'),
    # path('run/<int:pk>/changeduration/', views.change_run_duration, name='change-run-duration'),
    path('run/<int:pk>/changerun/', views.RunUpdate.as_view(), name='run-update'),
    path('run/<int:pk>/deleterun/', views.RunDelete.as_view(), name='run-delete'),
    path('addrun/', views.addNewRun, name='run-add'),
]
