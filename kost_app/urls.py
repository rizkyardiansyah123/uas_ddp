from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('kost/<int:pk>/', views.kost_detail, name='kost_detail'),
    path('kost/<int:pk>/booking/', views.booking, name='booking'),
    path('booking/success/<int:booking_id>/', views.booking_success, name='booking_success'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('accounts/', include('django.contrib.auth.urls')),
]
