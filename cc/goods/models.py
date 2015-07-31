from django.db import models
from django.contrib.auth.models import User
import decimal
import uuid
import os

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('good_images', filename)

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
            res.insert(0, good.parent)
            good = good.parent
        return res

    def list_costs(self):
        return self._traverse_costs(self)

    def min_max_cost(self):
        _min = None
        _max = None

        def cb(cost):
            nonlocal _min, _max
            try:
                if _min is None or cost.unit_cost() < _min.unit_cost():
                    _min = cost
                if _max is None or cost.unit_cost() > _max.unit_cost():
                    _max = cost
            except:
                pass

        self._traverse_costs(self, cb)
        return _min, _max

    def list_children(self):
        children = Good.objects.filter(parent=self)
        for child in children:
            _min, _max = child.min_max_cost()
            child.min = _min
            child.max = _max
        return children

    def _traverse_costs(self, good, callback=None):
        res = []
        for cost in Cost.objects.filter(good=good):
            if callback is None:
                res.append(cost)
            else:
                res.append(callback(cost))
        for child in Good.objects.filter(parent=good):
            res += self._traverse_costs(child, callback)
        return res

    def get_absolute_url(self):
        return '/goods/view/%i' % self.id

    def __str__(self):
        return self.title

class GoodImage(models.Model):
    image = models.ImageField(upload_to=get_file_path)
    good = models.ForeignKey(Good)

class Cost(models.Model):
    good = models.ForeignKey(Good)
    shop = models.ForeignKey(Shop)
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    discount = models.BooleanField(default=False)

    def unit_cost(self):
        return self.cost/self.amount/self.good.pack_volume

    def unit_cost_str(self):
        try:
            return "%.2f" % (self.unit_cost())
        except decimal.DivisionByZero:
            return 'n/a'

    def pack_cost(self):
        return self.cost/self.amount

    def pack_cost_str(self):
        try:
            return "%.2f" % (self.pack_cost())
        except decimal.DivisionByZero:
            return 'n/a'

    def __str__(self):
        return self.good.title + ', ' + self.shop.title + ', ' + str(self.cost)
