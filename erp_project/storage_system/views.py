import calendar
import datetime
import os
import time

from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from datetime import timedelta

from .models import Customer, Product, Status, Category, Sold


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


def get_day():
    return datetime.date.today().day


def get_today():
    return datetime.date.today()


def get_month_date_list():
    date_list = []
    if get_month() in [1, 3, 5, 7, 8, 10, 12]:
        for i in range(1, 32):
            if i < 10:
                i = '0' + str(i)
            date_list.append('{}-{}-{}'.format(get_year(), get_month(), i))
    elif get_month() in [4, 6, 9, 11]:
        for i in range(1, 31):
            if i < 10:
                i = '0' + str(i)
            date_list.append('{}-{}-{}'.format(get_year(), get_month(), i))
    else:
        if (get_year() % 4) == 0 and (get_year() % 100) != 0 or (get_year() % 400) == 0:
            for i in range(1, 30):
                if i < 10:
                    i = '0' + str(i)
                date_list.append('{}-{}-{}'.format(get_year(), get_month(), i))
        else:
            for i in range(1, 29):
                if i < 10:
                    i = '0' + str(i)
                date_list.append('{}-{}-{}'.format(get_year(), get_month(), i))
    return date_list


def get_date_list():
    date_list = []
    if get_month() in [1, 3, 5, 7, 8, 10, 12]:
        for i in range(1, 32):
            date_list.append(i)
    elif get_month() in [4, 6, 9, 11]:
        for i in range(1, 31):
            date_list.append(i)
    else:
        if (get_year() % 4) == 0 and (get_year() % 100) != 0 or (get_year() % 400) == 0:
            for i in range(1, 30):
                date_list.append(i)
        else:
            for i in range(1, 29):
                date_list.append(i)
    return date_list


def get_weekday_date_list():
    date_list = []
    today = datetime.date.today()
    this_week_start = today - timedelta(days=today.weekday())
    this_week_end = today + timedelta(days=6 - today.weekday())
    for i in range(int(str(this_week_start).split('-')[-1]), int(str(this_week_end).split('-')[-1]) + 1):
        if i < 10:
            i = '0' + str(i)
        date_list.append('{}-{}-{}'.format(get_year(), get_month(), i))
    return date_list


def take_second(elem):
    return elem[1]


def index(request):
    product = Product.objects.all().order_by('-created_time')
    category = Category.objects.all()
    short_storage_product = Product.objects.all().order_by('storage')[:6]
    custom = Customer.objects.all()
    name_list = []
    for i in custom:
        number = Sold.objects.filter(purchaser_id=i.id).count()
        name_list.append([i.username, number, i.id])
    name_list.sort(key=take_second, reverse=True)
    if len(name_list) < 6:
        for i in range(6-len(name_list)):
            name_list.append(['虚位以待', 0, 0])
    else:
        name_list = name_list[0:6]
    data_list = []
    for i in category:
        number = Product.objects.filter(category_id=i.id).count()
        data_list.append([i.name, number, i.id])
    data_list.sort(key=take_second, reverse=True)
    if len(name_list) > 5:
        data_list = data_list[:5]
    short_storage_product_list = []
    for i in short_storage_product:
        short_storage_product_list.append([i.name, i.storage, i.storage * 10, i.id])
    sold_number = Sold.objects.filter(sale_date__contains=get_today()).count()
    today_sold = Sold.objects.filter(sale_date__contains=get_today())
    month_sold = Sold.objects.filter(sale_date__gte=get_month_first_day_and_last_day(get_year(), get_month())[0],
                                     sale_date__lte=get_month_first_day_and_last_day(get_year(), get_month())[1])
    today_earn = month_earn = 0
    for sold in today_sold:
        today_earn += float(sold.sold_price) * int(sold.storage)

    for sold in month_sold:
        month_earn += float(sold.sold_price) * int(sold.storage)

    return render(request, 'index.html', {'month_earn': month_earn,
                                          'today_earn': today_earn,
                                          'sold_number': sold_number,
                                          'customer': get_customer(),
                                          'today': get_today(),
                                          'month': get_month(),
                                          'product': product[:5],
                                          'category': data_list,
                                          'short_storage_product': short_storage_product_list,
                                          'c': name_list,
                                          'title': '留琛金玉之盟'
                                          })


def custom_list(request):
    custom = Customer.objects.all().order_by('-created_time')
    count = Customer.objects.all().count()
    custom_list = []
    for c in custom:
        number = Sold.objects.filter(purchaser_id=c.id).count()
        custom_list.append([c.id, c.username, number, c.image, c.cellphone, c.wechat, c.birthday, c.address, c.user_info])
    return render(request, 'custom/custom_list.html', {'custom_list': custom_list,
                                                       'count': count,
                                                       'title': '顾客列表'})


def product_list(request):
    product = Product.objects.all().order_by('-created_time')
    count = Product.objects.all().count()
    paginator = Paginator(product, 10)
    page = request.GET.get('page')
    if page:
        try:
            product = paginator.page(page)
        except PageNotAnInteger:
            product = paginator.page(1)
        except EmptyPage:
            product = paginator.page(1)
    else:
        product = paginator.page(1)
    return render(request, 'product/product_list.html', {'product': product,
                                                         'count': count,
                                                         'title': '商品列表'})


def product_sold_list(request):
    if request.method == 'GET':
        sold = Sold.objects.all().order_by('-created_time')
        count = sold.count()
        paginator = Paginator(sold, 10)
        page = request.GET.get('page')
        if page:
            try:
                sold = paginator.page(page)
            except PageNotAnInteger:
                sold = paginator.page(1)
            except EmptyPage:
                sold = paginator.page(1)
        else:
            sold = paginator.page(1)
        return render(request, 'product/product_sold_list.html', {'year': get_year(),
                                                                  'month': get_month(),
                                                                  'day': get_day(),
                                                                  'sold': sold,
                                                                  'count': count,
                                                                  'date': '',
                                                                  'title': '商品销售列表'})
    else:
        data = request.POST
        year = data['year']
        month = data['month']
        day = data['day']
        if month == '' and day == '':
            date = year
        elif day == '':
            if int(month) < 10 and len(str(month)) == 1:
                month = '0' + str(month)
            date = year + '-' + month
        elif month == '' and day != '':
            date = '0000-00-00'
        else:
            if int(day) < 10 and len(str(day)) == 1:
                day = '0' + str(day)
            if int(month) < 10 and len(str(month)) == 1:
                month = '0' + str(month)
            date = year + '-' + month + '-' + day
        sold = Sold.objects.filter(sale_date__contains=date).order_by('-created_time')
        count = sold.count()
        return render(request, 'product/product_sold_list.html', {'year': year,
                                                                  'month': month,
                                                                  'day': day,
                                                                  'sold': sold,
                                                                  'count': count,
                                                                  'date': date,
                                                                  'title': '商品销售列表'})


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


def product_category_list(request, cid):
    product = Product.objects.filter(category_id=cid)
    name = Category.objects.get(id=cid).name
    return render(request, 'product/product_category_list.html', {'product': product,
                                                                  'name': name,
                                                                  'title': '销售商品列表'})


def create_custom(request):
    custom = Customer.objects.all().order_by('-created_time')
    name_list = []
    for c in custom:
        name_list.append(c.username)
    if request.method == 'POST':
        data = request.POST
        if data['username'] in name_list:
            return render(request, 'repeat.html', {'title': '错误'})
        try:
            image = request.FILES['image']
        except:
            image = 'custom/default.png'
        birthday = data['year'] + '-' + data['month'] + '-' + data['day']
        custom = Customer.objects.create(username=data['username'],
                                         cellphone=data['cellphone'],
                                         image=image,
                                         wechat=data['wechat'],
                                         address=data['address'],
                                         birthday=birthday,
                                         user_info=data['user_info'])
        custom.save(force_update=True)
        return redirect('/custom_list')
    else:
        return render(request, 'custom/create_custom.html', {'title': '顾客录入'})


def create_product(request):
    category = Category.objects.all().order_by('-created_time')
    category_list = []
    for cate in category:
        category_list.append(cate.name)

    product = Product.objects.all().order_by('-created_time')
    product_list = []
    for p in product:
        product_list.append(p.name)

    if request.method == 'POST':
        data = request.POST
        try:
            image = request.FILES['image']
        except:
            image = 'product/default.png'
        if data['category'] not in category_list and data['category'] != '':
            new_category = Category.objects.create(name=data['category'])
            new_category.save()
        if data['name'] in product_list:
            return render(request, 'repeat.html', {'title': '错误'})
        category_id = Category.objects.get(name=data['category']).id
        product = Product.objects.create(name=data['name'],
                                         price=data['price'],
                                         image=image,
                                         storage=data['storage'],
                                         #  status_id=data['status'],
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


def custom_update(request, cid):
    custom = Customer.objects.get(id=cid)
    if custom.birthday is None:
        birthday = ['', '', '']
    else:
        birthday = str(custom.birthday).split('-')
    if request.method == "GET":
        return render(request, "custom/custom_update.html", {'custom': custom,
                                                             'year': birthday[0],
                                                             'month': birthday[1],
                                                             'day': birthday[2],
                                                             'title': '修改顾客信息'})
    else:
        custom_all = Customer.objects.all().order_by('-created_time')
        name_list = []
        for c in custom_all:
            name_list.append(c.username)
        data = request.POST
        if data['username'] in name_list and data['username'] != custom.username:
            return render(request, 'repeat.html', {'title': '错误'})
        else:
            pre_img = str(custom.image)
            img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), pre_img)
            custom.username = data['username']
            custom.cellphone = data['cellphone']
            try:
                custom.image = request.FILES['image']
                flag_img = 1
            except:
                flag_img = 0
            year = data['year']
            month = data['month']
            day = data['day']
            birthday = year + '-' + month + '-' + day
            custom.birthday = birthday
            custom.wechat = data['wechat']
            custom.address = data['address']
            custom.user_info = data['user_info']
            custom.save(force_update=True)
            if flag_img == 1 and os.path.exists(img_path) and not pre_img.endswith('default.png'):
                os.remove(img_path)
            return redirect('/custom_list/')


def product_search(request):
    q = request.POST.get('keyword', '')
    product = Product.objects.filter(Q(name__icontains=q) | Q(info__icontains=q)).order_by('-created_time')
    count = product.count()
    if count == 0:
        return render(request, 'product/product_result.html', {'count': count,
                                                               'title': '查找商品'})
    return render(request, 'product/product_result.html', {'product': product,
                                                           'title': '查找商品'})


# def sold_product_search(request):
#     q = request.POST.get('keyword', '')
#     product = Product.objects.filter(Q(name__icontains=q) | Q(info__icontains=q)).order_by('-created_time')
#     count = product.count()
#     if count == 0:
#         return render(request, 'product/sold_product_result.html', {'count': count,
#                                                                     'title': '查找销售商品'})
#     else:
#         print(product)
#         return render(request, 'product/sold_product_result.html', {'product': product,
#                                                                     'title': '查找销售商品'})


def product_detail(request, pid):
    product = Product.objects.get(id=pid)
    return render(request, 'product/product_detail.html', {'product': product,
                                                           'title': '商品详情'})


def product_update(request, pid):
    product = Product.objects.get(id=pid)
    sold = Sold.objects.filter(name=product.name)
    status = Status.objects.all()
    category = Category.objects.all()
    if request.method == "GET":
        return render(request, "product/product_update.html", {'product': product,
                                                               'status': status,
                                                               'category': category,
                                                               'title': '修改商品信息'})
    else:
        data = request.POST
        name_list = []
        for p in Product.objects.all():
            name_list.append(p.name)
        if data['name'] in name_list and data['name'] != product.name:
            return render(request, 'repeat.html', {'title': '错误'})
        category_list = []
        for cate in category:
            category_list.append(cate.name)
        if data['category'] not in category_list and data['category'] != '':
            new_category = Category.objects.create(name=data['category'])
            new_category.save()
        product.name = data['name']
        product.price = data['price']
        if request.FILES.get('image', '') != '':
            pre_img = str(product.image)
            img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), pre_img)
            if os.path.exists(img_path) and not img_path.endswith('default.png'):
                os.remove(img_path)
            product.image = request.FILES['image']
            for s in sold:
                pre_img = str(s.image)
                img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), pre_img)
                if os.path.exists(img_path) and not img_path.endswith('default.png'):
                    os.remove(img_path)
                s.image = request.FILES['image']
                s.save()
        if data['category'] == '':
            product.category_id = Category.objects.get(name=product.category).id
        else:
            product.category_id = Category.objects.get(name=data['category']).id
        product.storage = data['storage']
        product.save(force_update=True)
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
                                   payment_method=data['payment_method'],
                                   sale_date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        sold.save(force_update=True)
        storage = int(product.storage) - int(data['storage'])
        product.storage = storage
        product.save()
        return redirect('/product_sold_list/')


def sold_product_update(request, pid):
    product = Sold.objects.get(id=pid)
    category = Category.objects.all().order_by('-created_time')
    # 获取之前销售数量
    storage_before = product.storage
    # 获取当前商品的库存数量
    product1 = Product.objects.get(name=product.name)
    product2 = Sold.objects.filter(name=product.name).filter(~Q(id=product.id))
    allow_storage = int(storage_before) + int(product1.storage)
    custom = Customer.objects.all().order_by('-created_time')
    name_list = []
    for name in custom:
        name_list.append(name.username)
    if request.method == "GET":
        return render(request, "product/sold_product_update.html", {'product': product,
                                                                    'category': category,
                                                                    'custom': custom,
                                                                    'allow_storage': allow_storage,
                                                                    'title': '销售商品修改'})
    else:
        data = request.POST
        change_storage = int(data['storage']) - int(product.storage)
        if data['custom'] not in name_list and data['custom'] != '':
            new_custom = Customer.objects.create(username=data['custom'])
            new_custom.save()
        purchaser_id = Customer.objects.get(username=data['custom']).id
        product.purchaser_id = purchaser_id
        product.sold_price = data['price']
        if request.FILES.get('image', '') != '':
            pre_img = str(product1.image)
            img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), pre_img)
            if os.path.exists(img_path) and not img_path.endswith('default.png'):
                os.remove(img_path)
            product1.image = request.FILES['image']
            pre_img = str(product.image)
            img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), pre_img)
            if os.path.exists(img_path) and not img_path.endswith('default.png'):
                os.remove(img_path)
            product.image = request.FILES['image']
            for p in product2:
                pre_img = str(p.image)
                img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), pre_img)
                if os.path.exists(img_path) and not img_path.endswith('default.png'):
                    os.remove(img_path)
                p.image = request.FILES['image']
                p.save()
        product.storage = data['storage']
        product.payment_method = data['payment_method']
        product.save()
        product1.storage -= change_storage
        product1.save(force_update=True)
        return redirect('/product_sold_list/')


def category_list(request):
    category = Category.objects.all().order_by('-created_time')
    data_list = []
    for c in category:
        count = Product.objects.filter(category_id=c.id).count()
        data_list.append([c.name, count, c.id, c.created_time])
    return render(request, 'category/category_list.html', {'data_list': data_list})


def category_update(request, cid):
    category = Category.objects.get(id=cid)

    if request.method == "GET":
        return render(request, 'category/category_update.html', {'category': category})
    else:
        category_all = Category.objects.all()
        c_list = []
        for c in category_all:
            c_list.append(c.name)
        data = request.POST
        if data['name'] in c_list and data['name'] != category.name:
            return render(request, 'repeat.html', {'title': '错误'})
        else:
            category.name = data['name']
            category.save()
            return redirect('/category_list/')


def create_category(request):
    category = Category.objects.all().order_by('-created_time')
    category_list = []
    for cate in category:
        category_list.append(cate.name)

    if request.method == 'POST':
        data = request.POST
        if data['name'] not in category_list:
            new_category = Category.objects.create(name=data['name'])
            new_category.save()
            return redirect('/category_list/')
        else:
            return render(request, 'repeat.html', {'title': '错误'})
    else:
        return render(request, 'category/create_category.html', {'title': '新建分类'})


def product_custom_list(request, cid):
    product = Sold.objects.filter(purchaser_id=cid).order_by('-sale_date')
    name = Customer.objects.get(id=cid).username
    return render(request, 'product/product_custom_list.html', {'product': product,
                                                                'name': name,
                                                                'title': '购买商品列表'})


def total_data(request):
    null = False
    y_axis_pre_day_by_month = []
    for date in get_month_date_list():
        earn_by_month = 0
        sold = Sold.objects.filter(sale_date__contains=date)
        if len(sold) == 0:
            y_axis_pre_day_by_month.append(0)
        else:
            for s in sold:
                earn_by_month += float(s.sold_price) * int(s.storage)
            y_axis_pre_day_by_month.append(earn_by_month)

    y_axis_pre_day_by_week = []

    for date in get_weekday_date_list():
        sold = Sold.objects.filter(sale_date__contains=date)
        if len(sold) == 0:
            y_axis_pre_day_by_week.append(0)
        else:
            earn_by_week = 0
            for s in sold:
                earn_by_week += float(s.sold_price) * int(s.storage)
            y_axis_pre_day_by_week.append(earn_by_week)

    today_sold = Sold.objects.filter(sale_date__contains=get_today())
    name_list = []
    for s in today_sold:
        name = str(s.name)
        if name not in name_list:
            name_list.append(name)
    value_list = []
    for i in name_list:
        try:
            today_sold_by_name = Sold.objects.filter(sale_date__contains=get_today()).get(name=i)
            value_list.append([int(today_sold_by_name.storage), i])
        except:
            today_sold_by_name = Sold.objects.filter(sale_date__contains=get_today()).filter(name=i)
            storage = 0
            for j in today_sold_by_name:
                storage += int(j.storage)
            value_list.append([storage, i])
    if len(name_list) == 0:
        null = True
    return render(request, 'data/total_data.html', {'month': get_month(),
                                                    'x_axis_pre_day_by_month': get_month_date_list(),
                                                    'y_axis_pre_day_by_month': y_axis_pre_day_by_month,
                                                    'y_axis_pre_day_by_week': y_axis_pre_day_by_week,
                                                    'category_list': name_list,
                                                    'value_list': value_list,
                                                    'null': null})


def sale_data_by_day(request):
    null = False
    if request.method == 'POST':
        data = request.POST
        year = data['year']
        month = data['month']
        day = data['day']
        if month == '' and day == '':
            date = year
        elif day == '':
            if int(month) < 10 and len(str(month)) == 1:
                month = '0' + str(month)
            date = year + '-' + month
        elif month == '' and day != '':
            date = '0000-00-00'
        else:
            if int(day) < 10 and len(str(day)) == 1:
                day = '0' + str(day)
            if int(month) < 10 and len(str(month)) == 1:
                month = '0' + str(month)
            date = year + '-' + month + '-' + day
        today_sold = Sold.objects.filter(sale_date__contains=date)
        name_list = []
        for s in today_sold:
            name = str(s.name)
            if name not in name_list:
                name_list.append(name)
        value_list = []
        for i in name_list:
            try:
                today_sold_by_name = Sold.objects.filter(sale_date__contains=date).get(name=i)
                value_list.append([int(today_sold_by_name.storage), i])
            except:
                today_sold_by_name = Sold.objects.filter(sale_date__contains=date).filter(name=i)
                storage = 0
                for j in today_sold_by_name:
                    storage += int(j.storage)
                value_list.append([storage, i])

        if len(name_list) == 0:
            null = True

        sold_number = Sold.objects.filter(sale_date__contains=get_today()).count()
        today_sold = Sold.objects.filter(sale_date__contains=get_today())
        today_earn = 0
        for sold in today_sold:
            today_earn += float(sold.sold_price) * int(sold.storage)
        return render(request, 'data/sale_data_by_day.html', {'year': year,
                                                              'month': month,
                                                              'day': day,
                                                              'date': date,
                                                              'category_list': name_list,
                                                              'value_list': value_list,
                                                              'null': null,
                                                              'today_earn': today_earn,
                                                              'sold_number': sold_number})
    else:
        today_sold = Sold.objects.filter(sale_date__contains=get_today())
        name_list = []
        for s in today_sold:
            name = str(s.name)
            if name not in name_list:
                name_list.append(name)
        value_list = []
        for i in name_list:
            try:
                today_sold_by_name = Sold.objects.filter(sale_date__contains=get_today()).get(name=i)
                value_list.append([int(today_sold_by_name.storage), i])
            except:
                today_sold_by_name = Sold.objects.filter(sale_date__contains=get_today()).filter(name=i)
                storage = 0
                for j in today_sold_by_name:
                    storage += int(j.storage)
                value_list.append([storage, i])
        if len(name_list) == 0:
            null = True

        sold_number = Sold.objects.filter(sale_date__contains=get_today()).count()
        today_sold = Sold.objects.filter(sale_date__contains=get_today())
        today_earn = 0
        for sold in today_sold:
            today_earn += float(sold.sold_price) * int(sold.storage)
        return render(request, 'data/sale_data_by_day.html', {'year': get_year(),
                                                              'month': get_month(),
                                                              'day': get_day(),
                                                              'date': '{}-{}-{}'.format(get_year(), get_month(), get_day()),
                                                              'category_list': name_list,
                                                              'value_list': value_list,
                                                              'null': null,
                                                              'today_earn': today_earn,
                                                              'sold_number': sold_number,
                                                              'get': True})


def sale_data_by_month(request):
    if request.method == 'POST':
        return
    else:
        return render(request, 'data/sale_data_by_month.html', {'x_axis': [1, 2, 3, 4, 5],
                                                                'y_axis': [100, 111, 222, 48, 0]})


def sale_data_by_year(request):
    sold = Sold.objects.all()

    paginator = Paginator(sold, 2)  # 按每页10条分页
    page = request.GET.get('page', '1')  # 默认跳转到第一页
    result = paginator.page(page)
    return render(request, 'data/sale_data_by_year.html', {'messages': result})




