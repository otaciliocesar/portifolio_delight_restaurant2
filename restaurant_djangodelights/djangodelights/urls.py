from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from inventory.views import HomePageView
from django.conf import settings
from django.conf.urls.static import static

def home(request):
    return HttpResponse("Página Inicial do Projeto")

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('', HomePageView.as_view(), name='home'),
    path('inventory/', include(('inventory.urls', 'inventory'), namespace='inventory')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
