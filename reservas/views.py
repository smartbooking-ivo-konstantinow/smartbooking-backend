from rest_framework import viewsets

from .models import Reserva
from .serializers import ReservaSerializer


class ReservaViewSet(viewsets.ModelViewSet):
    serializer_class = ReservaSerializer

    def get_queryset(self):
        usuario = self.request.user
        if usuario.rol == usuario.Rol.ADMIN:
            return Reserva.objects.all()
        return Reserva.objects.filter(usuario=usuario)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)