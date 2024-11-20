import os
from dotenv import load_dotenv
from services.data_fetcher import fetch_market_data
from services.analyzer import analyze_data


load_dotenv()

def main():
    print("🚀 Bem-vindo ao SignalX!")
    print("🔍 Buscando dados do mercado...")
    data = fetch_market_data()
    if data:
        
        result = analyze_data(data)
        print("📊 Resultado da análise:")
        print(result)
    else:
        print("❌ Falha ao buscar dados.")

if __name__ == "__main__":
    main()
