import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import pytz

def fetch_market_data(symbol="AAPL", interval="5m"):
    """
    Busca dados de mercado usando a API do Yahoo Finance (yfinance).
    Ajusta os horários para o horário local do computador e verifica
    se os dados estão atualizados.

    Args:
        symbol (str): Símbolo do ativo (ex.: "AAPL" para Apple).
        interval (str): Intervalo de tempo entre os dados (ex.: "1m", "5m").
    
    Returns:
        pd.DataFrame: Dados de mercado organizados como DataFrame.
    """
    try:
        print(f"🔍 Buscando dados para {symbol} com intervalo de {interval}...")

        # Baixa os dados intraday do Yahoo Finance
        data = yf.download(tickers=symbol, period="1d", interval=interval)

        if data.empty:
            print("⚠️ Nenhum dado encontrado. Verifique o símbolo ou o intervalo.")
            return None

        # Renomeia as colunas para manter o padrão
        data.rename(columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        }, inplace=True)

        # Verifica se os horários já possuem timezone
        if data.index.tz is None:
            data.index = data.index.tz_localize("UTC")  # Adiciona timezone UTC
        data.index = data.index.tz_convert("America/Sao_Paulo")  # Converte para UTC-3

        print(f"🕒 Dados ajustados para o horário local (UTC-3):\n{data.head()}")

        # Remove timezone para exibição mais limpa (opcional)
        data.index = data.index.tz_localize(None)

        # Ordena os dados em ordem cronológica
        data = data.sort_index()

        # Verifica se o horário do último dado é recente
        last_data_time = data.index[-1]  # Horário do último dado
        current_time = datetime.now()  # Horário atual do sistema

        # Define um limite de 30 minutos para os dados estarem atualizados
        if current_time - last_data_time > timedelta(minutes=30):  # Alterado de 15 para 30 minutos
            print(f"⚠️ Os dados estão desatualizados! Último dado: {last_data_time}")
            return None  # Retorna None se os dados estiverem desatualizados
        else:
            print(f"✅ Dados atualizados! Último dado: {last_data_time}")

        return data
    except Exception as e:
        print(f"❌ Erro ao buscar dados: {e}")
        return None
