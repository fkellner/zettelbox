from django.urls import path

from . import views

app_name = 'zettelbox'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('box/<str:box_name>/', views.box, name='box'),
    path('box/<str:box_name>/add', views.addPaper, name='add_paper'),
    path('box/<str:box_name>/delete/<int:paper_id>', views.deletePaper, name='delete_paper'),
    path('box/<str:box_name>/insert/<int:paper_id>', views.insertPaper, name='insert_paper'),
    path('box/<str:box_name>/insertAll>', views.insertAll, name='insert_all'),
    path('box/<str:box_name>/forceInsertAll>', views.forceInsertAll, name='force_insert_all'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('taufe/', views.taufe, name='taufe'),
    path('rename/', views.rename, name='rename'),
]
