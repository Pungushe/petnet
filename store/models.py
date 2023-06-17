from django.contrib.auth.models import User
from django.db import models

from django.core.files import File
from io import BytesIO
from PIL import Image

from django.template.defaultfilters import slugify


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    DRAFT = 'draft'
    WAITING_APPROVAL = 'waitingapproval'
    ACTIVE = 'active'
    DELETED = 'deleted'

    STATUS_CHOICES = (
        (DRAFT, 'В ожидании'),
        (WAITING_APPROVAL, 'Ожидающий подтверждения'),
        (ACTIVE, 'Активный'),
        (DELETED, 'Удаленный'),
    )

    user = models.ForeignKey(User, related_name="products", on_delete=models.CASCADE, verbose_name='Покупатель')
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE, verbose_name='Категории')
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')
    image = models.ImageField(upload_to='uploads/product_images/', blank=True, null=True, verbose_name='Изображение товара')
    thumbnail = models.ImageField(upload_to='uploads/product_images/thumbnail/', blank=True, null=True, verbose_name='Миниатюра')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=ACTIVE, verbose_name='Статус')

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.title

    def get_display_price(self):
        return self.price / 100

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return "https://via.placeholder.com/240x240x.jpg"

    def make_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        name = image.name.replace('uploads/product_images/', '')
        thumbnail = File(thumb_io, name=name)

        return thumbnail

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class Order(models.Model):
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    address = models.CharField(max_length=255 , verbose_name='Адрес')
    zipcode = models.CharField(max_length=255, verbose_name='Индекс')
    city = models.CharField(max_length=255, verbose_name='Город')
    paid_amount = models.IntegerField(blank=True, null=True, verbose_name='Количество')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    payment_intent =models.CharField(max_length=255, verbose_name='Оплата')
    created_by = models.ForeignKey(User, related_name="orders", on_delete=models.SET_NULL, null=True, verbose_name='Создан')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return self.first_name

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="items", on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Заказ товара"
        verbose_name_plural = "Заказ товаров"

    def __str__(self):
        return str(self.product)

    def get_display_price(self):
        return self.price / 100
