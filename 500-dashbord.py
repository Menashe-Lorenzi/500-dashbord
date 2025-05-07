import streamlit as st
import yfinance as yf
import pandas as pd

# Fetch the S&P 500 stock symbols from Wikipedia
@st.cache
def get_sp500_symbols():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    table = pd.read_html(url)[0]
    return table[['Symbol', 'Security', 'GICS Sector']]

# Fetch stock data using yfinance
@st.cache
def fetch_stock_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="1y")
        return history
    except Exception as e:
        return None

st.set_page_config(page_title="S&P 500 Stocks Dashboard", layout="wide")

st.title("S&P 500 Stocks Dashboard")
st.write("Explore the performance and stats of S&P 500 companies.")

# Fetch symbols
sp500_table = get_sp500_symbols()

# Sidebar filters
sector = st.sidebar.selectbox("Select Sector", ["All"] + sorted(sp500_table['GICS Sector'].unique()))
selected_symbol = st.sidebar.selectbox("Select Symbol", ["All"] + sorted(sp500_table['Symbol'].unique()))

# Filter data based on user selection
filtered_table = sp500_table
if sector != "All":
    filtered_table = filtered_table[filtered_table['GICS Sector'] == sector]
if selected_symbol != "All":
    filtered_table = filtered_table[filtered_table['Symbol'] == selected_symbol]

st.dataframe(filtered_table)

# Show general stats
st.header("General Stats")
if selected_symbol != "All":
    data = fetch_stock_data(selected_symbol)
    if data is not None:
        st.line_chart(data['Close'])
        st.write(f"General statistics for {selected_symbol}:")
        st.write(data.describe())
    else:
        st.write("Failed to fetch data for the selected symbol.")
else:
    st.write("Select a specific stock symbol to view detailed statistics.")

st.sidebar.markdown("Developed with Streamlit and Yahoo Finance API.")
