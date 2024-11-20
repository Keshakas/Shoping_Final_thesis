from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name="Nuotrauka", upload_to="profile_pics", default="profile_pics/default.png")
    class Meta:
        verbose_name = "Profilis"
        verbose_name_plural = "Profiliai"
    def __str__(self):
        return f"{self.user.username} profilis"


class Store(models.Model):
    name = models.CharField(verbose_name="Parduotuvė", max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Parduotuvė"
        verbose_name_plural = "Parduotuvės"


class Category(models.Model):
    name = models.CharField(verbose_name="Kategorija", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategorija"
        verbose_name_plural = "Kategorijos"


class Product(models.Model):
    name = models.CharField(verbose_name="Produktas", max_length=100)
    category = models.ForeignKey(Category, verbose_name="Kategorija", on_delete=models.CASCADE)

    def __str__(self):
        #return f"{self.name} - {self.category.name}"
        return self.name

    class Meta:
        verbose_name = "Produktas"
        verbose_name_plural = "Produktai"


class ShoppingCart(models.Model):
    date = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    user = models.ForeignKey(User, verbose_name="Vartotojas", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.date} -- "

    class Meta:
        verbose_name = "Pirkinių krepšelis"
        verbose_name_plural = "Pirkinių krepšeliai"
        ordering = ['-date']


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, verbose_name="Produktas", on_delete=models.CASCADE)
    store = models.ForeignKey(Store, verbose_name="Parduotuvė", on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(verbose_name="Kaina", max_digits=10, decimal_places=2)
    cart = models.ForeignKey(ShoppingCart, verbose_name="Pirkinių krepšelis", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.price} {self.cart}"

    class Meta:
        verbose_name = "Produkto kaina"
        verbose_name_plural = "Produktų kainos"


