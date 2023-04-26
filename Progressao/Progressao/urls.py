
from django.contrib import admin
from paginas import views
from django.urls import path, include


# app_name = 'paginas'


# urlpatterns = [
#     # path('admin/my-form/', MeuForm.as_view(), name='my-form'),
#     path('admin/', admin.site.urls),
#     path('home/', views.home, name='home'),
#     path('accounts/', include('django.contrib.auth.urls')),
#     path('accounts/login/',
#          auth_views.LoginView.as_view(template_name='login.html'), name='login'),
#     path('accounts/signup/', views.signup_view, name='signup'),
#     path('accounts/logout/', views.logout_view,
#          name='logout_view'),  # mudança aqui
#     path('reset_password/', views.password_reset, name='reset_password'),


# ]

from django.urls import path, include
from django.contrib.auth import views as auth_views
from paginas import views
from paginas.views import MyPasswordResetView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('accounts/', include(('django.contrib.auth.urls', 'auth'), namespace='auth')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/signup/', views.signup_view, name='signup'),
    path('accounts/logout/', views.logout_view, name='logout_view'),
    path('test/', views.test_view, name='test'),
    path('reset_password/', MyPasswordResetView.as_view(), name='reset_password'),




    #     path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
    #         template_name="password_reset_sent.html"), name="password_reset_done"),
    #     path('reset_password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    #         template_name="password_reset_form.html"), name="password_reset_confirm"),
    #     path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
    #         template_name="password_reset_complete.html"), name="password_reset_complete"),
]
