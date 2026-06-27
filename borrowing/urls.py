from django.urls import path
from . import views

app_name = 'borrowing'

urlpatterns = [
    path('', views.BorrowListView.as_view(), name='list'),
    path('issue/', views.IssueBookView.as_view(), name='issue'),
    path('<uuid:pk>/', views.BorrowDetailView.as_view(), name='detail'),
    path('<uuid:pk>/return/', views.ReturnBookView.as_view(), name='return'),
    path('<uuid:pk>/renew/', views.RenewBookView.as_view(), name='renew'),
]
