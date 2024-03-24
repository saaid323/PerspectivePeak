from django.db import models
from django.contrib.auth.models import User
import readtime
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, null=False)
    body = CKEditor5Field('Text', config_name='extends')
    header_image = models.ImageField(null=True, blank=True, upload_to='images/header')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at', '-created_at']
    
    def get_readtime(self):
        result = readtime.of_text(self.body)
        return result.text 

    def __str__(self) -> str:
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='images/users/default.jpg', upload_to='images/users')
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username
