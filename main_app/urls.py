from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('about/',views.about, name='about'),
    path('movies/<str:show_id>/', views.movie_detail, name='movie_detail'),
    path('movies/new/', views.movie_create, name='movie_create'),
    path('movies/<str:show_id>/edit/', views.movie_update, name='movie_update'),
    path('movies/<str:show_id>/delete/', views.movie_delete, name='movie_delete'),
]