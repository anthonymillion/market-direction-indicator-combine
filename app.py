import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

st.set_page_config(layout='wide')
st.title("📊 Market Direction Indicator — Unified Dashboard")

# Sample data: Simulated time series for each asset
date_range = pd.date_range(start='2024-01-01', periods=100, freq='D')
assets = ['EUR/USD', 'SPX', 'AAPL', 'USD/JPY', 'DAX', 'TSLA']
asset_data = {
    asset: {
        "Date": date_range,
        "Fundamentals": pd.Series(range(50 + i, 150 + i)),
        "Sentiment": pd.Series(range(60 + i, 160 + i)),
        "Geopolitical Risk": pd.Series(range(30 + i, 130 + i))
    }
    for i, asset in enumerate(assets)
}

# Alert thresholds
def show_alerts(df, asset):
    last = df.iloc[-1]
    if last['Fundamentals'] > 70:
        st.toast(f"📈 {asset} Fundamentals: {last['Fundamentals']} (Strong Bullish)", icon="✅")
        play_sound()
    if last['Sentiment'] < 30:
        st.toast(f"📉 {asset} Sentiment: {last['Sentiment']} (Strong Bearish)", icon="⚠️")
        play_sound()
    if last['Geopolitical Risk'] > 65:
        st.toast(f"⚠️ {asset} Geopolitical Risk: {last['Geopolitical Risk']} (High Tension)", icon="🚨")
        play_sound()

# Sound injection
def play_sound():
    st.markdown(
        '''
        <audio autoplay>
            <source src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" type="audio/ogg">
        </audio>
        ''',
        unsafe_allow_html=True
    )

# Display all assets on one dashboard
for asset in assets:
    st.markdown(f"### {asset}")
    df = pd.DataFrame(asset_data[asset])

    col1, col2, col3 = st.columns(3)
    with col1:
        fig = px.line(df, x="Date", y="Fundamentals", title="Fundamentals", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.line(df, x="Date", y="Sentiment", title="Sentiment", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    with col3:
        fig = px.line(df, x="Date", y="Geopolitical Risk", title="Geo Risk", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    # Show alerts
    show_alerts(df, asset)

    # Log scores
    today = datetime.date.today().isoformat()
    latest_row = df.iloc[-1].to_frame().T
    latest_row.insert(0, "Asset", asset)
    latest_row.to_csv(f"history_{asset.replace('/', '')}.csv", mode='a', index=False, header=False)

    st.markdown("---")