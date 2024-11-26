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
    name = models.CharField(verbose_name="Pavadinimas", max_length=100, null=True, blank=True)

    def total(self):
        total_sum = 0
        for my_product in self.my_products.all():
            total_sum += my_product.price
        return total_sum

    def __str__(self):
        return f"{self.date} -- {self.name}"

    class Meta:
        verbose_name = "Pirkinių krepšelis"
        verbose_name_plural = "Pirkinių krepšeliai"
        ordering = ['-date']


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, verbose_name="Produktas", on_delete=models.CASCADE)
    store = models.ForeignKey(Store, verbose_name="Parduotuvė", on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(verbose_name="Kaina", max_digits=10, decimal_places=2)
    cart = models.ForeignKey(ShoppingCart, verbose_name="Pirkinių krepšelis", on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return f"{self.product.name} - {self.price} {self.cart}"

    class Meta:
        verbose_name = "Produkto kaina"
        verbose_name_plural = "Produktų kainos"


class SavedResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Susiejame su vartotoju
    store = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    url = models.URLField(max_length=2000, null=True, blank=True)
    saved_at = models.DateTimeField(auto_now_add=True) # Pridedame išsaugojimo laiką
    cart = models.ForeignKey(ShoppingCart, verbose_name="Pirkinių krepšelis", on_delete=models.CASCADE, null=True, blank=True, related_name="my_products")

    def __str__(self):
        return f"{self.name} ({self.store}) - {self.price} €  ({self.user})"

    class Meta:
        verbose_name = "Mano produkto kaina"
        verbose_name_plural = "Mano produktų kainos"
