from django.forms import ModelForm, CharField, BooleanField, DecimalField, ModelChoiceField
from .models import Unit, Good, Shop, Cost

class ShopForm(ModelForm):
    class Meta:
        model = Shop

    address = CharField(label='Адрес')
    title = CharField(label='Название')


class GoodForm(ModelForm):
    class Meta:
        model = Good

    bar_code = CharField(label='Штрих-код', required=False)
    title = CharField(label='Название')
    parent = ModelChoiceField(queryset=Good.objects.all(), label='Группа', required=False)
    packed = BooleanField(label='Продается ли товар в фиксированной упаковке?', required=False)
    unit = ModelChoiceField(queryset=Unit.objects.all(), label='Единица измерения')
    pack_volume = DecimalField(label='Количество в упаковке', decimal_places=3, max_digits=10)


class SaleForm(ModelForm):
    class Meta:
        model = Cost
        fields = ['good', 'shop', 'cost', 'discount', 'amount']

    good = ModelChoiceField(queryset=Good.objects.all(), label='Продукт')
    shop = ModelChoiceField(queryset=Shop.objects.all(), label='Магазин')
    cost = DecimalField(label='Цена', max_digits=10, decimal_places=2)
    discount = BooleanField(label='Цена по акции', required=False)
    amount = DecimalField(label='Количество', max_digits=10, decimal_places=3)
