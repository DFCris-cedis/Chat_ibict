#from paginas.views import MyPasswordResetConfirmView
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.contrib import admin
from paginas import views
#from paginas.views import CustomPasswordResetView
# from paginas.views import CustomPasswordResetConfirmView
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('login'), name='login'),
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('accounts/', include(('django.contrib.auth.urls', 'auth'), namespace='auth')),
    # path('accounts/login/', views.custom_login, name='login'),
    # path('accounts/signup/', views.signup_view, name='signup'),
    path('signup/email/', views.signup_email, name='signup_email'),
    path('signup/name/', views.signup_name, name='signup_name'),
    path('signup/password/', views.signup_password, name='signup_password'),
    path('accounts/logout/', views.logout_view, name='logout_view'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # #path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    # path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('login/email/', views.email_login, name='login'),
    path('login/senha/', views.senha_login, name='senha_login'),
    path('conheca_mais/', views.conheca_mais, name='conheca_mais'),
    path('contate_nos/', views.contate_nos, name='contate_nos'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
]