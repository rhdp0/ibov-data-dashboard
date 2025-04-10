# 📈 App de Preço de Ações - B3

Este é um app desenvolvido em **Python com Streamlit** para visualização e análise da **performance histórica de ações da B3 (IBOV)**, com foco em eficiência, performance e usabilidade.

## 🚀 Funcionalidades

- ✅ Download automático das cotações via API do [Yahoo Finance](https://www.yfinance.info/)
- ✅ Armazenamento em cache local (pickle) para evitar requisições desnecessárias
- ✅ Interface interativa com filtros de datas e ações
- ✅ Gráfico de linha para visualização da evolução dos preços
- ✅ Cálculo de performance individual dos ativos no período selecionado
- ✅ Simulação de carteira com alocação igualitária
- ✅ Destaque visual de ganhos e perdas com cores (verde/vermelho)

## 🧠 Tecnologias Utilizadas

- [Streamlit](https://streamlit.io/) — criação da interface interativa
- [Pandas](https://pandas.pydata.org/) — manipulação de dados
- [yFinance](https://pypi.org/project/yfinance/) — consulta de dados financeiros históricos
- [Python 3.10+](https://www.python.org/)

## 📂 Estrutura Esperada

Antes de rodar o app, certifique-se de ter um arquivo `IBOV.csv` com os tickers das ações, no seguinte formato:


> ⚠️ O sistema adiciona automaticamente o sufixo `.SA` para consultar na B3.

## ▶️ Como Executar Localmente

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/nome-do-repo.git
cd nome-do-repo
```

2. Instale as dependências
pip install -r requirements.txt

3. Execute o app:
streamlit run app.py

## 📊 Exemplo de uso

📌 Observações
O cache local é salvo no arquivo cotacoes_cache.pkl. Se quiser forçar a atualização, basta apagar esse arquivo.

O carregamento inicial pode demorar um pouco na primeira execução, mas nas próximas será quase instantâneo.
