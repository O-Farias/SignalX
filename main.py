import os
from dotenv import load_dotenv
from services.data_fetcher import fetch_market_data
from services.analyzer import analyze_data

# Carrega as variáveis de ambiente
load_dotenv()

def main():
    print("🚀 Bem-vindo ao SignalX!")
    print("🔍 Configurando análise...")

    # Ativo e intervalo configuráveis
    symbol = "MSFT"  
    interval = "5min"  

    print(f"🔍 Buscando dados para {symbol} com intervalo de {interval}...")
    data = fetch_market_data(symbol=symbol, interval=interval)

    if data is not None:
        print("📊 Dados recebidos com sucesso!")
        print(data.head())  # Mostra as 5 primeiras linhas para validação

        # Aplicando a análise
        print("📈 Aplicando estratégias de análise...")
        result = analyze_data(data)

        # Mostra o resultado consolidado
        print("📊 Resultado da análise:")
        for strategy, signal in result.items():
            print(f"{strategy}: {signal}")
    else:
        print("❌ Falha ao buscar dados. Por favor, verifique sua API Key e conexão.")

if __name__ == "__main__":
    main()
