from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, loader
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.forms import Form
from django.db.models import Q

from .models import Good, Shop, Unit, Cost
from .forms import ShopForm, GoodForm, SaleForm

def empty2none(string):
    if len(string) > 0:
        return string
    else:
        return None

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class AddForm(LoginRequiredMixin, TemplateView):
    template_name = ""
    initial = {}
    form_class = Form
    ok_url = ""

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            self.process_cleaned_data(form, request)
            return HttpResponseRedirect(self.ok_url)

        return render(request, self.template_name, {'form': form})

    def process_cleaned_data(self, form, request):
        pass

class EditForm(LoginRequiredMixin, TemplateView):
    template_name = ""
    form_class = Form
    ok_url = ""

    def get(self, request, *args, **kwargs):
        model = self.get_model(int(kwargs.get('id', 0)))
        form = self.form_class(initial=model)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            self.process_cleaned_data(form, request)
            return HttpResponseRedirect(self.ok_url)

        return render(request, self.template_name, {'form': form})

    def process_cleaned_data(self, form, request):
        pass

    def get_model(self, id):
        pass

class ShopAdd(AddForm):
    template_name = "shops/add.html"
    initial = {}
    form_class = ShopForm
    ok_url = "/shops/list"

    def process_cleaned_data(self, form, request):
        data = form.cleaned_data
        shop = Shop(address=data['address'], title=data['title'])
        shop.save()


class GoodAdd(AddForm):
    template_name = "goods/add.html"
    initial = {
        'pack_volume': 1,
    }
    form_class = GoodForm
    ok_url = "/goods/list"

    def process_cleaned_data(self, form, request):
        data = form.cleaned_data
        good = Good(
            bar_code=data['bar_code'],
            title=data['title'],
            parent=empty2none(data['parent']),
            packed=data['packed'],
            unit=Unit.objects.get(pk=data['unit']),
            pack_volume=data['pack_volume']
        )
        good.save()

class GoodEdit(EditForm):
    template_name = "goods/edit.html"
    form_class = GoodForm
    ok_url = "/goods/list"

    def process_cleaned_data(self, form, request):
        data = form.cleaned_data
        good = Good(
            bar_code=data['bar_code'],
            title=data['title'],
            parent=empty2none(data['parent']),
            packed=data['packed'],
            unit=Unit.objects.get(pk=data['unit']),
            pack_volume=data['pack_volume']
        )
        good.save()


class CostAdd(AddForm):
    template_name = "sales/add.html"
    initial = {
        'amount': 1,
    }
    form_class = SaleForm
    ok_url = "/sales/list"

    def process_cleaned_data(self, form, request):
        data = form.cleaned_data
        cost = Cost(
            good=Good.objects.get(pk=data['good']),
            shop=Shop.objects.get(pk=data['shop']),
            user=request.user,
            cost=data['cost'],
            amount=data['amount'],
            discount=data['discount'],
        )
        cost.save()


def index(request):
    q = request.GET.get('q', '')
    if len(q) > 0:
        goods = Good.objects.filter(Q(bar_code__contains=q) | Q(title__contains=q))
    else:
        goods = []
    template = loader.get_template('index/index.html')
    context = RequestContext(request, {
        'q': q,
        'goods': goods,
    })
    return HttpResponse(template.render(context))

def goods_list(request):
    goods = Good.objects.filter(parent=None)
    template = loader.get_template('goods/list.html')
    context = RequestContext(request, {
        'goods': goods,
    })
    return HttpResponse(template.render(context))

def goods_view(request, good_id):
    good = Good.objects.get(pk=good_id)
    children = Good.objects.filter(parent=good)
    template = loader.get_template('goods/view.html')
    context = RequestContext(request, {
        'good': good,
        'children': children,
        'costs': good.list_costs(),
        'parents': good.list_parents(),
    })
    return HttpResponse(template.render(context))

def shops_list(request):
    shops = Shop.objects.all()
    template = loader.get_template('shops/list.html')
    context = RequestContext(request, {
        'shops': shops,
    })
    return HttpResponse(template.render(context))

def sales_list(request):
    costs = Cost.objects.all()
    template = loader.get_template('sales/list.html')
    context = RequestContext(request, {
        'sales': costs,
    })
    return HttpResponse(template.render(context))

def ajax_goods(request, query):
    def forAjax(good):
        return {
            'id': good.id,
            'title': good.title,
            'search_field': good.title + ' ' + good.bar_code,
        }
    res = {
        'goods': list(map(forAjax, Good.objects.all()))
    }
    return JsonResponse(res)

def ajax_shops(request, query):
    def forAjax(shop):
        return {
            'id': shop.id,
            'title': shop.title,
            'search_field': shop.title,
        }
    res = {
        'shops': list(map(forAjax, Shop.objects.all()))
    }
    return JsonResponse(res)
