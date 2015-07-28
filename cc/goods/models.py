from django.db import models
from django.contrib.auth.models import User
import decimal

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

    def list_parents(self):
        res = []
        good = self
        while good.parent:
            res.append(good.parent)
            good = good.parent
        return res

    def list_costs(self):
        if self.packed:
            def cb(cost):
                try:
                    cost.pack_cost = "%.2f" % (cost.cost/cost.amount)
                except decimal.DivisionByZero:
                    cost.pack_cost = 'n/a'

                try:
                    cost.unit_cost = "%.2f" % (cost.cost/cost.amount/cost.good.pack_volume)
                except decimal.DivisionByZero:
                    cost.unit_cost = 'n/a'
                return cost
        else:
            def cb(cost):
                try:
                    cost.unit_cost = "%.2f" % (cost.cost/cost.amount/cost.good.pack_volume)
                except decimal.DivisionByZero:
                    cost.unit_cost = 'n/a'
                return cost
        return self._traverse_costs(self, cb)

    def _traverse_costs(self, good, callback):
        res = []
        for cost in Cost.objects.filter(good=good):
            res.append(callback(cost))
        for child in Good.objects.filter(parent=good):
            res += self._traverse_costs(child, callback)
        return res

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
        return self.good.title + ', ' + self.shop.title + ', ' + str(self.cost)
