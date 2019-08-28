from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Customer, Product
from .forms import CustomForm, ProductForm


def get_customer():
    data = Customer.objects.count()
    return data


class GetData:
    # def month_earn(self):
    #     price = Product.objects.filter(status=)
    pass


def index(request):
    return render(request, 'index.html', {'month_earn': 100,
                                          'yearly_earn': 1000,
                                          'sold_number': 11,
                                          'customer': get_customer(),
                                          })


def custom_list(request):
    custom = Customer.objects.all().order_by('-created_time')
    return render(request, 'custom/custom_list.html', {'custom': custom})


def product_list(request):
    product = Product.objects.all().order_by('-created_time')
    return render(request, 'product/product_list.html', {'product': product})


def product_sold(request):
    product = Product.objects.filter(status=0).order_by('-created_time')
    return render(request, 'product/product_sold.html', {'product': product})


def create_custom(request):
    if request.method == 'POST':
        custom_form = CustomForm(data=request.POST)
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
        product_form = ProductForm(data=request.POST)
        if product_form.is_valid():
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
