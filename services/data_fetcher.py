import requests
import os
import pandas as pd
from datetime import datetime, timedelta
import pytz

def fetch_market_data(symbol="MSFT", interval="5min"):
    """
    Busca dados de mercado da API Alpha Vantage e retorna como um DataFrame,
    ajustando os horários para o horário local do computador e verificando
    se os dados estão atualizados.

    Args:
        symbol (str): Símbolo do ativo (ex.: "MSFT" para Microsoft).
        interval (str): Intervalo de tempo entre os dados (ex.: "5min").
    
    Returns:
        pd.DataFrame: Dados de mercado organizados como DataFrame.
    """
    api_key = os.getenv("API_KEY")
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={api_key}"

    try:
        # Faz a requisição para a API
        print(f"🔗 Enviando requisição para: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Verifica se os dados estão disponíveis
        if f"Time Series ({interval})" not in data:
            raise ValueError("⚠️ Dados não disponíveis ou limite de requisições excedido.")

        # Converte os dados para um DataFrame
        time_series = data[f"Time Series ({interval})"]
        df = pd.DataFrame.from_dict(time_series, orient="index", dtype=float)
        df.columns = ["open", "high", "low", "close", "volume"]

        # Ajusta os horários para datetime (UTC da API)
        df.index = pd.to_datetime(df.index).tz_localize("UTC")
        print(f"🕒 Dados recebidos em UTC:\n{df.head()}")

        # Ajusta os horários para o horário local do computador
        local_tz = pytz.timezone("America/Sao_Paulo")  # Fuso horário de Brasília
        df.index = df.index.tz_convert(local_tz)
        print(f"🕒 Dados ajustados para o horário local ({local_tz}):\n{df.head()}")

        # Remove informações de fuso (opcional)
        df.index = df.index.tz_localize(None)

        # Ordena os dados em ordem cronológica
        df = df.sort_index()

        # Verifica se o horário do último dado é recente
        last_data_time = df.index[-1]  # Horário do último dado
        current_time = datetime.now()  # Horário atual do sistema

        # Define um limite de 15 minutos para os dados estarem atualizados
        if current_time - last_data_time > timedelta(minutes=15):
            print(f"⚠️ Os dados estão desatualizados! Último dado: {last_data_time}")
            return None  # Retorna None se os dados estiverem desatualizados
        else:
            print(f"✅ Dados atualizados! Último dado: {last_data_time}")

        return df
    except requests.exceptions.RequestException as req_err:
        print(f"❌ Erro na requisição: {req_err}")
    except ValueError as val_err:
        print(f"⚠️ Erro nos dados recebidos: {val_err}")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

    return None
