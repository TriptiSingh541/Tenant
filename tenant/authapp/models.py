from django.db import models
from home.models import User 

class PermissionAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tenant = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    product_id = models.CharField(max_length=100)
    feature = models.CharField(max_length=100)
    permission = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.feature} - {self.permission}"
