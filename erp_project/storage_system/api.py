from erp_project.storage_system.models import Product, Customer


def get_customer_number():
    count = Customer.objects.count()
    return count


def get_daily_earn():
    sold_product = Product.objects.filter(status=2)
    for p in sold_product:
        print(p.price)


get_daily_earn()
