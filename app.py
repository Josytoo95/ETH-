from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from datetime import datetime
import json
import os

app = Flask(__name__)

KEYWORDS = ["ETH", "Ethereum"]
HIST_FILE = "historial.json"

# --- Obtener noticias de ETH ---
def fetch_coindesk_eth():
    url = "https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml"
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, "xml")  # sin necesidad de lxml
    items = soup.find_all("item")
    noticias = []

    for item in items:
        title = item.title.text
        description = item.description.text if item.description else ""
        if any(k.lower() in title.lower() for k in KEYWORDS):
            try:
                title_es = GoogleTranslator(source='en', target='es').translate(title)
                content_es = GoogleTranslator(source='en', target='es').translate(description)
            except:
                title_es = title
                content_es = description

            # Clasificar importancia
            titulo_lower = title_es.lower()
            if any(p in titulo_lower for p in ["hack", "crash", "regulation"]):
                importance = "alta"
            elif any(p in titulo_lower for p in ["upgrade", "merge", "adopcion"]):
                importance = "positiva"
            else:
                importance = "neutral"

            noticias.append({"title": title_es, "content": content_es, "importance": importance})

    return noticias

# --- Obtener liquidez de ETH ---
def fetch_eth_liquidity():
    url = "https://api.coingecko.com/api/v3/coins/ethereum"
    resp = requests.get(url, params={"localization": "false", "tickers": "false"})
    resp.raise_for_status()
    data = resp.json()
    md = data.get("market_data", {})
    total_volume = md.get("total_volume", {}).get("usd", 0)
    market_cap = md.get("market_cap", {}).get("usd", 0)
    price = md.get("current_price", {}).get("usd", 0)
    supply = md.get("circulating_supply", 0)
    last_updated = data.get("last_updated", "")

    # Guardar historial
    if os.path.exists(HIST_FILE):
        with open(HIST_FILE, "r") as f:
            historial = json.load(f)
    else:
        historial = {"fechas": [], "precios": [], "volumen": [], "market_cap": []}

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    historial["fechas"].append(now_str)
    historial["precios"].append(price)
    historial["volumen"].append(total_volume)
    historial["market_cap"].append(market_cap)

    # Mantener últimos 100 registros
    for key in historial:
        historial[key] = historial[key][-100:]

    with open(HIST_FILE, "w") as f:
        json.dump(historial, f)

    return {
        "price": price,
        "total_volume": total_volume,
        "market_cap": market_cap,
        "supply": supply,
        "last_updated": last_updated
    }

# --- Ruta principal ---
@app.route("/")
def index():
    noticias = fetch_coindesk_eth()
    eth = fetch_eth_liquidity()
    return render_template("index.html", news=noticias, eth=eth)

# --- Endpoint para historial (gráficos) ---
@app.route("/api/historial")
def historial_api():
    if os.path.exists(HIST_FILE):
        with open(HIST_FILE, "r") as f:
            historial = json.load(f)
    else:
        historial = {"fechas": [], "precios": [], "volumen": [], "market_cap": []}
    return jsonify(historial)

if __name__ == "__main__":
    app.run(debug=True)
