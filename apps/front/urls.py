from django.urls import path
from front import views


urlpatterns = [
    path('lobby/', views.lobby, name='lobby'),
    path('game/<int:id>/', views.game, name='game')
]