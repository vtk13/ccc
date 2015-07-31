from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, loader
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Good, Shop, Unit, Cost, GoodImage
from .forms import ShopForm, GoodForm, SaleForm

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

class ShopAdd(LoginRequiredMixin, CreateView):
    template_name = "shops/add.html"
    initial = {}
    model = Shop
    form_class = ShopForm
    success_url = "/shops/list"


class GoodAdd(LoginRequiredMixin, CreateView):
    template_name = "goods/add.html"
    initial = {
        'pack_volume': 1,
    }
    model = Good
    form_class = GoodForm


class GoodEdit(LoginRequiredMixin, UpdateView):
    template_name = "goods/edit.html"
    model = Good
    form_class = GoodForm

class CostAdd(LoginRequiredMixin, CreateView):
    template_name = "sales/add.html"
    initial = {
        'amount': 1,
    }
    model = Cost
    form_class = SaleForm
    success_url = "/sales/list"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CostAdd, self).form_valid(form)


def index(request):
    q = request.GET.get('q', '')
    if len(q) > 0:
        goods = Good.objects.filter(Q(bar_code__icontains=q) | Q(title__icontains=q))
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
    _min, _max = good.min_max_cost()
    good.min = _min
    good.max = _max

    images = GoodImage.objects.filter(good=good)
    template = loader.get_template('goods/view.html')
    context = RequestContext(request, {
        'good': good,
        'images': images,
        'children': good.list_children(),
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

@login_required
def sales_list(request):
    costs = Cost.objects.filter(user=request.user).order_by('-timestamp')
    template = loader.get_template('sales/list.html')
    context = RequestContext(request, {
        'sales': costs,
    })
    return HttpResponse(template.render(context))

def ajax_goods(request, query):
    def forAjax(good):
        return {
            'id': good.id,
            'bar_code': good.bar_code,
            'title': good.title,
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
        }
    res = {
        'shops': list(map(forAjax, Shop.objects.all()))
    }
    return JsonResponse(res)
