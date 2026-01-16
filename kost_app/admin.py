from django.contrib import admin
from .models import Kost, Booking
from django.utils.html import format_html
from django.utils.safestring import mark_safe

@admin.register(Kost)
class KostAdmin(admin.ModelAdmin):
    list_display = ['nama', 'jenis', 'harga_display', 'jumlah_kamar', 'tersedia', 'status_display', 'created_at']
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
        return "Rp {:,.0f}".format(obj.harga)
    harga_display.short_description = 'Harga/Bulan'
    
    def status_display(self, obj):
        if obj.tersedia:
            return mark_safe('<span style="color: green; font-weight: bold;">✓ Tersedia</span>')
        return mark_safe('<span style="color: red; font-weight: bold;">✗ Penuh</span>')
    status_display.short_description = 'Status'
    
    def preview_gambar(self, obj):
        if obj.gambar:
            return mark_safe('<img src="{}" width="300" style="border-radius: 10px;"/>'.format(obj.gambar.url))
        return mark_safe('<span style="color: gray;">Tidak ada gambar</span>')
    preview_gambar.short_description = 'Preview Gambar'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['nama_penyewa', 'kost', 'telepon', 'status', 'status_display', 'tanggal_mulai', 'durasi_bulan', 'created_at']
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
        color = colors.get(obj.status, 'gray')
        label = obj.get_status_display()
        return mark_safe('<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold;">{}</span>'.format(color, label))
    status_display.short_description = 'Status Display'
    
    actions = ['confirm_booking', 'cancel_booking']
    
    def confirm_booking(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, '{} booking telah dikonfirmasi.'.format(updated))
    confirm_booking.short_description = 'Konfirmasi booking yang dipilih'
    
    def cancel_booking(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, '{} booking telah dibatalkan.'.format(updated))
    cancel_booking.short_description = 'Batalkan booking yang dipilih'