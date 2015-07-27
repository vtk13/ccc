from django.db import models
from django.contrib.auth.models import User

class Unit(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Shop(models.Model):
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Good(models.Model):
    bar_code = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    parent = models.ForeignKey('self', null=True, blank=True)
    unit = models.ForeignKey(Unit)
    packed = models.BooleanField(default=False)
    pack_volume = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return self.title

class Cost(models.Model):
    good = models.ForeignKey(Good)
    shop = models.ForeignKey(Shop)
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    discount = models.BooleanField(default=False)

    def __str__(self):
        return self.good.title + self.cost
