import os
import time
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Customer, Product, Status, Category, Sold
from .forms import CustomForm


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

    sold = Sold.objects.all().order_by('-created_time')
    count = sold.count()
    return render(request, 'product/product_sold_list.html', {'sold': sold,
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
    category = Category.objects.all()
    category_list = []
    for cate in category:
        category_list.append(cate.name)
    if request.method == 'POST':
        data = request.POST
        try:
            image = request.FILES['image']
        except:
            image = 'media/product/default.png'
        if data['category'] not in category_list:
            new_category = Category.objects.create(name=data['category'])
            new_category.save()
        category_id = Category.objects.get(name=data['category']).id
        product = Product.objects.create(name=data['name'],
                                         price=data['price'],
                                         image=image,
                                         storage=data['storage'],
                                         status_id=data['status'],
                                         category_id=category_id,
                                         info=data['info'])
        product.save(force_update=True)
        return redirect('/product_list')
    else:
        return render(request, 'product/create_product.html', {'category': category})


def custom_search(request):
    q = request.POST.get('keyword', '')
    custom = Customer.objects.filter(Q(username__icontains=q) | Q(user_info__icontains=q))
    count = custom.count()
    if count == 0:
        return render(request, 'custom/custom_result.html', {'count': count})
    return render(request, 'custom/custom_result.html', {'custom': custom})


def product_search(request):
    q = request.POST.get('keyword', '')
    product = Product.objects.filter(Q(name__icontains=q) | Q(info__icontains=q))
    count = product.count()
    if count == 0:
        return render(request, 'product/product_result.html', {'count': count})
    return render(request, 'product/product_result.html', {'product': product})


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
        category_list = []
        for cate in category:
            category_list.append(cate.name)
        if data['category'] not in category_list:
            new_category = Category.objects.create(name=data['category'])
            new_category.save()
        pre_img = str(product.image)
        img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), pre_img)
        product.name = data['name']
        product.price = data['price']
        try:
            product.image = request.FILES['image']
            flag_img = 1
        except:
            flag_img = 0
        product.status_id = data['status']
        product.category_id = Category.objects.get(name=data['category']).id
        product.storage = data['storage']
        product.save(force_update=True)
        if flag_img == 1 and os.path.exists(img_path):
            os.remove(img_path)
        return redirect('/product_detail/{}'.format(pid))


def product_sold(request, pid):
    product = Product.objects.get(id=pid)
    custom = Customer.objects.all()
    name_list = []
    for name in custom:
        name_list.append(name.username)
    if request.method == "GET":
        return render(request, "product/product_sold.html", {'product': product,
                                                             'custom_list': custom})
    else:
        data = request.POST
        if data['custom'] not in name_list:
            new_custom = Customer.objects.create(username=data['custom'])
            new_custom.save()
        purchase_id = Customer.objects.get(username=data['custom']).id
        sold = Sold.objects.create(name=product.name,
                                   price=product.price,
                                   sold_price=data['price'],
                                   category=product.category,
                                   storage=data['storage'],
                                   image=product.image,
                                   purchaser_id=purchase_id,
                                   sale_date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        sold.save(force_update=True)
        storage = int(product.storage) - int(data['storage'])
        product.storage = storage
        product.save()
        return redirect('/product_sold_list/')


def sold_product_update(request, pid):
    product = Sold.objects.get(id=pid)
    category = Category.objects.all()
    custom = Customer.objects.all()
    if request.method == "GET":
        return render(request, "product/sold_product_update.html", {'product': product,
                                                                    'category': category,
                                                                    'custom': custom})
    else:
        data = request.POST
        category_list = []
        for cate in category:
            category_list.append(cate.name)
        if data['category'] not in category_list:
            new_category = Category.objects.create(name=data['category'])
            new_category.save()
        pre_img = str(product.image)
        img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), pre_img)
        product.name = data['name']
        product.price = data['price']
        try:
            product.image = request.FILES['image']
            flag_img = 1
        except:
            flag_img = 0
        product.category_name = data['category']
        product.storage = data['storage']
        product.save(force_update=True)
        if flag_img == 1 and os.path.exists(img_path):
            os.remove(img_path)
        return redirect('/product_sold_list/')




