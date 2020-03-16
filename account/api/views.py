from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from account.api.serializers import RegistrationSerializer
from datetime import datetime

# Returns the token if valid email and password is provided
class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        account = serializer.validated_data['user'] # Get the user
        Token.objects.get(user=account).delete() # Delete the old token
        token = Token.objects.create(user=account) # Create a new token
        data = {
            'token': token.key,
            'user_id': account.pk,
            'email': account.email
        }
        account.last_login = datetime.now() # Update last_login
        account.save()
        return Response(data)

# Requires email, password, password2
class Register(APIView):

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {} # This is what we'll return to the view
        if serializer.is_valid():
            account = serializer.save()
            data['email'] = account.email
            data['user_id'] = account.pk
            token = Token.objects.get(user=account)
            data['token'] = token.key
        else:
            # If the serializer throws any errors, return the error
            data = serializer.errors
        return Response(data=data, status=status.HTTP_201_CREATED)
