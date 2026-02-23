import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User

from .models import Warehouse, Product, StockItem


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")


class WarehouseFactory(DjangoModelFactory):
    class Meta:
        model = Warehouse

    name = factory.Faker("company")
    location = factory.Faker("city")
    capacity = factory.Faker("random_int", min=100, max=1000)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("word")
    description = factory.Faker("sentence")
    price = factory.Faker("pyfloat", left_digits=3, right_digits=2, positive=True)


class StockItemFactory(DjangoModelFactory):
    class Meta:
        model = StockItem

    warehouse = factory.Iterator(Warehouse.objects.all())
    product = factory.Iterator(Product.objects.all())
    quantity = factory.Faker("random_int", min=1, max=100)