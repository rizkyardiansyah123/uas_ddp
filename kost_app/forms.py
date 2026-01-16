from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['nama_penyewa', 'email', 'telepon', 'tanggal_mulai', 'durasi_bulan', 'ktp', 'catatan']
        widgets = {
            'nama_penyewa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Lengkap'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'telepon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '08xxxxxxxxxx'}),
            'tanggal_mulai': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'durasi_bulan': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Berapa bulan?'}),
            'ktp': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'catatan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Catatan tambahan (opsional)'}),
        }
