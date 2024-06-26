"""
URL configuration for billiardportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from core.views import CustomLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('about/', TemplateView.as_view(template_name="about.html"), name='about'),
    path('privacy/', TemplateView.as_view(template_name="privacy_policy.html"), name='privacy'),
    path('copyright/', TemplateView.as_view(template_name="copyright.html"), name='copyright'),
    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("player/", include("core.urls")),
    path("tournament/", include("tournaments.urls")),
]

admin.site.site_header = "BilliardPortal administration"
admin.site.index_title = "Administration BilliardPortal"