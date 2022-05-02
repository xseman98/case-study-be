from fastapi import FastAPI
import requests
app = FastAPI()

@app.get("/currencies")
async def currencies():
    url = "https://api.fastforex.io/currencies?api_key=8af0ed745d-545d45f398-rb7wfs"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['currencies']
    return {}

@app.get("/latest")
async def latest(base: str | None = None):
    if base:
        url = "https://api.fastforex.io/fetch-all?from={0}&api_key=8af0ed745d-545d45f398-rb7wfs".format(base)
    else:
        url = "https://api.fastforex.io/fetch-all?api_key=8af0ed745d-545d45f398-rb7wfs"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['results']
    return {}

@app.get("/convert")
async def convert(amount : float, toCurrency: str, fromCurrency : str | None = None):
    if fromCurrency:
        url = "https://api.fastforex.io/convert?from={0}&to={1}&amount={2}&api_key=8af0ed745d-545d45f398-rb7wfs".format(fromCurrency, toCurrency, amount)
    else:
        url = "https://api.fastforex.io/convert?to={1}&amount={2}&api_key=8af0ed745d-545d45f398-rb7wfs".format(toCurrency, amount)
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return {}