
import datetime
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf

# Initialize start and end date
today = datetime.date.today()
before = today - datetime.timedelta(days=365) # 1 year before today

with st.sidebar:
    # Input elements
    ticker_1 = st.text_input("Ticker-Symbol 1", value="GOOG")
    ticker_2 = st.text_input("Ticker-Symbol 2", value="AAPL")
    ticker_3 = st.text_input("Ticker-Symbol 3", value="MSFT")
    start_date = st.date_input("Start-Datum", value=before)
    end_date = st.date_input("End-Datum", value=today)
    
    st.markdown('''<small>__Anleitung__<br>
                1. In die Ticker-Symbol Felder müssen gültige Symbole eingetragen werden.  
                   Wenn nur ein oder zwei Aktienverläufe angezeigt werden sollen, können 
                   Felder leer gelassen werden.<br>
                2. Das Start-Datum muss vor dem End-Datum liegen.<br>
                <br>
                __Allgemeines__<br>
                Dieses Dashboard verwendet [Python](https://www.python.org/), [Streamlit](https://streamlit.io/), [Plotly](https://plotly.com/) und [yfinance](https://pypi.org/project/yfinance/).<br>
                Der Quelltext dieses Dashboards liegt auf [GitHub](https://github.com/alexmahesh/Stock_App).<br>
                <br>
               __Legal Disclaimer for Yahoo:__<br>
               Yahoo!, Y!Finance, and Yahoo! finance are registered trademarks of Yahoo, Inc.<br>
               yfinance is not affiliated, endorsed, or vetted by Yahoo, Inc. It's an open-source tool that uses Yahoo's publicly available APIs, and is intended for research and educational purposes.<br>
               You should refer to Yahoo!'s terms of use ([here](https://legal.yahoo.com/us/en/yahoo/terms/product-atos/apiforydn/index.html), [here](https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html), and [here](https://policies.yahoo.com/us/en/yahoo/terms/index.htm)) for details on your rights to use the actual data downloaded. Remember - the Yahoo! finance API is intended for personal use only.</small>''',
               unsafe_allow_html = True)
    
    st.markdown('''<small>__Impressum__<br>
                Verantwortlich für den Inhalt:<br>
                Alexander Schuppe<br>
                Email: spmail@aleku.eu<br>
                <br>
                __Datenschutz__<br>
                Dieses Dashboard speichert keine persönlichen Daten und verwendet keine Cookies.<br>
                Die Seite verwendet das kostenlose Hosting-Angebot von [Streamlit](https://streamlit.io/). Nähere Informationen zu deren Datenschutzangaben finden sie unter: [Streamlit Privacy Policy]().<br>
                <br>
                __Haftungsausschluss__<br>
                Es wird keine Garantie für die Richtigkeit der hier dargestellten Daten und Zusammenhänge übernommen.
                </small>''',
                unsafe_allow_html = True)

# Load data from Yahoo Finance
if ticker_1:
    dat_1 = yf.Ticker(ticker_1) # Info's about single share
    data_1 = yf.download(ticker_1, start=start_date, end=end_date) # Price history
    symbol_1 = dat_1.info['symbol']
    name_1 = dat_1.info['shortName']
else:
    symbol_1 = ''
    name_1 = ''
    
if ticker_2:
    dat_2 = yf.Ticker(ticker_2) # Info's about single share
    data_2 = yf.download(ticker_2, start=start_date, end=end_date) # Price history
    symbol_2 = dat_2.info['symbol']
    name_2 = dat_2.info['shortName']
else:
    symbol_2 = ''
    name_2 = ''
    
if ticker_3:
    dat_3 = yf.Ticker(ticker_3) # Info's about single share
    data_3 = yf.download(ticker_3, start=start_date, end=end_date) # Price history
    symbol_3 = dat_3.info['symbol']
    name_3 = dat_3.info['shortName']
else:
    symbol_3 = ''
    name_3 = ''

st.title("Börsenticker")

# Create Subheader
#blue, red, green
ampersand = False
subheader = f'##### Ticker für '
if ticker_1:
    subheader += f':blue[{name_1}]'
    ampersand = True
if ticker_2:
    if ampersand:
        subheader += f' & '
    subheader += f':red[{name_2}]'
    ampersand = True
if ticker_3:
    if ampersand:
        subheader += f' & '
    subheader += f':green[{name_3}]'

st.markdown(subheader)
# st.markdown(f'''##### Ticker für :blue[{name_1}] & :red[{name_2}] & :green[{name_3}]''')
st.markdown(f'''Vom {start_date.strftime("%d.%m.%Y")} bis zum {end_date.strftime("%d.%m.%Y")}''')

# Show line chart
#blue, red, green
fig = go.Figure()
if ticker_1:
    fig.add_trace(go.Scatter(x=data_1.index, y=data_1['Adj Close'], mode='lines', name=symbol_1,
                             line=dict(color='blue', width=2)))
if ticker_2:
    fig.add_trace(go.Scatter(x=data_2.index, y=data_2['Adj Close'], mode='lines', name=symbol_2,
                             line=dict(color='red', width=2)))
if ticker_3:
    fig.add_trace(go.Scatter(x=data_3.index, y=data_3['Adj Close'], mode='lines', name=symbol_3,
                             line=dict(color='green', width=2)))
fig.update_layout(
    title = 'Aktienkurse',
    xaxis_title = 'Datum',
    yaxis_title = 'Börsen-Schlusskurs'
)
st.plotly_chart(fig)

# Show table
opts = []
if ticker_1:
    opts.append('1. '+name_1)
if ticker_2:
    opts.append('2. '+name_2)
if ticker_3:
    opts.append('3. '+name_3)

tabelle = st.selectbox("Tabelle Aktienwerte", options = opts)
if tabelle[0] == '1':
    st.dataframe(data_1, use_container_width=True)
elif tabelle[0] == '2':
    st.dataframe(data_2, use_container_width=True)
elif tabelle[0] == '3':
    st.dataframe(data_3, use_container_width=True)
