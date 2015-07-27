from django.forms import Form, CharField, BooleanField, ChoiceField, DecimalField
from .models import Unit, Good, Shop

def num(s):
    try:
        return int(s)
    except ValueError:
        return 0

class ShopForm(Form):
    address = CharField(label='Адрес')
    title = CharField(label='Название')


class GoodForm(Form):
    bar_code = CharField(label='Штрих-код', required=False)
    title = CharField(label='Название')
    parent = ChoiceField(label='Группа', required=False)
    packed = BooleanField(label='Продается ли товар в фиксированной упаковке?', required=False)
    unit = ChoiceField(
        label='Единица измерения',
        choices=[(o.id, o.title) for o in Unit.objects.all()]
    )
    pack_volume = DecimalField(label='Количество в упаковке', decimal_places=3, max_digits=10)


class SaleForm(Form):
    good = ChoiceField(label='Продукт')
    shop = ChoiceField(label='Магазин')
    cost = DecimalField(label='Цена', max_digits=10, decimal_places=2)
    discount = BooleanField(label='Цена по акции', required=False)
    amount = DecimalField(label='Количество', max_digits=10, decimal_places=3)

    def full_clean(self):
        good_id = num(self.data.get('good', 0))
        if good_id > 0:
            good = Good.objects.get(pk=good_id)
            self.fields['good'].choices = [(good.id, good.title)]

        shop_id = num(self.data.get('shop', 0))
        if shop_id > 0:
            shop = Shop.objects.get(pk=shop_id)
            self.fields['shop'].choices = [(shop.id, shop.title)]

        return super(Form, self).full_clean()
