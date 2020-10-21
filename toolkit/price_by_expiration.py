import json, pandas, numpy, plotly, math, requests
import plotly.graph_objs as go
from django.http import JsonResponse
from django.template import loader

import toolkit as tk

def load_main_view(request):

    dd.get_options_data({
        "symbol": "FSLY",
        "contractType": "PUT"
    })

    for _, options_json in options_data.json()["putExpDateMap"].items():
        for _, value in options_json.items():
            if value[0]["strikePrice"] < 120 and value[0]["strikePrice"] > 30: #limit strike prices 
                bids_pandas = bids_pandas.append({
                    "Strike Price": float(value[0]["strikePrice"]),
                    "Bid": float(value[0]["bid"])
                }, ignore_index=True)
                asks_pandas = asks_pandas.append({
                    "Strike Price": float(value[0]["strikePrice"]), 
                    "Ask": float(value[0]["ask"])
                }, ignore_index=True)
        break
    


    return loader.get_template("prices_by_expirations.html").render({"whatever": "defined"})


    # https://plotly.com/python/time-series/