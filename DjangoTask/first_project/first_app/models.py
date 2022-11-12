from django.db import models

# Create your models here.
class FileContent(models.Model):
    Category=models.CharField(max_length=10)
    X=models.IntegerField()
    Y=models.IntegerField()

    def __str__(self):
      return self.Category