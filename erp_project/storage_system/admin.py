from django.contrib import admin

from .models import Tag, Status, Category, Product, Customer


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_time', 'modified_time']


class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'is_enable', 'created_time', 'modified_time']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_time', 'modified_time']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'image', 'status', 'sale_date', 'purchaser', 'info',
                    'storage', 'created_time', 'modified_time']

    list_filter = ('id', 'name', 'price', 'image', 'status', 'sale_date', 'purchaser', 'info',
                   'created_time', 'modified_time')  # 过滤器


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'created_time', 'modified_time']


admin.site.register(Tag, TagAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)

