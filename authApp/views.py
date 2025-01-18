from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import BeaconUserSerializer, BeaconDeviceSerializer
from .models import BeaconUser, BeaconDevice

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': BeaconUserSerializer(user).data
            })
        return Response({'error': 'Invalid credentials'}, status=400)

@api_view(['POST'])
def register_user(request):
    serializer = BeaconUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BeaconDeviceViewSet(viewsets.ModelViewSet):
    queryset = BeaconDevice.objects.all()
    serializer_class = BeaconDeviceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return BeaconDevice.objects.all()
        return BeaconDevice.objects.filter(created_by=self.request.user)