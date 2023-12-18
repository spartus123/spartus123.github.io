from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=200)
    phone = models.IntegerField(null=True, blank=True)
    email = models.EmailField()
    def __str__(self):
        return self.name


CATEGORY_CHOICES = (
    ('PS', 'Papildai sportui'),
    ('PSV', 'Papildai sveikatai'),
    ('MD', 'Maistas dietai'),
    ('AKS', 'Aksesuarai'),
    ('KP', 'Kiti produktai'),

)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=5)
    product_image = models.ImageField(upload_to='product')

    def __str__(self):
        return self.title


class Files(models.Model):
    file = models.FileField(upload_to='file')

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.title

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    stripe_order_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_payment_status = models.CharField(max_length=100, blank=True, null=True)
    stripe_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)

STATUS_CHOICES = (
    ('Uzsakymas priimtas', 'Uzsakymas priimtas'),
    ('Paruosta siuntimui', 'Paruosta siuntimui'),
    ('Issiusta', 'Issiusta'),
    ('Pristatyta', 'Atsaukta'),
    ('Atsaukta', 'Atsaukta'),
)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Uzsakymas priimtas")
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default="" )
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    def __str__(self):
        return self.product.title

