from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.BookListView.as_view(), name='list'),
    path('add/', views.BookCreateView.as_view(), name='add'),
    path('<uuid:pk>/', views.BookDetailView.as_view(), name='detail'),
    path('<uuid:pk>/edit/', views.BookEditView.as_view(), name='edit'),
    path('<uuid:pk>/delete/', views.BookDeleteView.as_view(), name='delete'),
]
