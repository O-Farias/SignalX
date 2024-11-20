import pandas as pd

def calculate_moving_average(data, period):
    """
    Calcula a média móvel de 'period' períodos.
    """
    return data['close'].rolling(window=period).mean()

def calculate_rsi(data, period=14):
    """
    Calcula o Índice de Força Relativa (RSI).
    """
    delta = data['close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def identify_support_resistance(data, window=10):
    """
    Identifica os níveis de suporte e resistência com base no preço mínimo/máximo.
    """
    data['support'] = data['close'].rolling(window=window).min()
    data['resistance'] = data['close'].rolling(window=window).max()
    return data

def strategy_moving_average(data):
    """
    Estratégia baseada no cruzamento de médias móveis.
    """
    data['ma_short'] = calculate_moving_average(data, period=9)
    data['ma_long'] = calculate_moving_average(data, period=21)

    # Sinal de compra/venda
    if data['ma_short'].iloc[-1] > data['ma_long'].iloc[-1]:
        return "📈 Sinal de Compra (Médias Móveis)"
    elif data['ma_short'].iloc[-1] < data['ma_long'].iloc[-1]:
        return "📉 Sinal de Venda (Médias Móveis)"
    else:
        return "⏸️ Sem sinal claro (Médias Móveis)"

def strategy_rsi(data):
    """
    Estratégia baseada em RSI e níveis de suporte/resistência.
    """
    data['rsi'] = calculate_rsi(data)
    data = identify_support_resistance(data)

    # Verifica o último valor do RSI
    last_rsi = data['rsi'].iloc[-1]
    last_close = data['close'].iloc[-1]
    support = data['support'].iloc[-1]
    resistance = data['resistance'].iloc[-1]

    if last_rsi < 30 and last_close <= support:
        return "📈 Sinal de Compra (RSI e Suporte)"
    elif last_rsi > 70 and last_close >= resistance:
        return "📉 Sinal de Venda (RSI e Resistência)"
    else:
        return "⏸️ Sem sinal claro (RSI e Suporte/Resistência)"

def analyze_data(data):
    """
    Analisa os dados utilizando múltiplas estratégias e retorna os sinais.
    """
    try:
        # Estratégias a serem aplicadas
        ma_signal = strategy_moving_average(data)
        rsi_signal = strategy_rsi(data)

        # Retorno consolidado
        return {
            "moving_average_signal": ma_signal,
            "rsi_signal": rsi_signal
        }
    except Exception as e:
        return {"error": f"Erro na análise: {e}"}
