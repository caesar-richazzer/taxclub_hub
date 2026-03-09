from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser, UserRole
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth.mixins import LoginRequiredMixin

# --- HTML TEMPLATE VIEWS (The Pages) ---

class HomeLandingView(TemplateView):
    template_name = "home.html"

class LoginPageView(TemplateView):
    template_name = "accounts/login.html"

class RegisterPageView(TemplateView):
    template_name = "accounts/register.html"

# This is the one that was missing!
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"
    login_url = '/login-ui/' # Redirects here if not logged in

# --- API VIEWS (The Data) ---

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user