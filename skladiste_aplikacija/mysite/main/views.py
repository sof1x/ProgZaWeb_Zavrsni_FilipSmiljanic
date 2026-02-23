from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import F, Sum, FloatField, ExpressionWrapper
from django.db.models.functions import Coalesce

from .models import Warehouse, Product, StockItem


@login_required
def homepage(request):
    warehouses = Warehouse.objects.all()
    products_count = Product.objects.count()
    stock_count = StockItem.objects.count()

    context = {
        "warehouses": warehouses,
        "products_count": products_count,
        "stock_count": stock_count,
    }

    return render(request, "main/dashboard.html", context)


class WarehouseListView(ListView):
    model = Warehouse
    template_name = "main/warehouse_list.html"
    context_object_name = "warehouses"

    def get_queryset(self):
        query = self.request.GET.get("q")

        if query:
            return Warehouse.objects.filter(name__icontains=query)

        return Warehouse.objects.all()


class ProductListView(ListView):
    model = Product
    template_name = "main/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        query = self.request.GET.get("q")

        if query:
            return Product.objects.filter(name__icontains=query)

        return Product.objects.all()


class StockItemListView(ListView):
    model = StockItem
    template_name = "main/stockitem_list.html"
    context_object_name = "items"

    def get_queryset(self):
        qs = (
            StockItem.objects
            .select_related("product", "warehouse")
            .annotate(
                total_value=ExpressionWrapper(
                    F("quantity") * F("product__price"),
                    output_field=FloatField(),
                )
            )
        )

        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(product__name__icontains=q)

        warehouse_id = self.request.GET.get("warehouse")
        if warehouse_id:
            qs = qs.filter(warehouse_id=warehouse_id)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        base_qs = self.get_queryset()

        context["total_quantity"] = base_qs.aggregate(
            total=Coalesce(Sum("quantity"), 0)
        )["total"]

        context["total_value_sum"] = base_qs.aggregate(
            total=Coalesce(
                Sum("total_value"),
                0.0,
                output_field=FloatField(),
    )
)["total"]

        context["warehouses"] = Warehouse.objects.all()

        return context


class ProductCreateView(CreateView):
    model = Product
    fields = ["name", "description", "price"]
    template_name = "main/product_form.html"
    success_url = reverse_lazy("main:products")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs.update({
                "class": "w-full border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            })
        return form


class ProductUpdateView(UpdateView):
    model = Product
    fields = ["name", "description", "price"]
    template_name = "main/product_form.html"
    success_url = reverse_lazy("main:products")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs.update({
                "class": "w-full border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            })
        return form


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "main/product_confirm_delete.html"
    success_url = reverse_lazy("main:products")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("main:homepage")
    else:
        form = UserCreationForm()

    for field in form.fields.values():
        field.widget.attrs.update({
            "class": "w-full border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        })

    return render(request, "registration/register.html", {"form": form})