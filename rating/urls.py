from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReviewCreateApiView.as_view()),
    path('<int:pk>', views.ReviewUpdateApiView.as_view()),
]
