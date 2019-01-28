from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.CharField(max_length = 48, primary_key = True)
    password = models.CharField(max_length = 48)

    def __str__(self):
        return self.user_id

#name.csv uploaded
class SpinGlassField(models.Model):
    name = models.CharField(max_length = 48)
    site_num = models.IntegerField(default = 20)
    trotter_num = models.IntegerField(default = 10)
    result = models.IntegerField(default = None, null = True, blank = True)
    data = models.FileField(null = True, blank = True, max_length=128)

    def __str__(self):
        return self.name
