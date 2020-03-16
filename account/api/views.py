from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

# Returns the token if valid email and password is provided
class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        account = serializer.validated_data['user']
        token = Token.objects.get(user=account)
        data = {
            'token': token.key,
            'user_id': account.pk,
            'email': account.email
        }
        return Response(data)
