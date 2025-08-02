from rest_framework import serializers
from .models import Invitation
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = '__all__'
        read_only_fields = ['token', 'status', 'expiration_date']

class AcceptInvitationSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    password = serializers.CharField(write_only=True)

    def validate_token(self, value):
        try:
            invitation = Invitation.objects.get(token=value)
        except Invitation.DoesNotExist:
            raise serializers.ValidationError("Invalid token.")

        if invitation.status != 'Pending':
            raise serializers.ValidationError("Invitation is not pending.")
        if invitation.is_expired():
            raise serializers.ValidationError("Invitation has expired.")
        return value

    def save(self):
        token = self.validated_data['token']
        password = self.validated_data['password']
        invitation = Invitation.objects.get(token=token)

        user = User.objects.create(
            name=invitation.name,
            email=invitation.email,
            password=make_password(password)
        )
        invitation.status = 'Accepted'
        invitation.save()
        return user
