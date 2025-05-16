import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangodelights.settings')
django.setup()

# Cole aqui os códigos de 1 a 6
from inventory.models import Ingredient, MenuItem, RecipeRequirement, Purchase
from django.db.models import Sum, F

# 1. Inventário atual
inventory = Ingredient.objects.all()
for item in inventory:
    print(f"{item.name}: {item.quantity} {item.unit}")

# 2. Compras realizadas
purchases = Purchase.objects.select_related('menu_item').all()
for purchase in purchases:
    print(f"{purchase.menu_item.title} comprado em {purchase.timestamp}")

# 3. Cardápio e ingredientes necessários
menu_items = MenuItem.objects.prefetch_related('requirements__ingredient').all()
for item in menu_items:
    print(f"Item: {item.title} - Preço: R$ {item.price}")
    print("Ingredientes necessários:")
    for req in item.requirements.all():
        print(f" - {req.ingredient.name}: {req.quantity} {req.ingredient.unit}")

# 4. Receita total com base nas compras
total_revenue = Purchase.objects.aggregate(
    total=Sum(F('menu_item__price'))
)['total'] or 0
print(f"Receita total: R$ {total_revenue:.2f}")

# 5. Custo total de ingredientes usados nas compras
total_cost = 0
for purchase in purchases:
    for req in purchase.menu_item.requirements.all():
        total_cost += req.quantity * req.ingredient.price_per_unit
print(f"Custo total: R$ {total_cost:.2f}")

# 6. Lucro = receita - custo
profit = total_revenue - total_cost
print(f"Lucro total: R$ {profit:.2f}")