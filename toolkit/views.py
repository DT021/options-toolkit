from django.http import HttpResponse
from django.shortcuts import redirect
from toolkit import download_data

#   Most pages have their own py files; views are rendered by urls.py directly calling
#   functions in those files, without going through views.py. This file is for auxillary
#   and development/testing rendering only.

def index(request):
    return redirect("spreads_explorer/vertical_by_spread_width")

from json2html import json2html
def print_raw_data(request):
    options_data = download_data.get_options_data_raw({
        "symbol": "FSLY",
        "contractType": "PUT",
        "fromDate": "2020-11-30",
        "toDate": "2021-02-01"
    }).json()
    return HttpResponse(json2html.convert(json = options_data))