# from paginas.views import MyPasswordResetConfirmView
from django.contrib.auth import views as auth_views
from django.urls import path, include
from paginas import views
from paginas.views import CustomPasswordResetConfirmView
# from .views import SignUpNameView, SignUpEmailView, SignUpPasswordView


urlpatterns = [
    path('', views.home, name='home_root'),
    path('', include('paginas.urls', namespace='home')),
    # path('login/', views.custom_login, name='login'),
    # path('signup/name/', SignUpNameView.as_view(), name='sign_up_name'),
    # path('signup/email/', SignUpEmailView.as_view(), name='sign_up_email'),
    # path('signup/password/', SignUpPasswordView.as_view(), name='sign_up_password'),

    path('signup/email/', views.signup_email, name='signup_email'),
    path('signup/name/', views.signup_name, name='signup_name'),
    path('signup/password/', views.signup_password, name='signup_password'),
    # Adicione outras URLs necessárias aqui


    # path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout_view'),
    path('home/', include('paginas.urls')),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('login/email/', views.email_login, name='login'),
    path('login/senha/', views.senha_login, name='senha_login'),
]
