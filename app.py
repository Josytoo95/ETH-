from news import ethereum_news

def generate_html():
    # --- Bloque educativo fijo sobre Ethereum ---
    summary = """
    <div style="background-color:#111; padding:20px; border-radius:10px; margin-bottom:30px;">
        <h2 style="color:#1e90ff;">What is Ethereum?</h2>
        <p>Ethereum is a decentralized blockchain platform that allows developers to build and deploy smart contracts and decentralized applications (dApps). 
        Unlike Bitcoin, which was created primarily as a digital currency, Ethereum's goal is to provide a global platform for programmable finance and applications.</p>

        <p>Ethereum was proposed in late 2013 by Vitalik Buterin, a cryptocurrency researcher and programmer. The network went live on July 30, 2015, 
        with 72 million pre-mined Ether (ETH) as part of its initial distribution.</p>

        <p>Smart contracts are self-executing contracts with the terms of the agreement directly written into code. 
        Ethereum’s blockchain enables these smart contracts to run exactly as programmed without any possibility of downtime, fraud, or third-party interference.</p>

        <p>Ether (ETH) is the native cryptocurrency of Ethereum and is used to pay for transaction fees and computational services on the network. 
        Over the years, Ethereum has evolved into the foundation of the decentralized finance (DeFi) ecosystem, NFTs, DAOs, and numerous other applications.</p>

        <p>Ethereum continues to grow and innovate, with major upgrades like Ethereum 2.0 (also known as The Merge), 
        which transitioned the network from proof-of-work (PoW) to proof-of-stake (PoS), improving energy efficiency and scalability.</p>

        <p>Overall, Ethereum represents not just a cryptocurrency, but a whole ecosystem that empowers developers and users to create, trade, and interact with decentralized applications globally.</p>
    </div>
    """

    # --- Noticias dinámicas ---
    news_html = "<h2 style='color:#1e90ff; margin-top:40px;'>Latest Ethereum News</h2>"
    news_html += "<div style='display:flex; flex-direction:column; gap:15px; margin-bottom:30px;'>"
    for n in ethereum_news:
        news_html += f"<div style='background-color:#222; padding:15px; border-radius:8px; box-shadow: 0 0 10px #000;'>{n}</div>"
    news_html += "</div>"

    # --- Bloque de publicidad opcional ---
    ads_html = """
    <div style="margin-top: 40px; padding: 25px; background-color: #222; color: white; text-align:center; border-radius:10px; box-shadow:0 0 15px #000;">
        <p style="font-size:18px;"><strong>Advertisement</strong></p>
        <p>Your ad could be here!</p>
    </div>
    """

    # --- HTML completo con Google Analytics ---
    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Ethereum Weekly</title>
        <!-- Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-DK3VT62F2Y"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());

          gtag('config', 'G-DK3VT62F2Y');
        </script>
    </head>
    <body style="font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #000, #111); color: white;">
        <h1 style="color:#1e90ff; margin-bottom:30px;">Ethereum Weekly</h1>
        {summary}
        {news_html}
        {ads_html}
    </body>
    </html>
    """

    # --- Guardar archivo HTML ---
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

# ------------------------------
# Ejecutar todo
# ------------------------------
if __name__ == "__main__":
    generate_html()
    print("index.html generated successfully!")

