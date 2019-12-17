import calendar
import datetime
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


def get_month_first_day_and_last_day(year=None, month=None):
    if year:
        year = int(year)
    else:
        year = datetime.date.today().year

    if month:
        month = int(month)
    else:
        month = datetime.date.today().month

    # 获取当月第一天的星期和当月的总天数
    first_day_week_day, month_range = calendar.monthrange(year, month)

    # 获取当月的第一天
    first_day = datetime.date(year=year, month=month, day=1)
    last_day = datetime.date(year=year, month=month, day=month_range)

    return first_day, last_day


def get_year():
    return datetime.date.today().year


def get_month():
    return datetime.date.today().month


def get_today():
    return datetime.date.today()


def index(request):
    product = Product.objects.all().order_by('-created_time')[:5]
    sold_number = Sold.objects.filter(sale_date__contains=get_today()).count()
    today_sold = Sold.objects.filter(sale_date__contains=get_today())
    month_sold = Sold.objects.filter(sale_date__gte=get_month_first_day_and_last_day(get_year(), get_month())[0],
                                     sale_date__lte=get_month_first_day_and_last_day(get_year(), get_month())[1])
    today_earn = month_earn = 0
    for sold in today_sold:
        today_earn += int(sold.price) * int(sold.storage)

    for sold in month_sold:
        month_earn += int(sold.price) * int(sold.storage)

    return render(request, 'index.html', {'month_earn': month_earn,
                                          'today_earn': today_earn,
                                          'sold_number': sold_number,
                                          'customer': get_customer(),
                                          'today': get_today(),
                                          'month': get_month(),
                                          'product': product,
                                          'title': '留琛金玉之盟'
                                          })


def custom_list(request):
    custom = Customer.objects.all().order_by('-created_time')
    count = Customer.objects.all().count()
    return render(request, 'custom/custom_list.html', {'custom': custom,
                                                       'count': count,
                                                       'title': '顾客列表'})


def product_list(request):
    product = Product.objects.all().order_by('-created_time')
    count = Product.objects.all().count()
    return render(request, 'product/product_list.html', {'product': product,
                                                         'count': count,
                                                         'title': '商品列表'})


def product_sold_list(request):
    sold = Sold.objects.all().order_by('-created_time')
    count = sold.count()
    return render(request, 'product/product_sold_list.html', {'sold': sold,
                                                              'count': count,
                                                              'title': '销售商品列表'})


def today_sold_list(request):
    sold_list = Sold.objects.filter(sale_date__contains=get_today()).order_by('-created_time')
    return render(request, 'product/product_sold_list.html', {'sold': sold_list,
                                                              'date': get_today(),
                                                              'title': '{}销售商品列表'.format(get_today())})


def month_sold_list(request):
    sold_list = Sold.objects.filter(sale_date__gte=get_month_first_day_and_last_day(get_year(), get_month())[0],
                                    sale_date__lte=get_month_first_day_and_last_day(get_year(), get_month())[1]).order_by('-created_time')
    return render(request, 'product/product_sold_list.html', {'sold': sold_list,
                                                              'today': get_today(),
                                                              'date': str(get_month()) + '月',
                                                              'title': '{}月销售商品列表'.format(get_month())})


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
        context = {'custom_form': custom_form,
                   'title': '新建顾客'}
        # 返回模板
        return render(request, 'custom/create_custom.html', context)


def create_product(request):
    category = Category.objects.all().order_by('-created_time')
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
        return render(request, 'product/create_product.html', {'category': category,
                                                               'title': '商品录入'})


def custom_search(request):
    q = request.POST.get('keyword', '')
    custom = Customer.objects.filter(Q(username__icontains=q) | Q(user_info__icontains=q)).order_by('-created_time')
    count = custom.count()
    if count == 0:
        return render(request, 'custom/custom_result.html', {'count': count,
                                                             'title': '查找顾客'})
    return render(request, 'custom/custom_result.html', {'custom': custom,
                                                         'title': '查找顾客'})


def product_search(request):
    q = request.POST.get('keyword', '')
    product = Product.objects.filter(Q(name__icontains=q) | Q(info__icontains=q)).order_by('-created_time')
    count = product.count()
    if count == 0:
        return render(request, 'product/product_result.html', {'count': count,
                                                               'title': '查找商品'})
    return render(request, 'product/product_result.html', {'product': product,
                                                           'title': '查找商品'})


def sold_product_search(request):
    q = request.POST.get('keyword', '')
    product = Product.objects.filter(Q(name__icontains=q) | Q(info__icontains=q)).order_by('-created_time')
    count = product.count()
    if count == 0:
        return render(request, 'product/sold_product_result.html', {'count': count,
                                                                    'title': '查找销售商品'})
    return render(request, 'product/sold_product_result.html', {'product': product,
                                                                'title': '查找销售商品'})


def product_detail(request, pid):
    product = Product.objects.get(id=pid)
    return render(request, 'product/product_detail.html', {'product': product,
                                                           'title': '商品详情'})


def product_update(request, pid):
    product = Product.objects.get(id=pid)
    status = Status.objects.all()
    category = Category.objects.all()
    if request.method == "GET":
        return render(request, "product/product_update.html", {'product': product,
                                                               'status': status,
                                                               'category': category,
                                                               'title': '修改商品信息'})
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
        if data['category'] == '':
            product.category_id = Category.objects.get(name=product.category).id
        else:
            product.category_id = Category.objects.get(name=data['category']).id
        product.storage = data['storage']
        product.save(force_update=True)
        if flag_img == 1 and os.path.exists(img_path):
            os.remove(img_path)
        return redirect('/product_detail/{}'.format(pid))


def product_sold(request, pid):
    product = Product.objects.get(id=pid)
    custom = Customer.objects.all().order_by('-created_time')
    name_list = []
    for name in custom:
        name_list.append(name.username)
    if request.method == "GET":
        return render(request, "product/product_sold.html", {'product': product,
                                                             'custom_list': custom,
                                                             'title': '商品销货'})
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
    category = Category.objects.all().order_by('-created_time')
    custom = Customer.objects.all().order_by('-created_time')
    if request.method == "GET":
        return render(request, "product/sold_product_update.html", {'product': product,
                                                                    'category': category,
                                                                    'custom': custom,
                                                                    'title': '销售商品修改'})
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




