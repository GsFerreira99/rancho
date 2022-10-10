from django.urls import path
from site_publico import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
]