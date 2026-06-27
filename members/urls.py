from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('', views.MemberListView.as_view(), name='list'),
    path('add/', views.MemberCreateView.as_view(), name='add'),
    path('<uuid:pk>/', views.MemberDetailView.as_view(), name='detail'),
    path('<uuid:pk>/edit/', views.MemberEditView.as_view(), name='edit'),
    path('<uuid:pk>/delete/', views.MemberDeleteView.as_view(), name='delete'),
]
