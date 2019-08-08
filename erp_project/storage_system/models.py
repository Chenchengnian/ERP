from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)

    class Meta(AbstractUser.Meta):
        pass


class Tag(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    is_enable = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Status(models.Model):
    status = models.CharField(max_length=64)
    is_enable = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    is_enable = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    image = models.ImageField(blank=True, null=True)
    username = models.CharField(max_length=100, blank=False, null=False, unique=True)
    cellphone = models.CharField(max_length=200)
    wechat = models.CharField(max_length=200)
    birthday = models.DateField()
    address = models.CharField(max_length=200)
    user_info = models.TextField()
    tag = models.ManyToManyField(Tag, blank=True)
    is_enable = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    price = models.FloatField()
    image = models.ImageField(blank=True, null=True)
    status = models.ForeignKey(Status)
    category = models.ForeignKey(Category)
    sale_date = models.DateTimeField()
    purchaser = models.ForeignKey(Customer)
    info = models.TextField(blank=True, null=True)
    tag = models.ManyToManyField(Tag, blank=True)
    is_enable = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
