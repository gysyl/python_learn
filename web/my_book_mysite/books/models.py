from django.db import models

# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=100,null=False)
    author = models.CharField(max_length=100,null=False)
    pub_time = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=5,decimal_places=2,null=False)
    
