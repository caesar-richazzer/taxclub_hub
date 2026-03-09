from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenRefreshView,
)
from . import views

urlpatterns = [
    # ── HTML Pages (The UI) ──────────────────────────────────
    path('', views.HomeLandingView.as_view(), name='home'),
    path('login-ui/', views.LoginPageView.as_view(), name='login-page'),
    path('register-ui/', views.RegisterPageView.as_view(), name='register-page'),

    # ── API Endpoints (The Logic) ────────────────────────────
    path('api/register/', views.RegisterView.as_view(), name='api-register'),
    path('api/profile/', views.ProfileView.as_view(), name='api-profile'),
    

    # JWT Auth (The ones that were causing the crash)
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]