from django.urls import path

from igdb import views

urlpatterns = [
    path('genres/', views.GenresList.as_view(), name='genres'),
    path('platforms/', views.PlatformsList.as_view(), name='platforms'),

    path('update_genres/', views.update_genres, name='update-genres'),
    path('update_platforms/', views.update_platforms, name='update-platforms'),
]
