from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from inventory.views import HomePageView

def home(request):
    return HttpResponse("Página Inicial do Projeto")

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('', HomePageView.as_view(), name='home'),
    path('inventory/', include(('inventory.urls', 'inventory'), namespace='inventory')),

]
