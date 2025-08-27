import time
import json
import requests
from flask import Flask, render_template
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

app = Flask(__name__)

# --- Cachés en memoria ---
cache_eth = {"data": None, "last_fetch": 0}
cache_noticias = {"data": None, "last_fetch": 0}

# --- Función para obtener datos de ETH ---
def fetch_eth_data():
    ahora = time.time()
    if cache_eth["data"] and ahora - cache_eth["last_fetch"] < 60:
        return cache_eth["data"]

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
        cache_eth["data"] = eth_info
        cache_eth["last_fetch"] = ahora
        return eth_info
    except requests.exceptions.HTTPError as e:
        if resp.status_code == 429:
            print("Demasiadas solicitudes a CoinGecko, usando último valor guardado")
            return cache_eth.get("data", {"precio": 0, "volumen_24h": 0, "market_cap": 0})
        else:
            raise e
    except Exception as e:
        print("Error al consultar CoinGecko:", e)
        return {"precio": 0, "volumen_24h": 0, "market_cap": 0}

# --- Función para obtener noticias ETH ---
def fetch_coindesk_eth():
    ahora = time.time()
    if cache_noticias["data"] and ahora - cache_noticias["last_fetch"] < 300:  # 5 min
        return cache_noticias["data"]

    url = "https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml"
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, "html.parser")
        items = soup.find_all("item")
        noticias = []

        for item in items:
            title = item.title.text
            link = item.link.text
            if "ETH" in title or "Ethereum" in title:
                try:
                    title_es = GoogleTranslator(source='en', target='es').translate(title)
                except Exception as e:
                    print("Error al traducir:", e)
                    title_es = title
                noticias.append({"titulo": title_es, "link": link})

        cache_noticias["data"] = noticias
        cache_noticias["last_fetch"] = ahora
        return noticias
    except Exception as e:
        print("Error al obtener noticias:", e)
        return cache_noticias.get("data", [])

# --- Ruta principal ---
@app.route("/")
def index():
    eth_data = fetch_eth_data()
    noticias = fetch_coindesk_eth()
    return render_template("index.html", eth_data=eth_data, noticias=noticias)

if __name__ == "__main__":
    app.run(debug=True)
