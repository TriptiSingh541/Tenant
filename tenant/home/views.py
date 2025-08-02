from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Invitation,User
from .serializers import InvitationSerializer, AcceptInvitationSerializer
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
from .permissions import check_permission
import logging
from django.http import JsonResponse
from .services import call_auth_service

def check_auth_view(request):
    try:
        response=call_auth_service()
        return JsonResponse({'status':'success','auth_status':response.status_code})
    except Exception as e:
        return JsonResponse({"status":'erroe','message':str(e)},status=503)
    
class DashboardView(APIView):
    @check_permission(product_id="abc", feature="dashboard", permission="read")
    def get(self, request):
        return Response({"message": "Welcome to the dashboard!"}, status=status.HTTP_200_OK)

logger = logging.getLogger("home")

class LoggingView(APIView):
    def get(self, request):
        logger.info("Dashboard accessed", extra={
            "trace_id": getattr(request, "trace_id", None),
            "service": "home",
            "user_id": getattr(request.user, "id", None),
            "tenant_id": request.headers.get("X-Tenant-ID")
        })
        return Response({"message": "Welcome to the dashboard!"}, status=status.HTTP_200_OK)

class CreateInvitationAPIView(APIView):
    def post(self, request):
        data = request.data.copy()
        data['expiration_date'] = timezone.now() + timedelta(days=7)
        data['status'] = 'Pending'
        data['metadata'] = {
            'ip': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT')
        }
        serializer = InvitationSerializer(data=data)
        if serializer.is_valid():
            invitation=serializer.save()
            #  for Sending  email with invitation token
            subject = "You're invited!"
            message = f"""
            Hi {invitation.name},

            You have been invited to join. Please use the following token to accept the invitation:

            Token: {invitation.token}

            This token will expire on {invitation.expiration_date}.

            Thank you!
            """
            recipient_list = [invitation.email]
            from_email = settings.DEFAULT_FROM_EMAIL

            send_mail(subject, message, from_email, recipient_list)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AcceptInvitationAPIView(APIView):
    def post(self, request):
        serializer = AcceptInvitationSerializer(data=request.data)
        if serializer.is_valid():
            invitation = Invitation.objects.get(token=request.data.get("token"))

            # Check if user already exists
            if User.objects.filter(email=invitation.email).exists():
                return Response(
                    {'error': 'User with this email already exists.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.create(
                name=invitation.name,
                email=invitation.email,

                password=make_password(request.data.get("password"))
            )
            invitation.status = 'Accepted'
            invitation.save()

            return Response({'message': 'Invitation accepted. User created.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CancelInvitationAPIView(APIView):
    def post(self, request):
        token = request.data.get('token')
        try:
            invitation = Invitation.objects.get(token=token)
        except Invitation.DoesNotExist:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_404_NOT_FOUND)

        invitation.status = 'Canceled'
        invitation.save()
        return Response({'message': 'Invitation canceled.'}, status=status.HTTP_200_OK)
