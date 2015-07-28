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

    def list_parents(self):
        res = []
        good = self
        while good.parent:
            res.append(good.parent)
            good = good.parent
        return res

    def list_costs(self):
        """
        $id = (int)$id;
        $node = $this->db->selectRow("SELECT * FROM goods WHERE id={$id}");
        if ($node['packed']) {
            return $this->db->select(
                "SELECT b.title, a.timestamp, ROUND(a.cost/a.amount, 2) as pack_cost, ROUND(a.cost/a.amount/sg.pack_volume, 2) as unit_cost
               FROM goods g
                    JOIN sales a ON g.id=a.good_id
                    JOIN goods sg ON a.good_id=sg.id
                    JOIN shops b ON a.shop_id=b.id
              WHERE {$node['node_left']}<=g.node_left AND g.node_right<={$node['node_right']}
           ORDER BY a.timestamp DESC"
            );
        } else {
            return $this->db->select(
                "SELECT b.title, a.timestamp, ROUND(a.cost/a.amount/sg.pack_volume, 2) as unit_cost
               FROM goods g
                    JOIN sales a ON g.id=a.good_id
                    JOIN goods sg ON a.good_id=sg.id
                    JOIN shops b ON a.shop_id=b.id
              WHERE {$node['node_left']}<=g.node_left AND g.node_right<={$node['node_right']}
           ORDER BY a.timestamp DESC"
            );
        }
        """
        if self.packed:
            def cb(cost):
                cost.pack_cost = "%.2f" % (cost.cost/cost.amount)
                cost.unit_cost = "%.2f" % (cost.cost/cost.amount/cost.good.pack_volume)
                return cost
        else:
            def cb(cost):
                cost.unit_cost = "%.2f" % (cost.cost/cost.amount/cost.good.pack_volume)
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
