from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    
    path("spreads_discovery/", views.spreads_discovery),
    path("spreads_discovery/sd_update_shift_price/", views.sd_update_shift_price),
    
    path("prices_by_expirations/", views.prices_by_expirations),

    path("print_raw_data/", views.print_raw_data)
]
