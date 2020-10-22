import json, pandas, numpy, plotly, math, requests, re
import plotly.graph_objs as go
from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.shortcuts import render

from toolkit import download_data, utilities

def load_main_view(request):
    global options_array
    
    ### download data
    if utilities.is_ajax(request):
        symbol = request.POST.get("symbol", None)
    else:
        symbol = None
    if symbol is None: symbol = "FSLY"

    options_array = download_data.get_options_data_pandas({
        "symbol": symbol,
        "contractType": "PUT"
    })

    ### generate chains and plot
    div_chains = get_chains(0)

    ### output
    main_content = loader.get_template("SE_vertical_by_spread_width.html").render({
        "div_chains": div_chains,
        "symbol": symbol,
        "div_plot": get_plot()
    })

    if utilities.is_ajax(request):
         return HttpResponse(main_content)
    return render(request, "base.html", {
        "main_content": main_content
    })

### handle shift price ajax update
def update_shift_price(request):
    shift_price = int(request.GET.get('shift_price', None))
    div_chains = get_chains(shift_price)
    return JsonResponse({
        "div_chains": div_chains,
        "div_plot": get_plot()
    })

### print spread chains
def get_chains(shift_price):
    global options_array, plot_data, fig
    
    ### initialize plot
    plot_data = {}
    fig = go.Figure()

    output_chains = ""
    for options_item in options_array:
        output_chains += "<div>Expiration Date: " + options_item["Exp Date"] + "<br>" \
            + get_chain(options_item["Exp Date"], options_item["Bids"], options_item["Asks"], shift_price) + "</div>"
    return output_chains

### print spread chain unit
def get_chain(exp_date, bids_pandas, asks_pandas, shift_price):
    global plot_data

    asks_pandas_shifted = pandas.DataFrame(columns={
        "Strike Price": float,
        "Ask": float,
        "Ask Original Strike": float
    })
    asks_pandas_shifted = asks_pandas.copy()
    asks_pandas_shifted["Ask Original Strike"] = asks_pandas_shifted["Strike Price"]
    if shift_price is not 0: asks_pandas_shifted["Strike Price"] += float(shift_price)

    combined_pandas = asks_pandas_shifted.join(bids_pandas.set_index("Strike Price"), on="Strike Price", how="outer")
    combined_pandas.sort_values(by=["Strike Price"], ascending=False, inplace=True)
    
    ### Generate Chains
    ### TODO: replace the following section with Django HTML template
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

            ### Store data for plot
            ### 1. find whether the spread is already there.
            spread_name = float_to_html(row["Strike Price"]) + "/" + float_to_html(row["Ask Original Strike"])
            x = plot_data.get(spread_name)
            if x is None:
                plot_data[spread_name] = {
                    "Exp Date": [re.search(r"\d*-\d*-\d*", exp_date).group(0)],
                    "ROI": [spread_diff]
                }
            else:
                plot_data[spread_name]["Exp Date"].append(re.search(r"\d*-\d*-\d*", exp_date).group(0))
                plot_data[spread_name]["ROI"].append(spread_diff)

    return str_chain + "</tbody></table>"

def get_plot():
    global fig, plot_data
    for strike, data in plot_data.items():
        fig.add_trace(go.Scatter(x=data["Exp Date"], y=data["ROI"],
                     mode='lines+markers', name=strike))
    fig.layout["height"] = 1000
    return plotly.offline.plot(fig, output_type='div', include_plotlyjs=False)

def float_to_html (data):
    if math.isnan(data):
        return ""
    return "{:.2f}".format(data)