from django.contrib import admin

from .models import User, Tag, Status, Category, Product, Customer


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'nickname']


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_time', 'modified_time']


class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'is_enable', 'created_time', 'modified_time']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_time', 'modified_time']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'created_time', 'modified_time']


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'created_time', 'modified_time']


admin.site.register(User, UserAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)

