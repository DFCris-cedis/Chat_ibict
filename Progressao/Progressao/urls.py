from django.contrib import admin
from django.urls import path
from paginas import views
from django.urls import path, include
from paginas import views as user_views
from django.contrib.auth.views import LoginView, LogoutView
from paginas.views import signup_view, logout_view
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_views
app_name = 'paginas'
from django.urls import path
from paginas.views import CustomPasswordResetForm


urlpatterns = [
    # path('admin/my-form/', MeuForm.as_view(), name='my-form'),
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/signup/', views.signup_view, name='signup'),
    path('accounts/logout/', views.logout_view, name='logout_view'), # mudança aqui
    # path('password_reset/', auth_views.LoginView.as_view(template_name='password_reset_email.html'), name='password_reset_email'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_email.html'), name='password_reset_email'),

    # path('password_reset/',
    #      auth_views.PasswordResetView.as_view(
    #          form_class=CustomPasswordResetForm,
    #          template_name='password_reset_email.html'
    #      ),
    #      name='password_reset_email'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

]


    
  
    


