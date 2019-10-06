from django.urls import path
from . import views


urlpatterns = [
    path('music/', views.SongsListAPIView.as_view(), name="songs-list"),
    path('music/<int:pk>/', views.SongsDetailAPIView.as_view(), name="songs-detail"),
]
