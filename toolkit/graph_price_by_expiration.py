import json, pandas, numpy, plotly, math, requests, re
import plotly.graph_objs as go
from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.shortcuts import render

from toolkit import download_data, utilities

def load_main_view(request):
    global options_array

    # download data
    if utilities.is_ajax(request):
        symbol = request.POST.get("symbol", None)
    else:
        symbol = None
    if symbol is None: symbol = "FSLY"

    _, options_array = download_data.get_options_data_raw_and_pandas({
        "symbol": symbol,
        "contractType": "PUT"
    })

    # the following code is bids only, for now
    all_strikes = set(options_array[0]["Bids"]["Strike Price"].unique())
    for i in range(1, len(options_array)):
        all_strikes = all_strikes.union(set(options_array[i]["Bids"]["Strike Price"].unique()))
    
    all_strikes = sorted(all_strikes, reverse=True)

    ### Output
    main_content = loader.get_template("graph_price_by_expiration.html").render({
        "all_strikes": all_strikes,
        "div_plot": graph(all_strikes)
    })

    if utilities.is_ajax(request):
         return HttpResponse(main_content)
    return render(request, "base.html", {
        "main_content": main_content
    })


def graph(strikes):
    global options_array
    fig = go.Figure()
    for strike in strikes:
        if int(strike*100) % 500 is not 0: continue
        array_dates = []
        array_prices = []
        for i in range(len(options_array)):
            x = options_array[i]["Bids"]
            y = x[x["Strike Price"] == strike]
            if y.shape[0] is not 0:
                array_dates.append(re.search(r"\d*-\d*-\d*", options_array[i]["Exp Date"]).group(0))
                array_prices.append(y.iloc[0]["Bid"])
        fig.add_trace(go.Scatter(x=array_dates, y=array_prices, mode='lines+markers', name=str(strike)))
    fig.layout["height"] = 1000
    return plotly.offline.plot(fig, output_type='div', include_plotlyjs=False)

        