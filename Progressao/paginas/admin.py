from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

class MeuModeloAdmin(admin.ModelAdmin):
    def meu_form_link(self):
        url = reverse('meu_form')
        return format_html(f'<a href="{url}">Meu formulário personalizado</a>')
    meu_form_link.short_description = 'Formulário personalizado'
    meu_form_link.allow_tags = True
    meu_form_link.admin_order_field = 'id'

    list_display = ('id', 'campo1', 'campo2', 'meu_form_link')