import time
import json
import requests
from flask import Flask, render_template
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import os

app = Flask(__name__)

# --- Archivos locales ---
HISTORIAL_FILE = "historial.json"
NOTICIAS_FILE = "noticias.json"

# --- Función para consultar CoinGecko con caché ---
def fetch_eth_data():
    """Devuelve el precio, volumen y market cap de ETH usando caché de 1 min."""
    if os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
            historial = json.load(f)
    else:
        historial = {}

    ahora = time.time()
    # Si el último fetch fue hace menos de 60s, devuelve cache
    if "last_fetch" in historial and ahora - historial["last_fetch"] < 60:
        return historial["data"]

    url = "https://api.coingecko.com/api/v3/coins/ethereum?localization=false&tickers=false"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        eth_info = {
            "precio": data["market_data"]["current_price"]["usd"],
            "volumen_24h": data["market_data"]["total_volume"]["usd"],
            "market_cap": data["market_data"]["market_cap"]["usd"]
        }
        # Guardar en cache
        historial["last_fetch"] = ahora
        historial["data"] = eth_info
        with open(HISTORIAL_FILE, "w", encoding="utf-8") as f:
            json.dump(historial, f, ensure_ascii=False, indent=2)
        return eth_info
    except requests.exceptions.HTTPError as e:
        if resp.status_code == 429:
            print("Demasiadas solicitudes a CoinGecko, usando último valor guardado")
            return historial.get("data", {"precio":0,"volumen_24h":0,"market_cap":0})
        else:
            raise e

# --- Función para obtener noticias ETH desde Coindesk ---
def fetch_coindesk_eth():
    url = "https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")
    items = soup.find_all("item")
    noticias = []

    for item in items:
        title = item.title.text
        link = item.link.text
        if "ETH" in title or "Ethereum" in title:
            # Traducir a español
            title_es = GoogleTranslator(source='en', target='es').translate(title)
            noticias.append({"titulo": title_es, "link": link})

    # Guardar noticias en archivo
    with open(NOTICIAS_FILE, "w", encoding="utf-8") as f:
        json.dump(noticias, f, ensure_ascii=False, indent=2)

    return noticias

# --- Ruta principal ---
@app.route("/")
def index():
    eth_data = fetch_eth_data()
    noticias = fetch_coindesk_eth()
    return render_template("index.html", eth_data=eth_data, noticias=noticias)

if __name__ == "__main__":
    app.run(debug=True)
