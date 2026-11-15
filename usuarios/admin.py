from django.contrib import admin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'rol', 'is_active')   # TODO: las 5 columnas
    search_fields = ('email',)
    ordering = ('email',)