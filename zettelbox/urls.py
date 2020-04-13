from django.urls import path

from . import views

app_name = 'zettelbox'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('box/<str:box_name>/', views.box, name='box'),
    path('box/<str:box_name>/signup', views.signUp, name='sign_up'),
    path('box/<str:box_name>/random', views.getRandom, name='random'),
    path('box/<str:box_name>/insert/<int:paper_id>', views.insertPaper, name='insert_paper'),
    path('box/<str:box_name>/confirm/<int:paper_id>', views.confirmPaper, name='confirm_paper'),
    path('box/<str:box_name>/forceInsertAll>', views.forceInsertAll, name='force_insert_all'),
]
