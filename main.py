from fastapi import FastAPI
import requests
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# FastAPI setup 
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Firebase setup
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# API KEY from fastFOREX
api_key = "8af0ed745d-545d45f398-rb7wfs"

@app.get("/currencies")
async def currencies():
    url = "https://api.fastforex.io/currencies?api_key={0}".format(api_key)
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = []
        for k, v in response.json()['currencies'].items():
            result.append({'code': k, 'name': v})
        return result
    return {}

@app.get("/latest")
async def latest(base: str | None = None):
    if base:
        url = "https://api.fastforex.io/fetch-all?from={0}&api_key={1}".format(base, api_key)
    else:
        url = "https://api.fastforex.io/fetch-all?api_key={0}".format(api_key)
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = []
        for k, v in response.json()['results'].items():
            result.append({'code': k, 'value': v})
        return result
    return {}

@app.get("/convert")
async def convert(amount : float, toCurrency: str, fromCurrency : str | None = None):
    if fromCurrency:
        url = "https://api.fastforex.io/convert?from={0}&to={1}&amount={2}&api_key={3}".format(fromCurrency, toCurrency, amount, api_key)
    else:
        url = "https://api.fastforex.io/convert?to={0}&amount={1}&api_key={2}".format(toCurrency, amount, api_key)
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        db.collection('history').add({
            'amount': amount,
            'conversion': response.json()['result'][toCurrency],
            'from': fromCurrency,
            'rate': response.json()['result']['rate'],
            'to': toCurrency
        })
        return response.json()
    return {}

@app.get("/statistics/history")
async def statisticsHistory():
    docs = db.collection('history').get()
    history = []
    for doc in docs:
        history.append(doc.to_dict())
    return history