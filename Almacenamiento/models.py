from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo_name = models.CharField(max_length=1000, null=True)
    status = models.BooleanField(default=False, null=True)
    hash_code = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.todo_name
    
    def __str__(self):
        return self.hash_code