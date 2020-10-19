import requests
import toolkit.credentials as cred

resourceURL = "https://api.tdameritrade.com/v1/marketdata/chains"

def get_options_data(params):
    params["apikey"] = cred.CLIENT_ID
    return requests.get(url = resourceURL, params = params)
    
