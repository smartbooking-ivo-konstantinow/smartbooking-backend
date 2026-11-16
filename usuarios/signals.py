import logging

from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver

logger = logging.getLogger('security')


@receiver(user_login_failed)
def registrar_login_fallido(sender, credentials, request=None, **kwargs):
    email = credentials.get('email')
    ip = request.META.get('REMOTE_ADDR') if request else None
    recurso = request.path if request else None
    logger.warning(
        'email=%s accion=login recurso=%s resultado=fallido ip=%s',
        email, recurso, ip,
    )