import json, pandas, numpy, plotly, math, requests
import plotly.graph_objs as go
from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.shortcuts import render

import toolkit.download_data as dd
import toolkit.utilities as utils

def spreads_discovery(request):
    global options_array
    
    # download data
    if utils.is_ajax(request):
        symbol = request.POST.get("symbol", None)
    else:
        symbol = None
    if symbol is None: symbol = "FSLY"

    options_data = dd.get_options_data({
        "symbol": symbol,
        "contractType": "PUT"
    }).json()

    # format data to pandas
    current_price = float(options_data["underlyingPrice"])
    options_array = []
    for exp_date, prices in options_data["putExpDateMap"].items():
        bids_pandas = pandas.DataFrame(columns={ "Strike Price": float,"Bid": float })
        asks_pandas = pandas.DataFrame(columns={ "Strike Price": float,"Ask": float })
        for _, value in prices.items():
            # price filter criteria 
            if value[0]["strikePrice"] < current_price * 0.9 and value[0]["strikePrice"] > current_price * 0.3: 
                bids_pandas = bids_pandas.append({
                    "Strike Price": float(value[0]["strikePrice"]),
                    "Bid": float(value[0]["bid"])
                }, ignore_index=True)
                asks_pandas = asks_pandas.append({
                    "Strike Price": float(value[0]["strikePrice"]), 
                    "Ask": float(value[0]["ask"])
                }, ignore_index=True)
        options_array.append({"Exp Date": exp_date, "Bids": bids_pandas, "Asks": asks_pandas})

    # Output
    main_content = loader.get_template("spreads_discovery.html").render({"div_chains": get_chains(0), "symbol": symbol})

    if utils.is_ajax(request):
         return HttpResponse(main_content)
    return render(request, "base.html", {
        "main_content": main_content
    })

"""
def get_plot():
    global bids_pandas, asks_pandas, asks_pandas_shifted
    div_plot = get_options_plotly_div(
                    bids_pandas.transpose().to_dict('split')["data"],
                    asks_pandas_shifted.transpose().to_dict("split")["data"])
    return div_plot
"""

def update_shift_price(request):
    shift_price = int(request.GET.get('shift_price', None))
    return JsonResponse({
        "div_chains": get_chains(shift_price)
    })

def get_chains(shift_price):
    global options_array
    output_chains = ""
    for options_item in options_array:
        output_chains += "<div>Expiration Date: " + options_item["Exp Date"] + "<br>" \
            + get_chain(options_item["Bids"], options_item["Asks"], shift_price) + "</div>"
    return output_chains

def get_chain(bids_pandas, asks_pandas, shift_price):
    asks_pandas_shifted = pandas.DataFrame(columns={
        "Strike Price": float,
        "Ask": float,
        "Ask Original Strike": float
    })
    asks_pandas_shifted = asks_pandas.copy()
    asks_pandas_shifted["Ask Original Strike"] = asks_pandas_shifted["Strike Price"]
    if shift_price is not 0: asks_pandas_shifted["Strike Price"] += float(shift_price)

    str_chain = """
        <table>
            <thead>
                <tr>
                    <th>Short Strike</th>
                    <th>Bid</th>
                    <th>""" + "ROI" + """</th>
                    <th>Ask</th>
                    <th>Long Strike</th>
                </tr>
            </thead>
            <tbody>"""
    combined_pandas = bids_pandas.join(asks_pandas_shifted.set_index("Strike Price"), on="Strike Price", how="outer")
    combined_pandas.sort_values(by=["Strike Price"], ascending=False, inplace=True)
    
    for _, row in combined_pandas.iterrows():
        spread_diff = row["Bid"] - row["Ask"]

        if spread_diff > 0:
            bghsl = "'background-color:hsl(" + str(int(spread_diff/float(shift_price)*350)) + ", 60%, " + format(1-spread_diff/float(shift_price)*0.6, '2.0%') + ");'"
            str_chain += "<tr style=" + bghsl + " temp_style=" + bghsl + "> \
                <td class='bid_cell bid_cell_" + str(int(row["Strike Price"]*100)) + "'>" + float_to_html(row["Strike Price"]) + "</td> \
                <td>" + float_to_html(row["Bid"]) + "</td> \
                <td>" + (format(spread_diff/float(shift_price), '2.0%') if spread_diff > 0 else "") + "</td> \
                <td>" + float_to_html(row["Ask"]) + "</td> \
                <td>" + float_to_html(row["Ask Original Strike"]) + "</td> \
            </tr>"
    return str_chain + "</tbody></table>"

"""
def get_options_plotly_div(bids_array, asks_array):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=bids_array[0], y=bids_array[1],
                     mode='lines', name='Bid',
                     opacity=1, marker_color='red'))
    fig.add_trace(go.Scatter(x=asks_array[0], y=asks_array[1],
                     mode='lines', name='Ask',
                     opacity=1, marker_color='blue'))
    fig.layout["height"] = 780
    return plotly.offline.plot(fig, output_type='div', include_plotlyjs=False);
"""

def float_to_html (data):
    if math.isnan(data):
        return ""
    return "{:.2f}".format(data)