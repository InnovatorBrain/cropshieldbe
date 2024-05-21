from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import ClaimApplication
from .serializers import ClaimApplicationSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import generics

class ClaimApplicationCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id 
        serializer = ClaimApplicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClaimApplicationDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = ClaimApplication.objects.all()
    serializer_class = ClaimApplicationSerializer
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return ClaimApplication.objects.filter(user=self.request.user)
        else:
            return ClaimApplication.objects.none()


# Manage Claims Applications
class ManageClaimApplicationsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClaimApplicationSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return ClaimApplication.objects.filter(user=self.request.user)
        else:
            return ClaimApplication.objects.none()
    

class ClaimApplicationCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id 
        serializer = ClaimApplicationSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)