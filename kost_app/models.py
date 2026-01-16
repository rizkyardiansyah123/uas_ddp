from django.db import models
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
    ktp = models.ImageField(upload_to='ktp_images/', blank=True, null=True, help_text='Upload foto KTP Anda')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nama_penyewa} - {self.kost.nama}"
    
    class Meta:
        ordering = ['-created_at']
