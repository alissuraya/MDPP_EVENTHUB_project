from django.db import models
from django.utils import timezone
from django.db.models import Max

class NonAvailableDate(models.Model):
    date = models.DateField(unique=True)

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d')}"

class NonAvailableTime(models.Model):
    time = models.CharField(max_length=100, unique=True, default='-')

    def __str__(self):
        return self.time

class Tempat(models.Model):
    idTempat = models.AutoField(primary_key=True)
    namaTempat = models.TextField(unique=True)
    cajSewaan_hari_siang = models.CharField(max_length=100)
    cajSewaan_jam_siang = models.CharField(max_length=100)
    cajSewaan_hari_malam = models.CharField(max_length=100)
    cajSewaan_jam_malam = models.CharField(max_length=100)
    non_available_dates_per_hari = models.ManyToManyField(NonAvailableDate, related_name='tempat_non_available_per_hari')
    non_available_dates_per_jam = models.ManyToManyField(NonAvailableDate, related_name='tempat_non_available_per_jam')
    non_available_times_per_jam = models.ManyToManyField(NonAvailableTime)

    def __str__(self):
        return self.namaTempat

class Tempahan(models.Model):
    noTempahan = models.IntegerField(unique=True, null=True, blank=True)
    tarikhTempahan = models.DateField(auto_now_add=True)
    namatempat = models.ForeignKey(Tempat, on_delete=models.CASCADE)
    selectedTime = models.ManyToManyField(NonAvailableTime, blank=True)
    jenis_sewaan_choices = [
        ('Per Hari', 'Sewaan Per Hari'),
        ('Per Jam', 'Sewaan Per Jam'),
    ]
    jenisSewaan = models.CharField(max_length=20, choices=jenis_sewaan_choices)
    slot_sewaan_choices = [
        ('Siang', 'Sewaan Slot Siang'),
        ('Malam', 'Sewaan Slot Malam'),
    ]
    slotSewaan = models.CharField(max_length=10, choices=slot_sewaan_choices)
    namaPenempah = models.TextField()
    noKP = models.CharField(max_length=14)
    noTelUtama = models.CharField(max_length=12)
    alamat = models.TextField()
    poskod = models.CharField(max_length=10, default='-')
    negeri = models.TextField(default='-')
    butiranBayaran = models.CharField(max_length=100, default='-')
    selectedDate = models.ManyToManyField(NonAvailableDate)  

    def save(self, *args, **kwargs):
        if self._state.adding and not self.noTempahan:
            max_no = Tempahan.objects.aggregate(Max('noTempahan'))['noTempahan__max']
            self.noTempahan = 1 if max_no is None else max_no + 1
        # Set a default value for jenisSewaan if it's not provided
        if not self.jenisSewaan:
            self.jenisSewaan = '-'  # You can set any default value you prefer here
        if not self.slotSewaan:
            self.slotSewaan = '-'
        # Set a default value for namaPelanggan if it's not provided
        if not self.namaPenempah:
            self.namaPenempah = '-'
        if not self.noKP:
            self.noKP = '-'
        if not self.noTelUtama:
            self.noTelUtama = '-'
        if not self.alamat:
            self.alamat = '-'
        if not self.poskod:
            self.poskod = '-'
        if not self.negeri:
            self.negeri = '-'
        super(Tempahan, self).save(*args, **kwargs)
        if self.selectedDate.exists():
            for date in self.selectedDate.all():
                self.selectedDate.add(date)
        if self.jenisSewaan == 'Per Hari':
            self.selectedTime.clear()  # Clear existing selectedTime
            self.selectedTime.add(NonAvailableTime.objects.get_or_create(time='-')[0])  # Add '-' as selectedTime

    def __str__(self):
        return f"Tempahan for {self.namatempat.namaTempat} on {self.tarikhTempahan}"

class Staff(models.Model):
    namaStaff = models.TextField()
    idStaff = models.CharField(max_length=12, primary_key=True)
    password = models.CharField(max_length=12)

    def __str__(self):
        return self.namaStaff