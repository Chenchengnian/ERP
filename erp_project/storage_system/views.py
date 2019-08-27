from django.shortcuts import render

from .models import Customer, Product


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
                                          'n': 999})




