from django.urls import path
from . import views

from toolkit import SE_vertical_by_spread_width, SE_vertical_by_one_leg, graph_price_by_expiration

urlpatterns = [
    path("", views.index, name="index"),
    path("spreads_explorer/vertical_by_spread_width/", SE_vertical_by_spread_width.load_main_view),
    path("spreads_explorer/vertical_by_spread_width/update_shift_price/", SE_vertical_by_spread_width.update_shift_price),
    path("spreads_explorer/vertical_by_one_leg/", SE_vertical_by_one_leg.load_main_view),
    path("graph_price_by_expiration/", graph_price_by_expiration.load_main_view),
    path("print_raw_data/", views.print_raw_data)
]