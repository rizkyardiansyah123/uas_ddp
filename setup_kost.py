import os
import sys

def create_file(path, content):
    """Membuat file dengan konten"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Created: {path}")

def setup_kost_project():
    """Setup project Django untuk web sewa kost"""
    
    base_dir = "kost_rental"
    
    # Structure
    dirs = [
        f"{base_dir}/kost_project",
        f"{base_dir}/kost_app",
        f"{base_dir}/kost_app/templates",
        f"{base_dir}/kost_app/static/css",
        f"{base_dir}/kost_app/static/js",
        f"{base_dir}/kost_app/static/images",
        f"{base_dir}/media/kost_images",
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    print("📁 Creating project structure...\n")
    
    # 1. kost_project/settings.py
    settings_content = """from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-change-this-in-production-123456789'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'kost_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kost_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'kost_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'id-id'
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
"""
    create_file(f"{base_dir}/kost_project/settings.py", settings_content)

    # 2. kost_project/urls.py
    urls_content = """from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('kost_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
    create_file(f"{base_dir}/kost_project/urls.py", urls_content)

    # 3. kost_project/wsgi.py
    wsgi_content = """import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kost_project.settings')
application = get_wsgi_application()
"""
    create_file(f"{base_dir}/kost_project/wsgi.py", wsgi_content)

    # 4. kost_project/__init__.py
    create_file(f"{base_dir}/kost_project/__init__.py", "")

    # 5. kost_app/models.py
    models_content = """from django.db import models
from django.contrib.auth.models import User

class Kost(models.Model):
    JENIS_CHOICES = [
        ('putra', 'Putra'),
        ('putri', 'Putri'),
        ('campur', 'Campur'),
    ]
    
    nama = models.CharField(max_length=200)
    alamat = models.TextField()
    jenis = models.CharField(max_length=10, choices=JENIS_CHOICES)
    harga = models.DecimalField(max_digits=10, decimal_places=0)
    fasilitas = models.TextField()
    deskripsi = models.TextField()
    gambar = models.ImageField(upload_to='kost_images/', blank=True, null=True)
    tersedia = models.BooleanField(default=True)
    jumlah_kamar = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nama
    
    class Meta:
        ordering = ['-created_at']

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    kost = models.ForeignKey(Kost, on_delete=models.CASCADE)
    nama_penyewa = models.CharField(max_length=200)
    email = models.EmailField()
    telepon = models.CharField(max_length=20)
    tanggal_mulai = models.DateField()
    durasi_bulan = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    catatan = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nama_penyewa} - {self.kost.nama}"
    
    class Meta:
        ordering = ['-created_at']
"""
    create_file(f"{base_dir}/kost_app/models.py", models_content)

    # 6. kost_app/views.py
    views_content = """from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Kost, Booking
from .forms import BookingForm

def home(request):
    kost_list = Kost.objects.filter(tersedia=True)
    jenis = request.GET.get('jenis')
    if jenis:
        kost_list = kost_list.filter(jenis=jenis)
    
    context = {
        'kost_list': kost_list,
        'jenis_filter': jenis,
    }
    return render(request, 'home.html', context)

def kost_detail(request, pk):
    kost = get_object_or_404(Kost, pk=pk)
    return render(request, 'kost_detail.html', {'kost': kost})

def booking(request, pk):
    kost = get_object_or_404(Kost, pk=pk)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.kost = kost
            booking.save()
            messages.success(request, 'Booking berhasil! Kami akan menghubungi Anda segera.')
            return redirect('home')
    else:
        form = BookingForm()
    
    return render(request, 'booking.html', {'form': form, 'kost': kost})
"""
    create_file(f"{base_dir}/kost_app/views.py", views_content)

    # 7. kost_app/forms.py
    forms_content = """from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['nama_penyewa', 'email', 'telepon', 'tanggal_mulai', 'durasi_bulan', 'catatan']
        widgets = {
            'nama_penyewa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Lengkap'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'telepon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '08xxxxxxxxxx'}),
            'tanggal_mulai': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'durasi_bulan': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Berapa bulan?'}),
            'catatan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Catatan tambahan (opsional)'}),
        }
"""
    create_file(f"{base_dir}/kost_app/forms.py", forms_content)

    # 8. kost_app/urls.py
    app_urls_content = """from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('kost/<int:pk>/', views.kost_detail, name='kost_detail'),
    path('kost/<int:pk>/booking/', views.booking, name='booking'),
]
"""
    create_file(f"{base_dir}/kost_app/urls.py", app_urls_content)

    # 9. kost_app/admin.py
    admin_content = """from django.contrib import admin
from .models import Kost, Booking
from django.utils.html import format_html

@admin.register(Kost)
class KostAdmin(admin.ModelAdmin):
    list_display = ['nama', 'jenis', 'harga_display', 'jumlah_kamar', 'status_display', 'created_at']
    list_filter = ['jenis', 'tersedia', 'created_at']
    search_fields = ['nama', 'alamat', 'deskripsi']
    list_editable = ['tersedia']
    readonly_fields = ['created_at', 'preview_gambar']
    
    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('nama', 'jenis', 'alamat', 'harga')
        }),
        ('Detail Kost', {
            'fields': ('deskripsi', 'fasilitas', 'jumlah_kamar')
        }),
        ('Media', {
            'fields': ('gambar', 'preview_gambar')
        }),
        ('Status', {
            'fields': ('tersedia', 'created_at')
        }),
    )
    
    def harga_display(self, obj):
        return f"Rp {obj.harga:,.0f}"
    harga_display.short_description = 'Harga/Bulan'
    
    def status_display(self, obj):
        if obj.tersedia:
            return format_html('<span style="color: green; font-weight: bold;">✓ Tersedia</span>')
        return format_html('<span style="color: red; font-weight: bold;">✗ Penuh</span>')
    status_display.short_description = 'Status'
    
    def preview_gambar(self, obj):
        if obj.gambar:
            return format_html('<img src="{}" width="300" style="border-radius: 10px;"/>', obj.gambar.url)
        return "Tidak ada gambar"
    preview_gambar.short_description = 'Preview Gambar'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['nama_penyewa', 'kost', 'telepon', 'status_display', 'tanggal_mulai', 'durasi_bulan', 'created_at']
    list_filter = ['status', 'created_at', 'tanggal_mulai']
    search_fields = ['nama_penyewa', 'email', 'telepon', 'kost__nama']
    list_editable = ['status']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Informasi Penyewa', {
            'fields': ('nama_penyewa', 'email', 'telepon')
        }),
        ('Detail Booking', {
            'fields': ('kost', 'tanggal_mulai', 'durasi_bulan', 'catatan')
        }),
        ('Status', {
            'fields': ('status', 'created_at')
        }),
    )
    
    def status_display(self, obj):
        colors = {
            'pending': 'orange',
            'confirmed': 'green',
            'cancelled': 'red'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    status_display.short_description = 'Status'
    
    actions = ['confirm_booking', 'cancel_booking']
    
    def confirm_booking(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} booking telah dikonfirmasi.')
    confirm_booking.short_description = 'Konfirmasi booking yang dipilih'
    
    def cancel_booking(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} booking telah dibatalkan.')
    cancel_booking.short_description = 'Batalkan booking yang dipilih'
"""
    create_file(f"{base_dir}/kost_app/admin.py", admin_content)

    # 10. kost_app/__init__.py
    create_file(f"{base_dir}/kost_app/__init__.py", "")

    # 11. kost_app/apps.py
    apps_content = """from django.apps import AppConfig

class KostAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kost_app'
"""
    create_file(f"{base_dir}/kost_app/apps.py", apps_content)

    # 12. manage.py
    manage_content = """#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kost_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)
"""
    create_file(f"{base_dir}/manage.py", manage_content)

    # 13. templates/base.html
    base_html = """{% load static %}
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Sewa Kost{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary sticky-top">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">
                <i class="fas fa-home"></i> KostKu
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'home' %}">Beranda</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'home' %}?jenis=putra">Kost Putra</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'home' %}?jenis=putri">Kost Putri</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    {% if messages %}
    <div class="container mt-3">
        {% for message in messages %}
        <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    {% block content %}{% endblock %}

    <footer class="bg-dark text-white py-4 mt-5">
        <div class="container text-center">
            <p>&copy; 2024 KostKu. Semua hak dilindungi.</p>
            <p><i class="fas fa-phone"></i> 0812-3456-7890 | <i class="fas fa-envelope"></i> info@kostku.com</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{% static 'js/script.js' %}"></script>
</body>
</html>
"""
    create_file(f"{base_dir}/kost_app/templates/base.html", base_html)

    # 14. templates/home.html
    home_html = """{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="hero-section">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-6">
                <h1 class="display-4 fw-bold text-white animate-fade-in">Temukan Kost Impian Anda</h1>
                <p class="lead text-white">Cari kost nyaman dengan harga terjangkau di lokasi strategis</p>
                <a href="#kost-list" class="btn btn-light btn-lg">Lihat Semua Kost</a>
            </div>
        </div>
    </div>
</div>

<div class="container my-5" id="kost-list">
    <div class="row mb-4">
        <div class="col-12">
            <h2 class="text-center mb-4">Daftar Kost Tersedia</h2>
            <div class="filter-buttons text-center">
                <a href="{% url 'home' %}" class="btn {% if not jenis_filter %}btn-primary{% else %}btn-outline-primary{% endif %} mx-1">Semua</a>
                <a href="{% url 'home' %}?jenis=putra" class="btn {% if jenis_filter == 'putra' %}btn-primary{% else %}btn-outline-primary{% endif %} mx-1">Putra</a>
                <a href="{% url 'home' %}?jenis=putri" class="btn {% if jenis_filter == 'putri' %}btn-primary{% else %}btn-outline-primary{% endif %} mx-1">Putri</a>
                <a href="{% url 'home' %}?jenis=campur" class="btn {% if jenis_filter == 'campur' %}btn-primary{% else %}btn-outline-primary{% endif %} mx-1">Campur</a>
            </div>
        </div>
    </div>

    <div class="row">
        {% for kost in kost_list %}
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="card kost-card h-100 shadow-sm">
                {% if kost.gambar %}
                <img src="{{ kost.gambar.url }}" class="card-img-top" alt="{{ kost.nama }}">
                {% else %}
                <div class="card-img-top bg-secondary d-flex align-items-center justify-content-center" style="height: 200px;">
                    <i class="fas fa-home fa-4x text-white"></i>
                </div>
                {% endif %}
                <div class="card-body">
                    <span class="badge bg-info mb-2">{{ kost.get_jenis_display }}</span>
                    <h5 class="card-title">{{ kost.nama }}</h5>
                    <p class="card-text text-muted"><i class="fas fa-map-marker-alt"></i> {{ kost.alamat|truncatewords:10 }}</p>
                    <h4 class="text-primary">Rp {{ kost.harga|floatformat:0 }}<small class="text-muted">/bulan</small></h4>
                    <p class="card-text"><small><i class="fas fa-door-open"></i> {{ kost.jumlah_kamar }} kamar tersedia</small></p>
                </div>
                <div class="card-footer bg-transparent">
                    <a href="{% url 'kost_detail' kost.pk %}" class="btn btn-primary w-100">Lihat Detail</a>
                </div>
            </div>
        </div>
        {% empty %}
        <div class="col-12 text-center">
            <p class="lead">Belum ada kost tersedia.</p>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
"""
    create_file(f"{base_dir}/kost_app/templates/home.html", home_html)

    # 15. templates/kost_detail.html
    detail_html = """{% extends 'base.html' %}

{% block title %}{{ kost.nama }} - Sewa Kost{% endblock %}

{% block content %}
<div class="container my-5">
    <!-- Breadcrumb -->
    <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="{% url 'home' %}">Beranda</a></li>
            <li class="breadcrumb-item active">{{ kost.nama }}</li>
        </ol>
    </nav>
    
    <div class="row">
        <div class="col-lg-8">
            <!-- Gambar Utama -->
            <div class="card shadow-sm mb-4">
                {% if kost.gambar %}
                <img src="{{ kost.gambar.url }}" class="card-img-top" alt="{{ kost.nama }}" style="max-height: 500px; object-fit: cover;">
                {% else %}
                <div class="card-img-top bg-secondary d-flex align-items-center justify-content-center" style="height: 400px;">
                    <i class="fas fa-home fa-5x text-white"></i>
                </div>
                {% endif %}
            </div>
            
            <!-- Informasi Detail -->
            <div class="card shadow-sm mb-4">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-3">
                        <div>
                            <span class="badge bg-info mb-2">{{ kost.get_jenis_display }}</span>
                            <h2 class="card-title mb-0">{{ kost.nama }}</h2>
                        </div>
                        {% if kost.tersedia %}
                        <span class="badge bg-success fs-6">Tersedia</span>
                        {% else %}
                        <span class="badge bg-danger fs-6">Penuh</span>
                        {% endif %}
                    </div>
                    
                    <p class="text-muted mb-4">
                        <i class="fas fa-map-marker-alt"></i> {{ kost.alamat }}
                    </p>
                    
                    <!-- Quick Info -->
                    <div class="row mb-4">
                        <div class="col-md-4 mb-3">
                            <div class="info-box p-3 bg-light rounded text-center">
                                <i class="fas fa-door-open fa-2x text-primary mb-2"></i>
                                <h5>{{ kost.jumlah_kamar }}</h5>
                                <small class="text-muted">Kamar Tersedia</small>
                            </div>
                        </div>
                        <div class="col-md-4 mb-3">
                            <div class="info-box p-3 bg-light rounded text-center">
                                <i class="fas fa-venus-mars fa-2x text-primary mb-2"></i>
                                <h5>{{ kost.get_jenis_display }}</h5>
                                <small class="text-muted">Jenis Kost</small>
                            </div>
                        </div>
                        <div class="col-md-4 mb-3">
                            <div class="info-box p-3 bg-light rounded text-center">
                                <i class="fas fa-money-bill-wave fa-2x text-primary mb-2"></i>
                                <h5>Rp {{ kost.harga|floatformat:0 }}</h5>
                                <small class="text-muted">Per Bulan</small>
                            </div>
                        </div>
                    </div>
                    
                    <hr>
                    
                    <!-- Deskripsi -->
                    <div class="mb-4">
                        <h4><i class="fas fa-info-circle text-primary"></i> Deskripsi</h4>
                        <p class="text-justify">{{ kost.deskripsi }}</p>
                    </div>
                    
                    <hr>
                    
                    <!-- Fasilitas -->
                    <div class="mb-4">
                        <h4><i class="fas fa-check-circle text-primary"></i> Fasilitas</h4>
                        <div class="row mt-3">
                            {% for fasilitas in kost.fasilitas.splitlines %}
                            <div class="col-md-6 mb-2">
                                <div class="d-flex align-items-center">
                                    <i class="fas fa-check-circle text-success me-2"></i>
                                    <span>{{ fasilitas }}</span>
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                    
                    <hr>
                    
                    <!-- Peraturan & Info Tambahan -->
                    <div class="mb-4">
                        <h4><i class="fas fa-clipboard-list text-primary"></i> Informasi Tambahan</h4>
                        <ul class="list-unstyled mt-3">
                            <li class="mb-2"><i class="fas fa-clock text-muted me-2"></i> Jam kunjungan: 24 jam</li>
                            <li class="mb-2"><i class="fas fa-id-card text-muted me-2"></i> Wajib KTP untuk pendaftaran</li>
                            <li class="mb-2"><i class="fas fa-calendar-alt text-muted me-2"></i> Pembayaran setiap tanggal 1</li>
                            <li class="mb-2"><i class="fas fa-handshake text-muted me-2"></i> Deposit 1 bulan</li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <!-- Lokasi -->
            <div class="card shadow-sm mb-4">
                <div class="card-body">
                    <h4><i class="fas fa-map-marked-alt text-primary"></i> Lokasi</h4>
                    <p class="text-muted mb-3"><i class="fas fa-map-marker-alt"></i> {{ kost.alamat }}</p>
                    <div class="bg-light p-3 rounded text-center">
                        <i class="fas fa-map fa-3x text-secondary"></i>
                        <p class="mt-2 mb-0 text-muted">Peta lokasi akan ditampilkan di sini</p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Sidebar Booking -->
        <div class="col-lg-4">
            <div class="card shadow-sm sticky-top" style="top: 80px;">
                <div class="card-body">
                    <div class="text-center mb-3">
                        <h3 class="text-primary mb-0">Rp {{ kost.harga|floatformat:0 }}</h3>
                        <p class="text-muted">per bulan</p>
                    </div>
                    
                    <hr>
                    
                    <!-- Detail Info -->
                    <div class="mb-3">
                        <div class="d-flex justify-content-between mb-2">
                            <span><i class="fas fa-door-open text-primary"></i> Kamar tersedia</span>
                            <strong>{{ kost.jumlah_kamar }}</strong>
                        </div>
                        <div class="d-flex justify-content-between mb-2">
                            <span><i class="fas fa-venus-mars text-primary"></i> Jenis</span>
                            <strong>{{ kost.get_jenis_display }}</strong>
                        </div>
                        <div class="d-flex justify-content-between mb-2">
                            <span><i class="fas fa-calendar text-primary"></i> Ditambahkan</span>
                            <strong>{{ kost.created_at|date:"d M Y" }}</strong>
                        </div>
                    </div>
                    
                    <hr>
                    
                    <!-- Action Buttons -->
                    {% if kost.tersedia %}
                    <a href="{% url 'booking' kost.pk %}" class="btn btn-primary btn-lg w-100 mb-2">
                        <i class="fas fa-calendar-check"></i> Booking Sekarang
                    </a>
                    {% else %}
                    <button class="btn btn-secondary btn-lg w-100 mb-2" disabled>
                        <i class="fas fa-times-circle"></i> Sudah Penuh
                    </button>
                    {% endif %}
                    
                    <a href="https://wa.me/6281234567890?text=Halo, saya tertarik dengan {{ kost.nama }}" 
                       class="btn btn-success btn-lg w-100 mb-2" target="_blank">
                        <i class="fab fa-whatsapp"></i> Hubungi via WhatsApp
                    </a>
                    
                    <a href="tel:081234567890" class="btn btn-outline-primary w-100">
                        <i class="fas fa-phone"></i> Telepon Sekarang
                    </a>
                    
                    <hr>
                    
                    <!-- Share -->
                    <div class="text-center">
                        <p class="text-muted mb-2">Bagikan:</p>
                        <div class="d-flex justify-content-center gap-2">
                            <a href="#" class="btn btn-sm btn-outline-primary rounded-circle" style="width: 40px; height: 40px;">
                                <i class="fab fa-facebook-f"></i>
                            </a>
                            <a href="#" class="btn btn-sm btn-outline-info rounded-circle" style="width: 40px; height: 40px;">
                                <i class="fab fa-twitter"></i>
                            </a>
                            <a href="#" class="btn btn-sm btn-outline-success rounded-circle" style="width: 40px; height: 40px;">
                                <i class="fab fa-whatsapp"></i>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Tips Section -->
            <div class="card shadow-sm mt-4">
                <div class="card-body">
                    <h5><i class="fas fa-lightbulb text-warning"></i> Tips Memilih Kost</h5>
                    <ul class="small text-muted">
                        <li>Cek kondisi kamar langsung</li>
                        <li>Tanyakan detail fasilitas</li>
                        <li>Pastikan lokasi strategis</li>
                        <li>Baca aturan kost dengan teliti</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Back Button -->
    <div class="text-center mt-4">
        <a href="{% url 'home' %}" class="btn btn-outline-secondary">
            <i class="fas fa-arrow-left"></i> Kembali ke Daftar Kost
        </a>
    </div>
</div>
{% endblock %}
"""
    create_file(f"{base_dir}/kost_app/templates/kost_detail.html", detail_html)

    # 16. templates/booking.html
    booking_html = """{% extends 'base.html' %}

{% block title %}Booking {{ kost.nama }}{% endblock %}

{% block content %}
<div class="container my-5">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <div class="card shadow">
                <div class="card-header bg-primary text-white">
                    <h3 class="mb-0"><i class="fas fa-calendar-check"></i> Form Booking Kost</h3>
                </div>
                <div class="card-body">
                    <div class="alert alert-info">
                        <strong>{{ kost.nama }}</strong><br>
                        <i class="fas fa-map-marker-alt"></i> {{ kost.alamat }}<br>
                        <strong class="text-primary">Rp {{ kost.harga|floatformat:0 }}/bulan</strong>
                    </div>
                    
                    <form method="post" class="needs-validation" novalidate>
                        {% csrf_token %}
                        
                        <div class="mb-3">
                            <label class="form-label">Nama Lengkap *</label>
                            {{ form.nama_penyewa }}
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Email *</label>
                            {{ form.email }}
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Nomor Telepon *</label>
                            {{ form.telepon }}
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Tanggal Mulai *</label>
                                {{ form.tanggal_mulai }}
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Durasi (bulan) *</label>
                                {{ form.durasi_bulan }}
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Catatan</label>
                            {{ form.catatan }}
                        </div>
                        
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="fas fa-paper-plane"></i> Kirim Booking
                            </button>
                            <a href="{% url 'kost_detail' kost.pk %}" class="btn btn-outline-secondary">Batal</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
    create_file(f"{base_dir}/kost_app/templates/booking.html", booking_html)

    # 17. static/css/style.css
    css_content = """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f8f9fa;
}

.hero-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 100px 0;
    margin-bottom: 50px;
}

.animate-fade-in {
    animation: fadeIn 1s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.kost-card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: none;
    border-radius: 15px;
    overflow: hidden;
}

.kost-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.kost-card img {
    height: 200px;
    object-fit: cover;
}

.card-footer {
    border-top: none;
}

.filter-buttons .btn {
    border-radius: 25px;
    padding: 10px 25px;
    margin: 5px;
}

.sticky-top {
    position: sticky;
}

footer {
    margin-top: auto;
}

.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
}

.btn-primary:hover {
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    transform: scale(1.05);
    transition: all 0.3s ease;
}

.badge {
    padding: 8px 15px;
    border-radius: 20px;
}

.form-control:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}
"""
    create_file(f"{base_dir}/kost_app/static/css/style.css", css_content)

    # 18. static/js/script.js
    js_content = """// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Form validation
(function() {
    'use strict';
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
})();

// Animate cards on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.kost-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'all 0.6s ease';
    observer.observe(card);
});
"""
    create_file(f"{base_dir}/kost_app/static/js/script.js", js_content)

    # 19. requirements.txt
    requirements_content = """Django>=4.2,<5.0
Pillow>=10.0.0
"""
    create_file(f"{base_dir}/requirements.txt", requirements_content)

    # 20. README.md
    readme_content = """# Web Sewa Kost - Django

Aplikasi web untuk menyewakan kost dengan desain modern dan dinamis.

## Fitur
- Tampilan daftar kost dengan filter
- Detail kost lengkap dengan fasilitas
- Form booking kost
- Admin panel untuk mengelola kost dan booking
- Desain responsive dan modern

## Instalasi

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Jalankan migrasi database:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Buat superuser untuk admin:
```bash
python manage.py createsuperuser
```

4. Jalankan server:
```bash
python manage.py runserver
```

5. Buka browser: http://127.0.0.1:8000

## Admin Panel
Akses admin panel di: http://127.0.0.1:8000/admin

## Struktur Folder
```
kost_rental/
├── kost_project/          # Konfigurasi project
├── kost_app/              # Aplikasi utama
│   ├── templates/         # HTML templates
│   ├── static/            # CSS, JS, Images
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   └── forms.py           # Forms
├── media/                 # Upload gambar
├── manage.py
└── requirements.txt
```

## Teknologi
- Django 4.2+
- Bootstrap 5
- Font Awesome
- SQLite (default)
"""
    create_file(f"{base_dir}/README.md", readme_content)

    print("\n" + "="*60)
    print("✅ PROJECT BERHASIL DIBUAT!")
    print("="*60)
    print(f"\nFolder project: {base_dir}/")
    print("\nLangkah selanjutnya:")
    print(f"1. cd {base_dir}")
    print("2. pip install -r requirements.txt")
    print("3. python manage.py makemigrations")
    print("4. python manage.py migrate")
    print("5. python manage.py createsuperuser")
    print("6. python manage.py runserver")
    print("\n✨ Selamat menggunakan!")

if __name__ == "__main__":
    try:
        setup_kost_project()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)