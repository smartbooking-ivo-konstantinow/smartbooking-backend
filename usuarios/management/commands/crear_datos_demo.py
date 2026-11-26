from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from usuarios.models import Usuario

# ADVERTENCIA DE SEGURIDAD
# Estas credenciales son de DEMOSTRACIÓN: públicas a propósito y documentadas
# en el README para que el tribunal pueda probar la aplicación.
# NUNCA deben existir en un entorno de producción. Si el sistema se desplegara,
# estos usuarios deben eliminarse o sus contraseñas deben cambiarse de inmediato.
USUARIOS_DEMO = [
    {
        'email': 'admin@smartbooking.com',
        'password': 'Admin#2026',
        'first_name': 'Admin',
        'last_name': 'Demo',
        'es_admin': True,
    },
    {
        'email': 'prueba@mail.com',
        'password': 'Clave#123',
        'first_name': 'Ana',
        'last_name': 'Pérez',
        'es_admin': False,
    },
]


class Command(BaseCommand):
    help = 'Crea los usuarios de demostración (Administrador y Usuario).'

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError(
                'Este comando solo puede ejecutarse en desarrollo (DEBUG=True).'
            )

        for datos in USUARIOS_DEMO:
            if Usuario.objects.filter(email=datos['email']).exists():
                self.stdout.write(self.style.WARNING(f"Ya existe: {datos['email']}"))
                continue

            crear = (Usuario.objects.create_superuser if datos['es_admin']
                    else Usuario.objects.create_user)
            crear(
                email=datos['email'],
                password=datos['password'],
                first_name=datos['first_name'],
                last_name=datos['last_name'],
            )

            self.stdout.write(self.style.SUCCESS(f"Creado: {datos['email']}"))