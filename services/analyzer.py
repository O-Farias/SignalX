def analyze_data(data):
    try:
        time_series = data["Time Series (5min)"]
        closing_prices = [float(v["4. close"]) for v in time_series.values()]
        
        # Regra simples: compra se o preço caiu muito, vende se subiu muito
        if closing_prices[0] < min(closing_prices[1:6]):
            return "📈 Sinal de Compra"
        elif closing_prices[0] > max(closing_prices[1:6]):
            return "📉 Sinal de Venda"
        else:
            return "⏸️ Sem ação recomendada"
    except Exception as e:
        return f"Erro na análise: {e}"
