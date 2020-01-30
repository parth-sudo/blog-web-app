
"""project_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('', include('users.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/post/new/logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('logout/login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('profile/logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

path('password-reset/',
     auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
     name='password_reset'),

path('password-reset/done',
     auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
     name='password_reset_done'), #email and password reset url.

path('password-reset-confirm/<uidb64>/<token>/', #confirmation takes 2 extra parameters, "uidb & token".
     auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
     name='password_reset_confirm'),

path('password-reset-complete/<uidb64>/<token>/', #password reset confirmation takes 2 extra parameters, "uidb & token".
     auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
     name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)