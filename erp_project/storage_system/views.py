from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Customer, Product, Status, Category
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


def sold_project(request):
    pass


def product_detail(request, pid):
    product = Product.objects.get(id=pid)
    return render(request, 'product/product_detail.html', {'product': product})


def product_update(request, pid):
    product = Product.objects.get(id=pid)
    status = Status.objects.all()
    category = Category.objects.all()
    if request.method == "GET":
        return render(request, "product/product_update.html", {'product': product,
                                                               'status': status,
                                                               'category': category})
    else:
        data = request.POST
        product.name = data['name']
        product.price = data['price']
        try:
            product.image = request.FILES['image']
        except:
            pass
        # # product.status = data['status']
        # # product.category = data['category']
        product.storage = data['storage']
        product.save()
        return redirect('/product_detail/{}'.format(pid))


