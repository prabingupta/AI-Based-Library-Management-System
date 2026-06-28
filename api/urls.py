from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

app_name = "api"

router = DefaultRouter()
router.register(r"books", views.BookViewSet, basename="book")
router.register(r"authors", views.AuthorViewSet, basename="author")
router.register(r"categories", views.CategoryViewSet, basename="category")
router.register(r"publishers", views.PublisherViewSet, basename="publisher")
router.register(r"members", views.MemberViewSet, basename="member")
router.register(r"borrow-records", views.BorrowRecordViewSet, basename="borrow-record")

urlpatterns = [
    path("", include(router.urls)),
    # JWT Auth
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # Custom endpoints
    path("dashboard/stats/", views.DashboardStatsAPIView.as_view(), name="dashboard_stats"),
    path("search/", views.SearchAPIView.as_view(), name="search"),
]
