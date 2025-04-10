from datetime import timedelta
import streamlit as st
import pandas as pd
import yfinance as yf
import os

# criar as funções de carregamento de dados
@st.cache_data
def carregar_dados(empresas):
    caminho_arquivo_cache = "cotacoes_cache.pkl"

    # Verifica se já existe cache salvo localmente
    if os.path.exists(caminho_arquivo_cache):
        try:
            cotacoes_validas = pd.read_pickle(caminho_arquivo_cache)
            return cotacoes_validas
        except Exception as e:
            print(f"Erro ao carregar cache local: {e}")
            # Se der erro ao carregar o cache, continua com o download

    # Se não existe cache ou deu erro, carrega tudo de novo
    cotacoes_validas = pd.DataFrame()
    progresso = st.progress(0)
    total = len(empresas)

    for i, ticker in enumerate(empresas):
        try:
            dados = yf.Ticker(ticker).history(period='1d', start="2010-01-01", end="2024-12-31")
            if not dados.empty:
                cotacoes_validas[ticker] = dados["Close"]
        except Exception as e:
            print(f"Erro ao carregar {ticker}: {e}")
        progresso.progress((i + 1) / total)

    progresso.empty()

    # Salva o cache em arquivo local
    try:
        cotacoes_validas.to_pickle(caminho_arquivo_cache)
    except Exception as e:
        print(f"Erro ao salvar cache local: {e}")

    return cotacoes_validas

@st.cache_data
def carregar_tickers_acoes():
    base_tickers = pd.read_csv("IBOV.csv", sep=";")
    tickers = list(base_tickers["Código"])
    tickers = [item + ".SA" for item in tickers]
    return tickers

acoes = carregar_tickers_acoes()
dados = carregar_dados(acoes)

#Criar a interface do streamlit

# prepara as visualizações = filtros
st.sidebar.header("Filtros")

# filtro de ações
lista_acoes = st.sidebar.multiselect("Escolha as ações para visualizar", dados.columns)
if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: "Close"})

# filtro de datas
data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()
data_inicio_padrao = data_final - timedelta(days=30)
intervalo_data = st.sidebar.slider(
    "Selecione o período",
    min_value=data_inicial,
    max_value=data_final,
    value=(data_inicio_padrao, data_final),
    help="Selecione o intervalo de datas para visualizar os preços"
)


dados = dados.loc[intervalo_data[0]:intervalo_data[1]]

st.title("📈 App de Preço de Ações")
st.caption(f"Visualizando de {intervalo_data[0].date()} até {intervalo_data[1].date()}")

#criar o grafico
st.line_chart(dados)

# calculo de performance
texto_performance_ativos = ""

if len(lista_acoes) == 0:
    lista_acoes = list(dados.columns)
elif len(lista_acoes) == 1:
    dados = dados.rename(columns={"Close": acao_unica})

carteira = [1000 for acao in lista_acoes]
total_inicial_carteira = sum(carteira)


for i, acao in enumerate(lista_acoes):
    performance_ativo = dados[acao].iloc[-1] / dados[acao].iloc[0] - 1
    performance_ativo = float(performance_ativo)

    carteira[i] = carteira[i] * (1 + performance_ativo)

    if performance_ativo > 0:
        #  :cor[texto]
        texto_performance_ativos = texto_performance_ativos + f"  \n{acao}:  :green[{performance_ativo:.1%}]"
    elif performance_ativo < 0:
        texto_performance_ativos = texto_performance_ativos + f"  \n{acao}: :red[{performance_ativo:.1%}]"
    else:
        texto_performance_ativos = texto_performance_ativos + f"  \n{acao}: {performance_ativo:.1%}"

total_final_carteira = sum(carteira)
performance_carteira = total_final_carteira / total_inicial_carteira -1

if performance_carteira > 0:
    texto_performance_carteira = f"Performance da carteira com todos os ativos:  :green[{performance_ativo:.1%}]"
elif performance_ativo < 0:
    texto_performance_carteira = f"Performance da carteira com todos os ativos: :red[{performance_ativo:.1%}]"
else:
    texto_performance_carteira = f"Performance da carteira com todos os ativos: {performance_ativo:.1%}"

st.write(
f"""
### Performance dos Ativos
Essa foi a performance de cada ativo no período selecionado:
 
{texto_performance_ativos}

{texto_performance_carteira}
""")
