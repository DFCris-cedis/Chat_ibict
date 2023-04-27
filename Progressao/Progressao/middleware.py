from django.shortcuts import redirect


class StaffOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exceptions = ['/accounts/login/', '/accounts/signup/','/accounts/reset_password/', '/accounts/reset_password/done/','/accounts/password_reset/<uidb64>/<token>/','/accounts/reset/done/',
                      '/accounts/password_reset_confirm/<uidb64>/<token>/','/accounts/reset/NQ/set-password/','/accounts/password_reset_confirm/NQ/bnbtit-57e083958c9392367b963d7db7bfd7c6/ HTTP/1.1']  # adicionar a URL de cadastro aqui
        if not request.user.is_authenticated or not request.user.is_staff:
            if request.path not in exceptions:
                return redirect('login')
        response = self.get_response(request)
        return response
