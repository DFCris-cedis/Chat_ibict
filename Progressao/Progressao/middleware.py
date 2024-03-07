# from django.shortcuts import redirect

# class StaffOnlyMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

    # def __call__(self, request):
    #     exceptions = [
            
    #         '/accounts/login/',
    #         '/accounts/signup/',
    #         '/accounts/password_reset/',
    #         '/accounts/password_reset/done/',
    #         '/accounts/reset/<uidb64>/<token>/',
    #         '/accounts/password_reset_confirm/',
    #         '/accounts/password_reset_form/',
    #         '/reset/done/',
    #         '/reset/<uidb64>/<token>/',
    #         '/password_reset/'
    #     ]  # adicionar a URL de cadastro aqui

    #     if not request.user.is_authenticated:
    #         if request.path not in exceptions and 'accounts/reset/<uidb64>/<token>' not in request.path:
    #             return redirect('login')


    #     response = self.get_response(request)
    #     return response

# class StaffOnlyMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Lógica antes da view ser chamada

#         response = self.get_response(request)

#         # Lógica após a view ser chamada

#         return response

#     # Você pode adicionar outros métodos de middleware conforme necessário
# from django.shortcuts import redirect
# from django.urls import resolve

# class StaffOnlyMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Lista de URLs que não exigem autenticação
#         exceptions = [
#             'login',  # Assumindo que 'login' é o nome da URL de login
#             'signup',
#             'password_reset',
#             'password_reset_done',
#             'password_reset_confirm'
#             # Adicione outros nomes de URL para suas páginas de exceção aqui
#         ]

#         if not request.user.is_authenticated:
#             # Resolve o nome da URL atual
#             url_name = resolve(request.path_info).url_name
#             # Se a URL atual não estiver nas exceções, redireciona para login
#             if url_name not in exceptions:
#                 return redirect('login')  # Garanta que 'login' é o nome correto da sua URL de login

#         # Chama a próxima função/middleware na cadeia
#         response = self.get_response(request)
#         return response
from django.shortcuts import redirect
from django.urls import resolve

class StaffOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Lista de nomes de URLs que não exigem autenticação
        exceptions = [
            'login',
            'signup',
            'password_reset',
            'password_reset_done',
            'password_reset_confirm',
            'password_reset_complete',
            'manual_de_uso',
            'sucesso_cadastro',
            'duvidas_frequentes',
            'signup_password',
            'signup_name',
            'signup_email',
            'senha_login',
            'contate_nos',
            'conheca_mais'

        ]

        # Verifica se o usuário está autenticado
        if not request.user.is_authenticated:
            # Resolve o nome da URL atual
            url_name = resolve(request.path_info).url_name
            # Se a URL atual não estiver nas exceções, redireciona para login
            if url_name not in exceptions:
                return redirect('login')  # Garanta que 'login' é o nome correto da sua URL de login

        response = self.get_response(request)
        return response
