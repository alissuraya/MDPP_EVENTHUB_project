from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('booking_process/<int:idTempat>/', views.booking_process, name='booking_process'),
    path("staff_login/", views.staff_login, name="staff_login"),
    path('status/<str:noTempahan>/', views.status, name='status'),
    path('staff_manage_date/', views.staff_manage_date, name='staff_manage_date'),
    path('staff_history_booking/', views.staff_history_booking, name='staff_history_booking'),
    path('customer_receipt/<int:noTempahan>/', views.customer_receipt, name='customer_receipt'),
    path('maintain_tempat/', views.maintain_tempat, name='maintain_tempat'),
    path('available_date/<str:idTempat>/', views.available_date, name='available_date'),
    path('maintain_tempat/staff_delete_tempat/<int:idTempat>/', views.staff_delete_tempat, name='staff_delete_tempat'),
    path('staff_add_tempat/', views.staff_add_tempat, name='staff_add_tempat'),
    path('staff_update_tempat/<str:idTempat>/', views.staff_update_tempat, name='staff_update_tempat'),
    path('staff_update_tempat/save_update_tempat/<str:idTempat>/', views.save_update_tempat, name='save_update_tempat'),
    path('staff_delete_tempat/<str:idTempat>/', views.staff_delete_tempat, name='staff_delete_tempat'),
]