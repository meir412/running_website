from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('allruns/', views.runSummary, name='run-summary'),
    path('runs/', views.RunListView.as_view(), name='runs'),
    path('run/<int:pk>', views.RunDetailView.as_view(), name='run-detail'),
    # path('run/<int:pk>/changeduration/', views.change_run_duration, name='change-run-duration'),
    path('run/<int:pk>/changerun/', views.RunUpdate.as_view(), name='run-update'),
    path('run/<int:pk>/deleterun/', views.RunDelete.as_view(), name='run-delete'),
    path('addrun/', views.addNewRun, name='run-add'),
    path('signup/', views.signUp, name='sign-up'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.activate, name='activate'),
    path('loggedin/', views.loggedIn, name='logged-in'),
]
