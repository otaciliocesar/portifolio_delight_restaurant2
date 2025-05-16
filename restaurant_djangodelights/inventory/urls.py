from django.urls import path
from .views import (
    HomePageView,
    IngredientListView,
    IngredientDeleteView,
    MenuItemListView,
    PurchaseListView,
    ReportView, 
    DashboardView
)
from . import views
from django.contrib.auth import views as auth_views

app = 'inventory'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='inventory:login'), name='logout'),
    path('home/', HomePageView.as_view(), name='home'),
    path('ingredients/', IngredientListView.as_view(), name='ingredients'),
    path('ingredients/delete/<int:pk>/', IngredientDeleteView.as_view(), name='ingredient-delete'),
    path('menu/', MenuItemListView.as_view(), name='menu'),
    path('purchases/', PurchaseListView.as_view(), name='purchases'),
    path('report/', ReportView.as_view(), name='report'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('ingredients/add/', views.IngredientCreateView.as_view(), name='ingredient-add'),
    path('menu/add/', views.MenuItemCreateView.as_view(), name='menuitem-add'),
    path('recipe/add/', views.RecipeRequirementCreateView.as_view(), name='reciperequirement-add'),
    path('purchase/add/', views.purchase_create_view, name='purchase-add'),
]
