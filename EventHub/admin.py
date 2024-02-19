from django.contrib import admin
from.models import NonAvailableDate,NonAvailableTime,Tempat,Tempahan,Staff

# Register your models here.
admin.site.register(NonAvailableDate)
admin.site.register(NonAvailableTime)
admin.site.register(Tempat)
admin.site.register(Tempahan)
admin.site.register(Staff)