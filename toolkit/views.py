from django.shortcuts import redirect

import toolkit.spreads_discovery as sd
import toolkit.prices_by_expirations as pe
import toolkit.utilities as utils

def index(request):
    return redirect("spreads_discovery/")

def spreads_discovery(request):
    return sd.spreads_discovery(request)

def sd_update_shift_price(request):
    return sd.update_shift_price(request)

def prices_by_expirations(request):
    return pe.prices_by_expirations(request)



import toolkit.download_data as dd
from django.http import HttpResponse
from json2html import *

def print_raw_data(request):
    options_data = dd.get_options_data({
        "symbol": "FSLY",
        "contractType": "PUT",
        "fromDate": "2020-11-30",
        "toDate": "2021-02-01"
    }).json()
    return HttpResponse(json2html.convert(json = options_data))