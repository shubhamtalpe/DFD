from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'Home'),
    path('predict/', views.predict, name = "Predict"),
    path('mission/', views.mission, name = "Mission"),
    path('aboutus/', views.aboutus, name = "Aboutus")
]