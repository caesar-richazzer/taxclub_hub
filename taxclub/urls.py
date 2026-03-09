from django.contrib import admin
from django.urls import path, include # <--- You must import 'include'

urlpatterns = [
    # 1. The Admin Panel
    path('admin/', admin.site.urls),

    # 2. Connect the Accounts App
    # This tells Django: "For any URL not starting with admin/, check accounts/urls.py"
    path('', include('accounts.urls')), 
]