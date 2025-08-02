from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PermissionAccess
from .serializers import CheckPermissionSerializer

class CheckPermissionView(APIView):
    def post(self, request):
        serializer = CheckPermissionSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            exists = PermissionAccess.objects.filter(
                user_id=data['user_id'],
                tenant=data['tenant'],
                role=data['role'],
                product_id=data['product_id'],
                feature=data['feature'],
                permission=data['permission']
            ).exists()

            return Response({'allowed': exists}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
