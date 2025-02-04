from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),

    path('famille/', views.famille, name="famille"),
    path('modele/', views.modele, name="modele"),
]