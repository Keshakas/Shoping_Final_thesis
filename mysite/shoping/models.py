from django.db import models


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
        return f"{self.name} - {self.category.name}"

    class Meta:
        verbose_name = "Produktas"
        verbose_name_plural = "Produktai"


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, verbose_name="Produktas", on_delete=models.CASCADE)
    store = models.ForeignKey(Store, verbose_name="Parduotuvė", on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name="Kaina", max_digits=10, decimal_places=2, null=True, blank=True)
    date_checked = models.DateTimeField(verbose_name="Tikrinimo data", auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.store.name}:  {self.price}"

    class Meta:
        verbose_name = "Produkto kaina"
        verbose_name_plural = "Produktų kainos"
        ordering = ['-date_checked']
