import random

from django.core.management.base import BaseCommand
from django.db import transaction

from main.models import Warehouse, Product, StockItem
from main.factory import (
    WarehouseFactory,
    ProductFactory,
    StockItemFactory,
)

NUM_WAREHOUSES = 5
NUM_PRODUCTS = 20
NUM_STOCK_ITEMS = 50


class Command(BaseCommand):
    help = "Generate test data for inventory"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")

        models = [StockItem, Product, Warehouse]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating warehouses...")
        for _ in range(NUM_WAREHOUSES):
            WarehouseFactory()

        self.stdout.write("Creating products...")
        for _ in range(NUM_PRODUCTS):
            ProductFactory()

        self.stdout.write("Creating stock items...")
        for _ in range(NUM_STOCK_ITEMS):
            StockItemFactory()

        self.stdout.write(self.style.SUCCESS("Test data generated!"))