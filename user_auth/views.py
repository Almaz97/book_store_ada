from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status, exceptions, generics, response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


from .serializers import RegisterSerializer, LoginSerializer


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'],
                            password=serializer.validated_data['password'])

        if not user:
            raise exceptions.AuthenticationFailed()
        user.last_login = timezone.now()
        user.save()

        token, _ = Token.objects.get_or_create(user=user)

        return response.Response(data={"token": token.key},
                                 status=status.HTTP_200_OK)
