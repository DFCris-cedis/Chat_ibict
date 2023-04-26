from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.urls import PasswordResetView
from django.contrib.auth.views import PasswordResetView
from paginas import views

# urlpatterns = [
#     path('', include('paginas.urls', namespace='home')),
#     path('login/', views.login_view, name='login'),
#     path('signup/', views.signup_view, name='signup'),
#     path('logout/', views.logout_view, name='logout_view'),
#     path('home/', include('paginas.urls')),
#     path('accounts/password_reset/',
#          auth_views.PasswordResetView.as_view(), name='password_reset'),
# ]

# path('reset_password_sent/', views.password_reset_done,
#      name='password_reset_done'),
# # path('reset/<uidb64>/<token>/', views.password_reset_confirm,
# #      name='password_reset_confirm'),
# path('reset_password_complete/', views.password_reset_complete,
#      name='password_reset_complete'),

from django.urls import path, include
from django.contrib.auth import views as auth_views
from paginas import views

# urlpatterns = [
#     path('', include('paginas.urls', namespace='home')),
#     path('login/', views.login_view, name='login'),
#     path('signup/', views.signup_view, name='signup'),
#     path('logout/', views.logout_view, name='logout_view'),
#     path('home/', include('paginas.urls')),
#     path('password_reset/', views.password_reset, name="password_reset"),
# ]
from django.urls import path, include
from django.contrib.auth import views as auth_views
from paginas import views
from .views import MyPasswordResetView

urlpatterns = [
    path('', include('paginas.urls', namespace='home')),
    path('test/', views.test_view, name='test'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout_view'),
    path('home/', include('paginas.urls')),
    path('reset_password/', MyPasswordResetView.as_view(), name='reset_password'),

]
