from django.db import models
from django.contrib.auth.models import User , Group


    
class SystemUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE,null=True,blank=True)
    entry = models.BooleanField(default=False)
    @property
    def user_name(self):
        return self.user.username

class FaceEncoding(models.Model):
    encoding = models.TextField()
    user = models.ForeignKey(SystemUser, on_delete=models.CASCADE, null=True)

    @property
    def user_name(self):
        return self.user.user.username if self.user else None
class Visits(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=512,null = True, blank = True)

