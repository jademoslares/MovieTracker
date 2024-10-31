from django.urls import path
from . import views
from django.conf.urls import handler404

urlpatterns = [
    path('',views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/',views.about, name='about'),
    path('movies/new/', views.movie_create, name='movie_create'),
    path('movies/<str:show_id>/', views.movie_detail, name='movie_detail'),
    path('movies/<str:show_id>/edit/', views.movie_update, name='movie_update'),
    path('movies/<str:show_id>/delete/', views.movie_delete, name='movie_delete'),
    path('profile/<str:user_name>/', views.profile, name='profile'),
    path('profile/<str:user_id>/edit/', views.profile_update, name='profile_update'),
    path('watchlist/add/<str:show_id>/<user_id>/<plan_to_do>', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/remove/<str:show_id>/<user_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('watchlist/update/<str:show_id>/<user_id>/<plan_to_do>/', views.update_watchlist, name='update_watchlist'),
    path('actors/new/', views.actor_create, name='actor_create'),
    path('genres/new/', views.genre_create, name='genre_create'),
]

handler404 = views.custom_404_view