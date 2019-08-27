from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True, verbose_name='用户名')

    class Meta(AbstractUser.Meta):
        verbose_name = '账号'
        verbose_name_plural = '账号'

    def __str__(self):
        return self.nickname


class Tag(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True, verbose_name='标签名')
    is_enable = models.BooleanField(default=True, verbose_name='是否可见')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

    def __str__(self):
        return self.name


class Status(models.Model):
    status_choice = (
        (0, '已入库'),
        (1, '')
    )
    status = models.CharField(max_length=64, verbose_name='状态')
    is_enable = models.BooleanField(default=True, verbose_name='是否可见')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '状态'
        verbose_name_plural = '状态'

    def __str__(self):
        return self.status


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True, verbose_name='分类')
    is_enable = models.BooleanField(default=True, verbose_name='是否可见')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类信息'

    def __str__(self):
        return self.name


class Customer(models.Model):
    image = models.ImageField(blank=True, null=True, verbose_name='顾客照片')
    username = models.CharField(max_length=100, blank=False, null=False, unique=True, verbose_name='顾客姓名')
    cellphone = models.CharField(max_length=200, verbose_name='顾客电话')
    wechat = models.CharField(max_length=200, verbose_name='顾客微信')
    birthday = models.DateField(verbose_name='顾客生日')
    address = models.CharField(max_length=200, verbose_name='顾客地址')
    user_info = models.TextField(verbose_name='顾客信息', blank=True, null=True)
    tag = models.ManyToManyField(Tag, blank=True, verbose_name='标签')
    is_enable = models.BooleanField(default=True, verbose_name='是否可见')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '顾客'
        verbose_name_plural = '顾客信息'

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, unique=True, verbose_name='商品名称')
    price = models.FloatField(verbose_name='商品价格')
    image = models.ImageField(blank=True, null=True, verbose_name='商品图片')
    status = models.ForeignKey(Status, verbose_name='商品状态', default=0)
    category = models.ForeignKey(Category, verbose_name='分类')
    sale_date = models.DateTimeField(blank=True, null=True, verbose_name='销售日期')
    purchaser = models.ForeignKey(Customer, blank=True, null=True, verbose_name='购买者')
    info = models.TextField(blank=True, null=True, verbose_name='产品信息')
    tag = models.ManyToManyField(Tag, blank=True, verbose_name='标签')
    is_enable = models.BooleanField(default=True, verbose_name='是否可见')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '产品'
        verbose_name_plural = '产品信息'

    def __str__(self):
        return self.name
