import streamlit as st
import pandas as pd
import plotly.express as px
from news_sentiment import fetch_news, analyze_sentiment

# Streamlit Page Config
st.set_page_config(page_title="📰 Market Sentiment Dashboard", layout="wide")
st.title("📰 Real-Time News Sentiment Dashboard")

# Get API key from user
api_key = st.text_input("Enter your NewsAPI Key", type="password")

if api_key:
    # Search query input
    query = st.text_input("Enter keyword or sector to search (e.g. stock market, Tesla, banking)", value="stock market")

    # Fetch news
    with st.spinner("Fetching latest news..."):
        df = fetch_news(api_key, query=query)
    
    if not df.empty:
        # Analyze sentiment
        df["sentiment_label"] = df["title"].apply(analyze_sentiment)
        # Show Data Table
        st.subheader("🧠 Analyzed News Headlines")
        st.dataframe(df[["publishedAt", "source", "title", "sentiment_label"]])

        # Sentiment Distribution Pie Chart
        st.subheader("📊 Sentiment Distribution")
        sentiment_counts = df["sentiment_label"].value_counts().reset_index()
        sentiment_counts.columns = ["Sentiment", "Count"]

        fig = px.pie(sentiment_counts, names="Sentiment", values="Count", color="Sentiment",
                     color_discrete_map={"Positive": "green", "Neutral": "gray", "Negative": "red"})
        st.plotly_chart(fig, use_container_width=True)

        # Optionally: show latest headlines
        with st.expander("🔍 View Full Articles"):
            for index, row in df.iterrows():
                st.markdown(f"**{row['title']}** — *{row['source']}*")
                st.markdown(f"[Read more]({row['url']})")
                st.markdown("---")
    else:
        st.warning("No news articles found for that keyword.")
else:
    st.info("🔑 Please enter your NewsAPI key to begin.")

