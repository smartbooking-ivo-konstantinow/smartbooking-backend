from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegistroSerializer


class RegistroView(generics.CreateAPIView):
    serializer_class = RegistroSerializer
    permission_classes = [AllowAny]
    
class LogoutView(APIView):

    def post(self, request):
        refresh = request.data.get('refresh')
        if not refresh:
            return Response(
                {'detail': 'El refresh token es obligatorio.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh)
        except TokenError:
            return Response(
                {'detail': 'El token es inválido o ya fue anulado.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if str(token['user_id']) != str(request.user.id):
            return Response(
                {'detail': 'No podés cerrar la sesión de otro usuario.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        token.blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)