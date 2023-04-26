from django.shortcuts import redirect


class StaffOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exceptions = ['/accounts/login/', '/accounts/signup/',
                      '/test/', '/reset_password/']  # adicionar a URL de cadastro aqui
        if not request.user.is_authenticated or not request.user.is_staff:
            if request.path not in exceptions:
                return redirect('login')
        response = self.get_response(request)
        return response
