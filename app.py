# app.py

from news import ethereum_news

def generate_html():
    # --- Resumen fijo sobre Ethereum ---
    summary = """
    <div style="background-color:#111; padding:20px; border-radius:10px; margin-bottom:30px;">
        <h2 style="color:#1e90ff;">What is Ethereum?</h2>
        <p>Ethereum is an open-source, blockchain-based platform that allows developers to build
        decentralized applications (dApps) and smart contracts. It was proposed in 2013 by
        Vitalik Buterin and development began in early 2014. The Ethereum network went live
        on July 30, 2015, with 72 million pre-mined coins called Ether (ETH).</p>
        <p>Ethereum introduced the concept of smart contracts, which are self-executing
        contracts with the terms directly written into code. Over time, it has become the
        foundation for decentralized finance (DeFi), NFTs, and many other blockchain projects.</p>
    </div>
    """

    # --- Noticias debajo del resumen ---
    news_html = "<h2 style='color:#1e90ff; margin-top:40px;'>Latest ETH News – Updated Every Hour</h2>"
    news_html += "<div style='display:flex; flex-direction:column; gap:15px; margin-bottom:30px;'>"
    for n in ethereum_news:
        news_html += f"<div style='background-color:#222; padding:15px; border-radius:8px; box-shadow: 0 0 10px #000;'>{n}</div>"
    news_html += "</div>"

    # --- HTML completo ---
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

        <!-- InfoLinks Ads -->
        <script type="text/javascript">
            var infolinks_pid = 3439640; 
            var infolinks_wsid = 0;
        </script>
        <script type="text/javascript" src="//resources.infolinks.com/js/infolinks_main.js"></script>
    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

# ------------------------------
# Ejecutar todo
# ------------------------------
if __name__ == "__main__":
    generate_html()
    print("index.html generated successfully!")
