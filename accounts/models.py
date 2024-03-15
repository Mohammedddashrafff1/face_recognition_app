from django.db import models
from django.contrib.auth.models import Group,User
from django.utils import timezone
import os





def image_upload_path(instance, filename):
    # Define the upload path based on system_user_name
    person_directory = instance.person.system_user_name
    return os.path.join('training_directory', person_directory, filename)



# Create your models here.
class System_Group(models.Model):
    group =  models.ForeignKey(Group,on_delete=models.CASCADE)
    group_description = models.TextField(null = True, blank = True)
    group_domain = models.CharField(max_length=512)
    group_admin = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.group.name




class System_User(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    group = models.ForeignKey(System_Group, on_delete=models.CASCADE)
    system_user_name = models.CharField(max_length=512,null = True, blank = True)



    def __str__(self):
        return self.system_user_name
    
    
    class MPTTMeta:
        order_insertion_by = ['system_user_name']
        
        
class Person(models.Model):
    
    system_user_name = models.CharField(max_length=512,null = True, blank = True)
    entry = models.BooleanField(default=False)





    def __str__(self):
        return self.system_user_name
    
    
    class MPTTMeta:
        order_insertion_by = ['system_user_name']        
        
        
class Image(models.Model):
    person = models.ForeignKey(Person, related_name='images', on_delete=models.CASCADE)
    document_file = models.ImageField(upload_to=image_upload_path)

class Attendance(models.Model):
    date = models.DateField(default=timezone.now)  # Assuming you want to set the current date as the default
    entry_time = models.TimeField(default=timezone.now)  # Assuming you want to set the current time as the default
    exit_time = models.TimeField(blank=True, null=True)
    person = models.ForeignKey(Person, related_name='attendances', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.person.system_user_name} - {self.date}"