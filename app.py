import streamlit as st
import yfinance as yf
from news import get_news

st.set_page_config(page_title="Financial Dashboard", layout="wide")
st.title("Real Time Financial Market Dashboard with News Sentiment")

ticker = st.text_input("Enter Stock Ticker (e.g. AAPL, GOOG, MSFT):", value = "AAPL").upper()

if ticker:
    stock = yf.Ticker(ticker)
    stock_info = stock.info
    st.subheader(f"{stock_info.get('shortName',ticker)}")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Price", f"${stock_info.get('regularMarketPrice', 'N/A')}")
        st.metric("Day High", f"${stock_info.get('dayHigh', 'N/A')}")
        st.metric("Day Low", f"${stock_info.get('dayLow', 'N/A')}")
    with col2:
        st.metric("Market Cap", f"${stock_info.get('marketCap', 'N/A'):,}")
        st.metric("PE Ratio", stock_info.get('trailingPE', 'N/A'))
        st.metric("52-Week Low", f"${stock_info.get('fiftyTwoWeekLow', 'N/A')}")

    st.markdown("---")
    st.subheader("Latest News & Sentiment")

    news_data = get_news(ticker)
    for article in news_data:
        sentiment_emoji = "😊" if article['sentiment'] > 0 else ("😐" if article['sentiment'] == 0 else "😠")
        st.markdown(f"**{article['title']}**")
        st.markdown(f"*Published on:* {article['published']}")
        st.markdown(f"Sentiment: {sentiment_emoji} ({article['sentiment']:.2f})")
        st.markdown(f"[Read more]({article['url']})")
        st.markdown("---")