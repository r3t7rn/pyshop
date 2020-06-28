from django.db import models

class Product(models.Model):
    pname = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    price = models.FloatField()
    stock = models.SmallIntegerField()
    pclass = models.CharField(max_length=50)
    pdescribe = models.CharField(max_length=500)

    def __str__(self):
        return self.pname
