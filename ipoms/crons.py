from erp_project.storage_system.models import Product


def update_shortage():
    product_list = Product.objects.filte(status=1)
    for product in product_list:
        if product.storage <= 5:
            product.status = '已出售'
            product.save()

