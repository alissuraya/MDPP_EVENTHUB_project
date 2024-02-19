from django.shortcuts import render
from.models import NonAvailableDate,Tempat,Tempahan,Staff
from .models import NonAvailableTime
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Max
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import ValidationError
import json

# Create your views here.

def index(request):
    tempat_list = Tempat.objects.all()

    return render(request, 'index.html', {'tempat_list': tempat_list})

def booking_process(request, idTempat):
    tempat = get_object_or_404(Tempat, idTempat=idTempat)
    
    # Get non-available dates and times for both types of bookings
    non_available_dates_per_hari = [date.date.strftime('%Y-%m-%d') for date in tempat.non_available_dates_per_hari.all()]
    non_available_dates_per_jam = [date.date.strftime('%Y-%m-%d') for date in tempat.non_available_dates_per_jam.all()]
    non_available_times_per_jam = [time.time for time in tempat.non_available_times_per_jam.all()]

    form_submitted = False  # Flag to indicate if form has been submitted
    selectedDate = ""  # Initialize selectedDate
    selectedTime = ""  # Initialize selectedTime

    if request.method == 'POST':
        # Extract form data from the request
        namaPenempah = request.POST.get('namaPenempah')
        noKP = request.POST.get('noKP')
        noTelUtama = request.POST.get('noTelUtama')
        alamat = request.POST.get('alamat')
        poskod = request.POST.get('poskod')
        negeri = request.POST.get('negeri')
        selectedDate_json = request.POST.get('selectedDate')  # Get the JSON string
        selectedDate = json.loads(selectedDate_json) if selectedDate_json else ""  # Convert JSON to Python list
        slotSewaan = request.POST.get('slotSewaan')
        selectedTime = request.POST.get('selectedTime')
        jenisSewaan = request.POST.get('jenisSewaan')

        # Set selectedTime to '-' if jenisSewaan is "Per Hari"
        if jenisSewaan == 'Per Hari':
            selectedTime = '-'
            
        tempahan = Tempahan(
            namatempat=tempat,
            namaPenempah=namaPenempah,
            noKP=noKP,
            noTelUtama=noTelUtama,
            alamat=alamat,
            poskod=poskod,
            negeri=negeri,
            slotSewaan=slotSewaan,
            jenisSewaan=jenisSewaan,
        )
        tempahan.save()

        # Save selected dates as NonAvailableDate objects based on jenisSewaan
        if jenisSewaan == 'Per Hari':
            for date_str in selectedDate:
                date_obj, created = NonAvailableDate.objects.get_or_create(date=date_str)
                tempahan.selectedDate.add(date_obj)  # Add the date object to the ManyToManyField
                
                # Update non_available_dates_per_hari if needed
                if date_str not in non_available_dates_per_hari:
                    non_available_dates_per_hari.append(date_str)
        elif jenisSewaan == 'Per Jam' and selectedTime:
            for date_str in selectedDate:
                date_obj, created = NonAvailableDate.objects.get_or_create(date=date_str)
                tempahan.selectedDate.add(date_obj)  # Add the date object to the ManyToManyField
                
                # Update non_available_dates_per_jam if needed
                if date_str not in non_available_dates_per_jam:
                    non_available_dates_per_jam.append(date_str)
            
            # Save selected times as NonAvailableTime objects
            selected_times = selectedTime.split(',')
            for time_str in selected_times:
                time_obj, created = NonAvailableTime.objects.get_or_create(time=time_str)
                tempahan.selectedTime.add(time_obj)  # Add the time object to the ManyToManyField
                
                # Update non_available_times_per_jam if needed
                if time_str not in non_available_times_per_jam:
                    non_available_times_per_jam.append(time_str)

        form_submitted = True  # Set the flag to indicate form submission

        # Redirect to a success page or another URL
        return redirect('staff_history_booking')

    context = {
        'tempat': tempat,
        'non_available_dates_per_hari': non_available_dates_per_hari,
        'non_available_dates_per_jam': non_available_dates_per_jam,
        'non_available_times_per_jam': non_available_times_per_jam,
        'form_submitted': form_submitted,  # Pass the form submission flag to the template
        'selectedDate': selectedDate,  # Pass selectedDate to the template
        'selectedTime': selectedTime,  # Pass selectedTime to the template
    }

    return render(request, "booking_process.html", context)

def calculate_rental_duration(tempahan):
    jenisSewaan = tempahan.jenisSewaan
    if jenisSewaan == 'Per Hari':
        durasiSewaan = tempahan.selectedDate.count()
    elif jenisSewaan == 'Per Jam':
        durasiSewaan = tempahan.selectedTime.count()   # Count the number of elements directly
    else:
        durasiSewaan = 0  # Default value if neither Per Hari nor Per Jam
    return durasiSewaan

def calculate_rental_fee(tempahan):
    jenisSewaan = tempahan.jenisSewaan
    slotSewaan = tempahan.slotSewaan
    cajSewaan = 0  # Default value
    if jenisSewaan == 'Per Hari':
        cajSewaan = float(tempahan.namatempat.cajSewaan_hari_siang) * tempahan.selectedDate.count()
    elif jenisSewaan == 'Per Jam':
        if slotSewaan == 'Siang':
            cajSewaan = float(tempahan.namatempat.cajSewaan_jam_siang) * (tempahan.selectedTime.count() + 1)  # Remove the argument ',' from count()
        elif slotSewaan == 'Malam':
            cajSewaan = float(tempahan.namatempat.cajSewaan_jam_malam) * (tempahan.selectedTime.count() + 1)  # Remove the argument ',' from count()
    return cajSewaan

def customer_receipt(request, noTempahan):
    tempahan = get_object_or_404(Tempahan, noTempahan=noTempahan)

    durasiSewaan = calculate_rental_duration(tempahan)
    cajSewaan = calculate_rental_fee(tempahan)

    selected_date_list = tempahan.selectedDate.all()
    selected_time_list = tempahan.selectedTime.all()

    context = {
        'tempahan': tempahan,
        'durasiSewaan': durasiSewaan,
        'cajSewaan': cajSewaan,
        'selected_time_list': selected_time_list,
        'selected_date_list': selected_date_list,
    }

    return render(request, "customer_receipt.html", context)

def staff_login(request):
    allstaff = Staff.objects.all()
    if request.method =='POST':
        idStaff = request.POST.get("idStaff")  
        password = request.POST.get("password")
        
        try:
            data = Staff.objects.get(idStaff=idStaff)
        except Staff.DoesNotExist:
            dict = {
                'message' : 'Ralat! Kata Nama Salah'
            }
            return render (request, "staff_login.html", dict)
        if password != data.password:
            dict = {
                'message' : 'Ralat! Kata Laluan Salah'
            }
            return render(request, "staff_login.html", dict)
        else:
            return HttpResponseRedirect(reverse('index'))

    else:
        return render (request, "staff_login.html")

def status(request, noTempahan):
    if request.method == 'POST':
        data3 = Tempahan.objects.get(noTempahan=noTempahan)
        allbooking = Tempahan.objects.all()

        data3.butiranBayaran = request.POST.get('status')
        data3.save()

        return redirect('staff_history_booking')  # Redirect back to the staff_history_booking view

    # Handle GET requests appropriately if needed
    return redirect('staff_history_booking')

def staff_history_booking(request):
    allbookings = Tempahan.objects.all()
    search_query = request.GET.get('Carian')

    if search_query:
        # Perform the search by noTempahan
        data = Tempahan.objects.filter(noTempahan__icontains=search_query)
    else:
        data = allbookings

    for booking in data:
        booking.durasiSewaan = calculate_rental_duration(booking)
        booking.cajSewaan = calculate_rental_fee(booking)
        booking.selectedTime_list = booking.selectedTime.all()  # Fetch related time objects
        booking.selectedDate_list = booking.selectedDate.all()  # Fetch related date objects

    context = {'allbookings': allbookings, 'data': data, 'search_query': search_query}
    return render(request, 'staff_history_booking.html', context)

def staff_manage_date(request):
    # Retrieve all unique namaTempat values from the Tempat model
    allbookings = Tempat.objects.all()

    search_query = request.GET.get('Carian')

    if search_query:
        data = Tempahan.objects.filter(namatempat__namaTempat__icontains=search_query)
    else:
        data = Tempahan.objects.all()

    for booking in data:
        booking.durasiSewaan = calculate_rental_duration(booking)
        booking.cajSewaan = calculate_rental_fee(booking)
        booking.selectedTime_list = booking.selectedTime.all()  # Fetch related time objects
        booking.selectedDate_list = booking.selectedDate.all()  # Fetch related date objects

    context = {'allbookings': allbookings, 'data': data, 'search_query': search_query}
    return render(request, 'staff_manage_date.html', context)

def maintain_tempat(request):
    query = request.GET.get('Carian')  # Retrieve the search query

    if query:
        # Split the query into words for a broader search
        query_words = query.split()
        q_objects = Q()

        # Create a query that looks for each word in the 'namaTempat' field
        for word in query_words:
            q_objects |= Q(namaTempat__icontains=word)

        # Filter Tempat objects based on the constructed query
        tempat_list = Tempat.objects.filter(q_objects)
    else:
        # If no query is present, retrieve all Tempat objects
        tempat_list = Tempat.objects.all()

    context = {
        'tempat_list': tempat_list,
    }

    return render(request, "maintain_tempat.html", context)

def available_date(request, idTempat):
    tempat = get_object_or_404(Tempat, idTempat=idTempat)

    context = {
        'tempat': tempat
    }

    return render(request, "available_date.html",context)

def staff_delete_tempat(request, idTempat):
    # Check if the request method is POST
    if request.method == "POST":
        # Try to retrieve the Tempat object and delete it
        try:
            tempat = Tempat.objects.get(pk=idTempat)
            tempat.delete()
            # Redirect to the maintain_tempat view after deletion
            return redirect('maintain_tempat')
        except Tempat.DoesNotExist:
            # Handle the case where the Tempat does not exist
            pass # Or handle appropriately

    # Redirect to the maintain_tempat view if not a POST request or if deletion fails
    return redirect('maintain_tempat')

def staff_add_tempat(request):
    msg = ''
    if request.method == 'POST':
        namaTempat = request.POST.get('namaTempat')
        cajSewaan_hari_siang = request.POST.get('cajSewaan_hari_siang')
        cajSewaan_hari_malam = request.POST.get('cajSewaan_hari_malam')
        cajSewaan_jam_siang = request.POST.get('cajSewaan_jam_siang')
        cajSewaan_jam_malam = request.POST.get('cajSewaan_jam_malam')

        # Change this line to use __iexact for case-insensitive match
        if Tempat.objects.filter(namaTempat__iexact=namaTempat).exists():
            msg = 'Tempat dengan nama ini sudah ada dalam sistem'
        else:
            Tempat.objects.create(
                namaTempat=namaTempat,
                cajSewaan_hari_siang=cajSewaan_hari_siang,
                cajSewaan_hari_malam=cajSewaan_hari_malam,
                cajSewaan_jam_siang=cajSewaan_jam_siang,
                cajSewaan_jam_malam=cajSewaan_jam_malam
            )
            return redirect('maintain_tempat')

    return render(request, "staff_add_tempat.html", {'msg': msg})

def staff_update_tempat(request,idTempat):
    data = Tempat.objects.get(idTempat=idTempat)

    context = {
        'tempat': data,
    }

    return render(request, "staff_update_tempat.html", context)

def save_update_tempat(request, idTempat):
    data = Tempat.objects.get(idTempat=idTempat)

    if request.method == 'POST':
        namaTempat = request.POST['namaTempat']
        cajSewaan_hari_siang = request.POST['cajSewaan_hari_siang']
        cajSewaan_hari_malam = request.POST['cajSewaan_hari_malam']
        cajSewaan_jam_siang = request.POST['cajSewaan_jam_siang']
        cajSewaan_jam_malam = request.POST['cajSewaan_jam_malam']

        # Update tempat information
        data.namaTempat = namaTempat
        data.cajSewaan_hari_siang = cajSewaan_hari_siang
        data.cajSewaan_hari_malam = cajSewaan_hari_malam
        data.cajSewaan_jam_siang = cajSewaan_jam_siang
        data.cajSewaan_jam_malam = cajSewaan_jam_malam

        # Save the updated tempat
        data.save()

    return HttpResponseRedirect(reverse("maintain_tempat"))

def staff_delete_tempat(request, idTempat):
    if request.method == 'POST':
        try:
            tempat = Tempat.objects.get(idTempat=idTempat)
            tempat.delete()
        except Tempat.DoesNotExist:
            pass  # Handle if the tempat doesn't exist (optional)
    return redirect('maintain_tempat')