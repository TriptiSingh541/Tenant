from rest_framework import serializers

class CheckPermissionSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    tenant = serializers.CharField()
    role = serializers.CharField()
    product_id = serializers.CharField()
    feature = serializers.CharField()
    permission = serializers.CharField()
