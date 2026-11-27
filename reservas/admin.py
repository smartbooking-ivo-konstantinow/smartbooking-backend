from django.contrib import admin

from .models import Reserva


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'hora_inicio', 'hora_fin', 'usuario', 'motivo')
    list_filter = ('fecha',)
    ordering = ('fecha', 'hora_inicio')