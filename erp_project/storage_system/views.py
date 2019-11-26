import json

from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Customer, Product, Status
from .forms import CustomForm, ProductForm


def get_customer():
    data = Customer.objects.count()
    return data


class GetData:
    pass


def index(request):
    return render(request, 'index.html', {'month_earn': 100,
                                          'yearly_earn': 1000,
                                          'sold_number': 11,
                                          'customer': get_customer(),
                                          })


def custom_list(request):
    custom = Customer.objects.all().order_by('-created_time')
    count = Customer.objects.all().count()
    return render(request, 'custom/custom_list.html', {'custom': custom,
                                                       'count': count})


def product_list(request):
    product = Product.objects.all().order_by('-created_time')
    count = Product.objects.all().count()
    return render(request, 'product/product_list.html', {'product': product,
                                                         'count': count})
    # sold_product = Product.objects.filter(status=2)
    # for p in sold_product:
    #     price = 0 + p.price
    #     print(price)
    # return render(request, 'product/product_list.html', {'product': sold_product})


def product_sold_list(request):
    try:
        get_sold_status = Status.objects.get(status='已销售')
        product = Product.objects.filter(status=get_sold_status).order_by('-created_time')
        count = product.count()
    except:
        product = ''
        count = 0
    return render(request, 'product/product_sold.html', {'product': product,
                                                         'count': count})


def create_custom(request):
    if request.method == 'POST':
        custom_form = CustomForm(request.POST, request.FILES)
        if custom_form.is_valid():
            custom_form.save()
            return redirect('/custom_list')
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        # 创建表单类实例
        custom_form = CustomForm()
        # 赋值上下文
        context = {'custom_form': custom_form}
        # 返回模板
        return render(request, 'custom/create_custom.html', context)


def create_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            img = product_form.cleaned_data
            product_form.save()
            return redirect('/product_list')
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        # 创建表单类实例
        product_form = ProductForm()
        # 赋值上下文
        context = {'product_form': product_form}
        # 返回模板
        return render(request, 'product/create_product.html', context)


def custom_search(request):
    q = request.POST.get('keyword', '')
    custom = Customer.objects.filter(Q(username__icontains=q) | Q(user_info__icontains=q))
    count = custom.count()
    if count == 0:
        return render(request, 'custom/custom_result.html', {'count': count})
    return render(request, 'custom/custom_result.html', {'custom': custom})


def product_search(request):
    q = request.POST.get('keyword', '')
    custom = Product.objects.filter(Q(name__icontains=q) | Q(info__icontains=q))
    count = custom.count()
    if count == 0:
        return render(request, 'product/product_result.html', {'count': count})
    return render(request, 'product/product_result.html', {'custom': custom})


def sale_product(request):
    pass