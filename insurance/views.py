from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import PolicyApplication
from .serializers import PolicyApplicationSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import RetrieveUpdateDestroyAPIView

class PolicyApplicationCreate(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = PolicyApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PolicyApplicationDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = PolicyApplication.objects.all()
    serializer_class = PolicyApplicationSerializer