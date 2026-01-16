from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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

@login_required
def booking(request, pk):
    kost = get_object_or_404(Kost, pk=pk)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, request.FILES)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.kost = kost
            booking.save()
            messages.success(request, 'Booking berhasil! Kami akan menghubungi Anda segera.')
            return redirect('booking_success', booking_id=booking.id)
    else:
        form = BookingForm()
    
    return render(request, 'booking.html', {'form': form, 'kost': kost})

def about(request):
    return render(request, 'about.html')

def gallery(request):
    kost_with_images = Kost.objects.filter(gambar__isnull=False).exclude(gambar='')
    context = {
        'kost_list': kost_with_images,
    }
    return render(request, 'gallery.html', context)

def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    context = {
        'booking': booking,
    }
    return render(request, 'booking_success.html', context)
