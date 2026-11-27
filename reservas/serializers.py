from datetime import datetime

from django.utils import timezone
from rest_framework import serializers

from .models import Reserva


class ReservaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reserva
        fields = ('id', 'usuario', 'fecha', 'hora_inicio', 'hora_fin', 'motivo')
        read_only_fields = ('usuario',)

    def validate(self, data):
        fecha = data['fecha']
        hora_inicio = data['hora_inicio']
        hora_fin = data['hora_fin']

        # RN03: la hora de fin debe ser posterior a la de inicio
        if hora_fin <= hora_inicio:
            raise serializers.ValidationError(
                {'hora_fin': 'La hora de fin debe ser posterior a la de inicio.'}
            )

        # RN02: no se puede reservar en el pasado
        inicio = timezone.make_aware(datetime.combine(fecha, hora_inicio))
        if inicio < timezone.now():
            raise serializers.ValidationError(
                {'fecha': 'No se puede reservar en una fecha u horario pasados.'}
            )

        # RN01: no puede superponerse con otra reserva de la sala
        superpuestas = Reserva.objects.filter(
            fecha=fecha,
            hora_inicio__lt=hora_fin,
            hora_fin__gt=hora_inicio,
        )
        if self.instance:
            superpuestas = superpuestas.exclude(pk=self.instance.pk)
        if superpuestas.exists():
            raise serializers.ValidationError(
                'La sala ya está reservada en esa franja horaria.'
            )

        return data