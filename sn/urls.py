from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from rest_framework import routers

from api import views as api_views
from soc import views as socium_views

router = routers.DefaultRouter()
router.register(r'users', api_views.UserViewSet)
router.register(r'posts', api_views.PostViewSet)

urlpatterns = [
                  path('api/', include(router.urls)),
                  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

                  path('', socium_views.BoardListView.as_view(), name='home'),
                  path('admin/', admin.site.urls),

                  path('create/', socium_views.new_post, name='new-post'),
                  path('post/<int:pk>/', socium_views.PostDetailView.as_view(), name='post-detail'),

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
                  url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                      auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
                      name='password_reset_confirm'),
                  url('reset/complete/',
                      auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
                      name='password_reset_complete'),

                  path('bot/', include('bot.urls'), name='bot'),

                  path('users/', socium_views.UserListView.as_view(), name='users-list'),
                  path('user/<int:pk>/', socium_views.UserDetailView.as_view(),
                       name='user-detail'),
                  path('signup/', socium_views.signup, name='signup'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
