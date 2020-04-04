from django.urls import path

from . import views

app_name = 'zettelbox'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('box/<str:box_name>/', views.box, name='box'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('taufe/', views.taufe, name='taufe'),
    path('rename/', views.rename, name='rename'),
]
