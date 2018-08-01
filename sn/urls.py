"""sn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include
from django.urls import path

from soc import views as socium_views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', socium_views.BoardListView.as_view(), name='home'),
                  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
                  path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
                  path('reset/',
                       auth_views.PasswordResetView.as_view(
                           template_name='password_reset.html',
                           email_template_name='password_reset_email.html',
                           subject_template_name='password_reset_subject.txt'
                       ),
                       name='password_reset'),
                  path('settings/account/', socium_views.UserUpdateView.as_view(), name='my_account'),
                  path('settings/password/',
                       auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
                       name='password_change'),
                  path('settings/password/done/',
                       auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
                       name='password_change_done'),
                  path('reset/done/',
                       auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
                       name='password_reset_done'),
                  path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                       auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
                       name='password_reset_confirm'),
                  path('bot/', include('bot.urls'), name='bot'),

                  path('users/', socium_views.UserListView.as_view(), name='users-list'),

                  path('user/<int:pk>/', socium_views.UserDetailView.as_view(),
                       name='user-detail'),
                  path('signup/', socium_views.signup, name='signup'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
