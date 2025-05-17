from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DeleteView, TemplateView, CreateView
from django.urls import reverse_lazy
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from .forms import IngredientForm, MenuItemForm, RecipeRequirementForm, PurchaseForm
from django.db.models import Sum, F
from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required




    


class HomePageView(TemplateView):    
    template_name = 'inventory/home.html'    
    context_object_name = 'home'

class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'inventory/ingredient_form.html'
    success_url = reverse_lazy('inventory:ingredients')
    login_url = 'inventory:login'

class IngredientListView(ListView):
    model = Ingredient
    template_name = 'inventory/inventory_list.html'
    context_object_name = 'ingredients'

class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredient
    template_name = 'inventory/ingredient_confirm_delete.html'
    success_url = reverse_lazy('inventory:ingredients')
    login_url = 'inventory:login'

class MenuItemListView(ListView):
    model = MenuItem
    template_name = 'inventory/menu.html'
    context_object_name = 'menu_items'

    def get_queryset(self):
        return MenuItem.objects.prefetch_related('requirements__ingredient')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passa todos os itens para a variável destaque_items para o template usar
        context['destaque_items'] = self.get_queryset()  
        # Se quiser manter menu_items também (opcional)
        context['menu_items'] = self.get_queryset()
        return context
    
class MenuItemCreateView(LoginRequiredMixin, CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'inventory/menuitem_form.html'
    success_url = '/inventory/menu/'
    

@login_required(login_url="inventory:login")
def purchase_create_view(request):
    error = None
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            requirements = purchase.menu_item.requirements.all()
            # Verifica se há estoque suficiente
            for req in requirements:
                if req.ingredient.quantity < req.quantity:
                    error = f"Estoque insuficiente para {req.ingredient.name}"
                    break
            else:
                # Desconta os ingredientes e salva
                for req in requirements:
                    req.ingredient.quantity -= req.quantity
                    req.ingredient.save()
                purchase.save()
                return redirect('/inventory/purchases/')
    else:
        form = PurchaseForm()
    return render(request, 'inventory/purchase_form.html', {'form': form, 'error': error})

    

class PurchaseListView(ListView):
    model = Purchase
    template_name = 'inventory/purchases.html'
    context_object_name = 'purchases'

class RecipeRequirementCreateView(LoginRequiredMixin, CreateView):
    model = RecipeRequirement
    form_class = RecipeRequirementForm
    template_name = 'inventory/reciperequirement_form.html'
    success_url = '/inventory/menu/'
    login_url = 'inventory:login'

class ReportView(TemplateView):
    template_name = 'inventory/report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        purchases = Purchase.objects.all()
        total_revenue = purchases.aggregate(total=Sum(F('menu_item__price')))['total'] or 0

        total_cost = 0
        for purchase in purchases:
            requirements = RecipeRequirement.objects.filter(menu_item=purchase.menu_item)
            for r in requirements:
                total_cost += Decimal(r.quantity) * r.ingredient.price_per_unit


        context['total_revenue'] = total_revenue
        context['total_cost'] = total_cost
        context['profit'] = total_revenue - total_cost
        return context
    

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['inventory'] = Ingredient.objects.all()
        context['purchases'] = Purchase.objects.select_related('menu_item').all()
        context['menu_items'] = MenuItem.objects.prefetch_related('requirements__ingredient').all()
        
        total_revenue = Purchase.objects.aggregate(
            total_revenue=Sum(F('menu_item__price'))
        )['total_revenue'] or Decimal('0.00')
        
        total_cost = Decimal('0.00')
        for purchase in context['purchases']:
            for req in purchase.menu_item.requirements.all():
                total_cost += Decimal(req.quantity) * req.ingredient.price_per_unit
        
        profit = total_revenue - total_cost
        
        context['total_revenue'] = total_revenue
        context['total_cost'] = total_cost
        context['profit'] = profit
        
        return context
    


