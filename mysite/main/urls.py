from django.urls import path
from django.conf.urls.static import static
from mysite import settings
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('parts/', views.parts, name='parts'),
    path('where/', views.map, name='map'),
    path('contact/', views.contacts, name='contacts'),
    path('account/', views.account, name='account'),
    path('cart/', views.cart, name='cart'),
    path('price/', views.price, name='price'),
]

# Loading in File Images
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
