from django.urls import path

from games import views

urlpatterns = [
    path('', views.index, name='index'),

    path('add_to_collection/', views.AddGameToCollection.as_view(),
         name='add-game-to-collection'),
    path('add_to_list/', views.AddGameToList.as_view(),
         name='add-game-to-list'),
    path('search/', views.SearchGames.as_view(),
         name='search'),
    path('<int:id>/', views.GameDetailView.as_view(),
         name='game-detail'),
]
