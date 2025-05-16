from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Página Inicial do Projeto")

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('inventory/', include(('inventory.urls', 'inventory'), namespace='inventory')),

]
