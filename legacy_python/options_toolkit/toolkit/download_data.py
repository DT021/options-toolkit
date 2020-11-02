import requests, pandas
import toolkit.credentials as cred

resourceURL = "https://api.tdameritrade.com/v1/marketdata/chains"

def get_options_data_raw(params):
    params["apikey"] = cred.CLIENT_ID
    return requests.get(url = resourceURL, params = params)

### convert data to 
def get_options_data_pandas(params):
    return get_options_data_pandas_core(get_options_data_raw(params).json())

def get_options_data_raw_and_pandas(params):
    options_data = get_options_data_raw(params).json()
    return options_data, get_options_data_pandas_core(options_data)

def get_options_data_pandas_core(options_data):
    ### format data to pandas
    stock_price = float(options_data["underlyingPrice"])
    options_array = []
    for exp_date, prices in options_data["putExpDateMap"].items():
        bids_pandas = pandas.DataFrame(columns={ "Strike Price": float,"Bid": float })
        asks_pandas = pandas.DataFrame(columns={ "Strike Price": float,"Ask": float })
        for strike, value in prices.items():
            strike = float(strike)
            if strike > stock_price: continue
            bids_pandas = bids_pandas.append({
                "Strike Price": strike,
                "Bid": float(value[0]["bid"])
            }, ignore_index=True)
            asks_pandas = asks_pandas.append({
                "Strike Price": strike, 
                "Ask": float(value[0]["ask"])
            }, ignore_index=True)
        options_array.append({"Exp Date": exp_date, "Bids": bids_pandas, "Asks": asks_pandas})
    return options_array