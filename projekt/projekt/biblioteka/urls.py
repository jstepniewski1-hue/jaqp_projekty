# plik biblioteka/urls.py

from django.urls import path, include
from . import views

urlpatterns = [
    path('books/', views.book_list),
    path('books/<int:pk>/', views.book_detail),
    path('books/update_delete/<int:pk>/', views.book_update_delete),
    path("welcome/", views.welcome_view),
    path("html/osoby/", views.osoba_list_html, name="osoba-list"),
    path("html/osoby/<int:id>/", views.osoba_detail_html, name="osoba-detail"),
    path("html/osoby/dodaj/", views.osoba_create_html, name="osoba-create"),
    path("html/osoby/dodaj_django/", views.osoba_create_django_form, name="osoba-create-django"),
    path('login/', views.user_login, name='user-login'),
    path('logout/', views.user_logout, name='user-logout'),
    
]
