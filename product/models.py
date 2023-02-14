from django.db import models
from django.contrib.auth import get_user_model
from category.models import Category
from ckeditor.fields import RichTextField


User = get_user_model()


class Product(models.Model):
    STATUS_CHOICES = (
        ('in_stock', 'В наличии'),
        ('out_of_stock', 'Нет в наличии')
    )

    owner = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='products')
    title = models.CharField(max_length=150)
    description = RichTextField(blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.RESTRICT)
    image = models.ImageField(upload_to='images')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.CharField(choices=STATUS_CHOICES, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_product')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')


    class Meta:
        unique_together = ['owner', 'product']


class Favorites(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_product')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')


    class Meta:
        unique_together = ['owner', 'product']
