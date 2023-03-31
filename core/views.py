from django.contrib.auth import get_user_model, authenticate, login
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, RegistrationSerializer
from rest_framework.authtoken.models import Token

User = get_user_model()

@api_view(['GET'])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    """
    REST API view for user login.
    """
    # Get username and password from request data
    username = request.data.get('username')
    password = request.data.get('password')

    # Authenticate user
    user = authenticate(request, username=username, password=password)

    # If authentication successful
    if user is not None:
        # Log in user
        login(request, user)

        # Generate and return auth token
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

    # If authentication unsuccessful
    else:
        return Response({'error': 'Invalid credentials'})