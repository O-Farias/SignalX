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

        # Validação de intervalos suportados
        valid_intervals = ["1m", "2m", "5m", "15m", "30m", "1h", "1d"]
        if interval not in valid_intervals:
            print(f"⚠️ Intervalo {interval} não suportado! Use um dos seguintes: {valid_intervals}")
            return None

        # Ajuste do período para ativos diferentes
        period = "1d" if interval in ["1m", "2m", "5m", "15m", "30m"] else "7d"

        # Baixa os dados do Yahoo Finance
        data = yf.download(tickers=symbol, period=period, interval=interval)

        if data.empty:
            print(f"⚠️ Nenhum dado encontrado para {symbol} com intervalo {interval}.")
            return None

        # Renomeia as colunas para manter o padrão
        data.rename(columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        }, inplace=True)

        # Ajusta os horários do DataFrame para UTC-3
        if data.index.tz is None:
            data.index = data.index.tz_localize("UTC")  # Adiciona timezone UTC
        data.index = data.index.tz_convert("America/Sao_Paulo")  # Converte para UTC-3

        # Força todos os horários no DataFrame para serem tz-naive (sem timezone)
        data.index = data.index.tz_localize(None)

        print(f"🕒 Dados ajustados para o horário local (UTC-3):\n{data.head()}")

        # Ordena os dados em ordem cronológica
        data = data.sort_index()

        # Captura o horário atual no fuso correto e remove a timezone (tz-naive)
        local_tz = pytz.timezone("America/Sao_Paulo")
        current_time = datetime.now(local_tz).replace(tzinfo=None)

        # Verifica se o horário do último dado é recente
        last_data_time = data.index[-1]  # Horário do último dado
        time_difference = current_time - last_data_time
        print(f"🔎 Horário atual do sistema (ajustado): {current_time}")
        print(f"🔎 Último dado recebido: {last_data_time}")
        print(f"🔎 Diferença de tempo: {time_difference}")

        # Define um limite de tolerância de 30 minutos
        if time_difference > timedelta(minutes=30):
            print(f"⚠️ Os dados estão desatualizados! Último dado: {last_data_time}")
            return None  # Retorna None se os dados estiverem desatualizados
        else:
            print(f"✅ Dados atualizados! Último dado: {last_data_time}")

        return data
    except Exception as e:
        print(f"❌ Erro ao buscar dados: {e}")
        return None
