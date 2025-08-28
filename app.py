from news import ethereum_news
from datetime import datetime, timedelta
import plotly.express as px

def generate_html():
    # --- Resumen semanal ---
    summary = """
    <div style="background-color:#111; padding:20px; border-radius:10px; margin-bottom:30px;">
        <h2 style="color:#1e90ff;">Ethereum Weekly Summary</h2>
        <p>This week, the price of ETH started at <strong>$4335.10</strong> and ended at <strong>$4517.32</strong>, 
        increasing by <strong>4.20%</strong> over the week.</p>
    </div>
    """

    # --- Gráfico de precios ---
    days = [(datetime.today() - timedelta(days=i)).strftime("%d-%m") for i in range(6, -1, -1)]
    prices = [4335, 4380, 4420, 4450, 4490, 4520, 4517]
    fig = px.line(x=days, y=prices, title="ETH Price (Last 7 Days)", labels={'x': 'Day', 'y': 'Price (USD)'})
    fig.update_layout(
        plot_bgcolor='#111', paper_bgcolor='#111', font_color='white',
        title_font_size=20, xaxis=dict(gridcolor='#333'), yaxis=dict(gridcolor='#333')
    )
    chart_html = fig.to_html(full_html=False)

    # --- Noticias debajo del gráfico ---
    news_html = "<h2 style='color:#1e90ff; margin-top:40px;'>Top Ethereum News (Last 7 Days)</h2>"
    news_html += "<div style='display:flex; flex-direction:column; gap:15px; margin-bottom:30px;'>"
    for n in ethereum_news:
        news_html += f"<div style='background-color:#222; padding:15px; border-radius:8px; box-shadow: 0 0 10px #000;'>{n}</div>"
    news_html += "</div>"

    # --- Bloque de publicidad ---
    ads_html = """
    <div style="margin-top: 40px; padding: 25px; background-color: #222; color: white; text-align:center; border-radius:10px; box-shadow:0 0 15px #000;">
        <p style="font-size:18px;"><strong>Advertisement</strong></p>
        <p>Your ad could be here!</p>
    </div>
    """

    # --- HTML completo ---
    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Ethereum Weekly</title>
    </head>
    <body style="font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #000, #111); color: white;">
        <h1 style="color:#1e90ff; margin-bottom:30px;">Ethereum Weekly</h1>
        {summary}
        <h2 style="color:#1e90ff;">Price Evolution</h2>
        {chart_html}
        {news_html}
        {ads_html}
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
