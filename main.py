import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime
import io
import time
import random

# --- CONFIG ---
st.set_page_config(page_title="Zero-Gravity: 2026 Core", layout="wide", initial_sidebar_state="expanded")

# --- INITIALIZE SESSION STATE ---
if 'alert_mode' not in st.session_state:
    st.session_state.alert_mode = False
if 'confidence_level' not in st.session_state:
    st.session_state.confidence_level = 85
if 'vault_active' not in st.session_state:
    st.session_state.vault_active = False

# --- DATA FETCHING ---
@st.cache_data(ttl=3600)
def fetch_rates():
    try:
        r = requests.get("https://api.frankfurter.app/latest?from=USD")
        return r.json().get('rates', {})
    except:
        return {"HUF": 355, "TRY": 31, "BRL": 5.1, "IRR": 42000}

rates = fetch_rates()

# --- CUSTOM FONTS ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

# --- SIDEBAR: CONTROLS & EMERGENCY ---
with st.sidebar:
    st.markdown("<h2 class='neon-text'>⌨️ TERMINAL_CMD</h2>", unsafe_allow_html=True)
    theme_neon = st.toggle("Max Neon Glow", value=True)
    scan_lines = st.toggle("Overlay Scanlines", value=True)
    
    st.divider()
    
    st.markdown("<h2 class='neon-text'>🚨 PROTOCOLS</h2>", unsafe_allow_html=True)
    if st.button("🔴 EMERGENCY_MELTDOWN", type="primary", use_container_width=True):
        st.session_state.alert_mode = not st.session_state.alert_mode
        st.session_state.confidence_level = 15 if st.session_state.alert_mode else 85
        st.rerun()
    
    if st.session_state.alert_mode:
        st.warning("CRITICAL ERROR: MARKET DETONATION DETECTED!")
    
    st.divider()
    
    st.markdown("<h2 class='neon-text'>💾 DATA_LINK</h2>", unsafe_allow_html=True)
    df_hist_data = [
        {"Country": "Hungary", "Year": 1946, "Zeros": 29, "ISO": "HUN", "BaseCurr": "HUF", "Risk": 0.9, "Stability": 0.1, "Faith": 0.05},
        {"Country": "Zimbabwe", "Year": 2009, "Zeros": 12, "ISO": "ZWE", "BaseCurr": "ZWL", "Risk": 0.95, "Stability": 0.05, "Faith": 0.1},
        {"Country": "Germany", "Year": 1923, "Zeros": 12, "ISO": "DEU", "BaseCurr": "EUR", "Risk": 0.1, "Stability": 0.9, "Faith": 0.95},
        {"Country": "Greece", "Year": 1944, "Zeros": 11, "ISO": "GRC", "BaseCurr": "EUR", "Risk": 0.2, "Stability": 0.8, "Faith": 0.8},
        {"Country": "Venezuela", "Year": 2021, "Zeros": 6, "ISO": "VEN", "BaseCurr": "VES", "Risk": 0.9, "Stability": 0.1, "Faith": 0.1},
        {"Country": "Bolivia", "Year": 1987, "Zeros": 6, "ISO": "BOL", "BaseCurr": "BOB", "Risk": 0.4, "Stability": 0.6, "Faith": 0.5},
        {"Country": "Peru", "Year": 1991, "Zeros": 6, "ISO": "PER", "BaseCurr": "PEN", "Risk": 0.3, "Stability": 0.7, "Faith": 0.7},
        {"Country": "Turkey", "Year": 2005, "Zeros": 6, "ISO": "TUR", "BaseCurr": "TRY", "Risk": 0.4, "Stability": 0.6, "Faith": 0.5},
        {"Country": "Argentina", "Year": 1992, "Zeros": 4, "ISO": "ARG", "BaseCurr": "ARS", "Risk": 0.8, "Stability": 0.2, "Faith": 0.3},
        {"Country": "Brazil", "Year": 1994, "Zeros": 3, "ISO": "BRA", "BaseCurr": "BRL", "Risk": 0.3, "Stability": 0.7, "Faith": 0.8},
        {"Country": "Russia", "Year": 1998, "Zeros": 3, "ISO": "RUS", "BaseCurr": "RUB", "Risk": 0.5, "Stability": 0.5, "Faith": 0.4},
        {"Country": "Mexico", "Year": 1993, "Zeros": 3, "ISO": "MEX", "BaseCurr": "MXN", "Risk": 0.2, "Stability": 0.8, "Faith": 0.8},
        {"Country": "Poland", "Year": 1995, "Zeros": 4, "ISO": "POL", "BaseCurr": "PLN", "Risk": 0.1, "Stability": 0.9, "Faith": 0.9},
        {"Country": "Ghana", "Year": 2007, "Zeros": 4, "ISO": "GHA", "BaseCurr": "GHS", "Risk": 0.5, "Stability": 0.5, "Faith": 0.5},
        {"Country": "Israel", "Year": 1985, "Zeros": 3, "ISO": "ISR", "BaseCurr": "ILS", "Risk": 0.1, "Stability": 0.9, "Faith": 0.9},
        {"Country": "Romania", "Year": 2005, "Zeros": 4, "ISO": "ROU", "BaseCurr": "RON", "Risk": 0.2, "Stability": 0.8, "Faith": 0.8},
        {"Country": "Iran", "Year": 2025, "Zeros": 4, "ISO": "IRN", "BaseCurr": "IRR", "Risk": 0.7, "Stability": 0.3, "Faith": 0.2},
        {"Country": "Ukraine", "Year": 1996, "Zeros": 5, "ISO": "UKR", "BaseCurr": "UAH", "Risk": 0.6, "Stability": 0.4, "Faith": 0.3},
        {"Country": "Yugoslavia", "Year": 1994, "Zeros": 7, "ISO": "SRB", "BaseCurr": "RSD", "Risk": 0.9, "Stability": 0.1, "Faith": 0.1},
        {"Country": "Nicaragua", "Year": 1991, "Zeros": 6, "ISO": "NIC", "BaseCurr": "NIO", "Risk": 0.7, "Stability": 0.3, "Faith": 0.3},
        {"Country": "Angola", "Year": 1999, "Zeros": 6, "ISO": "AGO", "BaseCurr": "AOA", "Risk": 0.8, "Stability": 0.2, "Faith": 0.2},
        {"Country": "France", "Year": 1960, "Zeros": 2, "ISO": "FRA", "BaseCurr": "EUR", "Risk": 0.05, "Stability": 0.95, "Faith": 0.98},
        {"Country": "Sudan", "Year": 2007, "Zeros": 2, "ISO": "SDN", "BaseCurr": "SDG", "Risk": 0.8, "Stability": 0.2, "Faith": 0.2},
        {"Country": "South Korea", "Year": 1962, "Zeros": 1, "ISO": "KOR", "BaseCurr": "KRW", "Risk": 0.1, "Stability": 0.9, "Faith": 0.95},
        {"Country": "Mozambique", "Year": 2006, "Zeros": 3, "ISO": "MOZ", "BaseCurr": "MZN", "Risk": 0.4, "Stability": 0.6, "Faith": 0.6},
        {"Country": "Madagascar", "Year": 2003, "Zeros": 1, "ISO": "MDG", "BaseCurr": "MGA", "Risk": 0.5, "Stability": 0.5, "Faith": 0.5}
    ]
    df_hist = pd.DataFrame(df_hist_data)
    csv = df_hist.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Sync Database", csv, "zeros_history.csv", "text/csv")
    
    st.divider()
    st.info("System Status: " + ("🚨 BREACHED" if st.session_state.alert_mode else "🌐 STABLE"))

# --- CSS: CYBERPUNK ENGINE 3.0 ---
primary_color = "#ff0000" if st.session_state.alert_mode else "#00d4ff"
glow_intensity = f"0 0 15px {primary_color}" if theme_neon else "none"
scanline_opacity = "0.1" if scan_lines else "0"
alert_animation = "shake 0.5s infinite" if st.session_state.alert_mode else "none"

st.markdown(f"""
    <style>
    /* Global Styles */
    .stApp {{
        background: radial-gradient(circle at 50% 50%, {'#1b0000' if st.session_state.alert_mode else '#0a0a12'}, #000000);
        color: #e0e0e0;
        font-family: 'Rajdhani', sans-serif;
        animation: {alert_animation};
    }}
    
    @keyframes shake {{
        0% {{ transform: translate(1px, 1px) rotate(0deg); }}
        10% {{ transform: translate(-1px, -2px) rotate(-1deg); }}
        20% {{ transform: translate(-3px, 0px) rotate(1deg); }}
        30% {{ transform: translate(3px, 2px) rotate(0deg); }}
        40% {{ transform: translate(1px, -1px) rotate(1deg); }}
        50% {{ transform: translate(-1px, 2px) rotate(-1deg); }}
        60% {{ transform: translate(-3px, 1px) rotate(0deg); }}
        70% {{ transform: translate(3px, 1px) rotate(-1deg); }}
        80% {{ transform: translate(-1px, -1px) rotate(1deg); }}
        90% {{ transform: translate(1px, 2px) rotate(0deg); }}
        100% {{ transform: translate(1px, -2px) rotate(-1deg); }}
    }}

    /* Scanlines Overlay */
    .stApp::before {{
        content: " ";
        display: block;
        position: fixed;
        top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
        z-index: 1000;
        background-size: 100% 2px, 3px 100%;
        pointer-events: none;
        opacity: {scanline_opacity};
    }}

    .glitch-text {{
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        font-weight: bold;
        color: white;
        text-transform: uppercase;
        animation: glitch 1s linear infinite;
        text-shadow: {glow_intensity};
    }}

    @keyframes glitch {{
        0% {{ transform: translate(0); text-shadow: -2px 0 red, 2px 0 blue; }}
        20% {{ transform: translate(-2px, 2px); }}
        40% {{ transform: translate(-2px, -2px); text-shadow: 2px 0 red, -2px 0 blue; }}
        60% {{ transform: translate(2px, 2px); }}
        80% {{ transform: translate(2px, -2px); text-shadow: -2px 0 red, 2px 0 blue; }}
        100% {{ transform: translate(0); }}
    }}

    .neon-text {{
        color: {primary_color};
        text-shadow: {glow_intensity};
        font-family: 'Orbitron', sans-serif;
    }}

    .glass-card {{
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid {primary_color}44;
        backdrop-filter: blur(10px);
        box-shadow: {glow_intensity};
        transition: transform 0.3s ease;
    }}
    
    .glass-card:hover {{
        transform: scale(1.02) translateY(-5px);
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid {primary_color};
    }}

    /* Ticker */
    @keyframes scroll {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
    .ticker-wrap {{ 
        width: 100%; 
        overflow: hidden; 
        background: rgba(0, 212, 255, 0.05); 
        padding: 10px 0; 
        border-bottom: 2px solid {primary_color}; 
        margin-bottom: 30px;
    }}
    .ticker {{ 
        white-space: nowrap; 
        display: inline-block; 
        animation: scroll 30s linear infinite; 
        font-family: 'Courier New', monospace; 
        color: {primary_color}; 
        font-weight: bold; 
    }}
    </style>
    """, unsafe_allow_html=True)

# --- NEWS TERMINAL (SIMULATED 2026) ---
news_feed = [
    "BREAKING: Lunar Colony adopts New Hungarian Pengo for space trade.",
    "ALERT: AI Central Bank predicts hyperinflation in the Metaverse real estate.",
    "UPDATE: Zero-G Protocol activated by G7 finance ministers.",
    "MARKET: Ghost Rates reach all-time highs in the Shadow Economy.",
    "INFO: Digital Yen redenominated to 'Neo-Yen' with 12 zeros removed."
]
ticker_content = " | ".join(news_feed)
st.markdown(f'<div class="ticker-wrap"><div class="ticker">{ticker_content}</div></div>', unsafe_allow_html=True)

# --- TITLE & SENTIMENT HUD ---
c_title, c_sent = st.columns([3, 1])
with c_title:
    st.markdown(f'<div class="glitch-text">ZERO-GRAVITY // {"RED_ALERT" if st.session_state.alert_mode else "2026"}</div>', unsafe_allow_html=True)
with c_sent:
    fig_sent = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = st.session_state.confidence_level,
        title = {'text': "MARKET_CONFIDENCE", 'font': {'family': 'Orbitron', 'size': 14}},
        gauge = {'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': primary_color},
                 'bar': {'color': primary_color},
                 'bgcolor': "rgba(0,0,0,0)",
                 'borderwidth': 2,
                 'bordercolor': primary_color,
                 'steps': [
                     {'range': [0, 30], 'color': "rgba(255, 0, 0, 0.3)"},
                     {'range': [30, 70], 'color': "rgba(255, 255, 0, 0.1)"},
                     {'range': [70, 100], 'color': "rgba(0, 212, 255, 0.1)"}],
                 'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 90}}
    ))
    fig_sent.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': primary_color, 'family': "Rajdhani"}, margin=dict(l=20, r=20, t=30, b=20), height=150)
    st.plotly_chart(fig_sent, use_container_width=True)

st.write("---")

# --- 1. THE ORACLE (AI ANALYST) ---
st.markdown("### 👁️ THE ORACLE'S VISION")
oracle_quotes = [
    "Currency is just paper with an ego.",
    "Zeros are the scars of history.",
    "Stability is a glitch in the simulation.",
    "The printer never sleeps, why should you?",
    "Redenomination: The financial version of 'turning it off and on again'."
] if not st.session_state.alert_mode else [
    "RUN.",
    "THE SIMULATION IS COLLAPSING.",
    "SELL EVERYTHING. BUY BREAD.",
    "ZIMBABWE WAS JUST THE TUTORIAL.",
    "ZERO IS COMING FOR YOUR CREDITS."
]
with st.container():
    st.markdown(f"""
    <div class='glass-card' style='border-left: 5px solid {primary_color};'>
        <p style='font-style: italic; font-size: 1.2em;'>"{random.choice(oracle_quotes)}"</p>
        <p style='text-align: right; color: {primary_color};'>— CORE_ANALYSIS_v{"9.9" if st.session_state.alert_mode else "4.2"}</p>
    </div>
    """, unsafe_allow_html=True)

st.write(" ")

# --- 2. THE EVAPORATOR (PHASE 3) ---
st.markdown("### 🌪️ THE_EVAPORATOR: WEALTH_DISSOLUTION_SIM")
evap_c1, evap_c2 = st.columns([1, 2])
with evap_c1:
    v_amt = st.number_input("Vault Deposit ($):", value=1000, step=100)
    if st.button("ACTIVATE_EVAPORATION", use_container_width=True):
        st.session_state.vault_active = True
with evap_c2:
    if st.session_state.vault_active:
        progress_bar = st.progress(100)
        status_text = st.empty()
        value_text = st.empty()
        for i in range(100, -1, -5):
            time.sleep(0.1)
            progress_bar.progress(i)
            status_text.text(f"DISSOLVING... Confidence: {i}%")
            current_v = v_amt * (i / 100)
            value_text.markdown(f"<h2 style='color: {primary_color};'>Value: ${current_v:,.2f}</h2>", unsafe_allow_html=True)
        st.session_state.vault_active = False
        st.error("EVAPORATION COMPLETE: ASSETS REDUCED TO DATA-DUST.")
    else:
        st.markdown("<div class='glass-card' style='height: 100px; display: flex; align-items: center; justify-content: center;'>VAULT_IDLE // AWAITING AUTHORIZATION</div>", unsafe_allow_html=True)

# --- 3. PREDICTIVE RISK MATRIX (PHASE 3) ---
st.write("---")
st.markdown("### 🔮 PREDICTIVE_RISK_MATRIX: THE_NEXT_ZERO")
df_hist['NextZeroProb'] = (df_hist['Risk'] * 0.5 + (df_hist['Zeros'] / 29) * 0.3 + (1 - df_hist['Stability']) * 0.2) * 100
df_sorted = df_hist.sort_values(by='NextZeroProb', ascending=False)
matrix_cols = st.columns(5)
for i in range(5):
    target = df_sorted.iloc[i]
    with matrix_cols[i]:
        st.markdown(f"""
        <div class='glass-card' style='border-top: 4px solid {primary_color if target['NextZeroProb'] > 70 else "#00d4ff"};'>
            <p style='color: #888; margin-bottom: 0;'>{target['Country']}</p>
            <h2 style='margin: 5px 0;'>{target['NextZeroProb']:.1f}%</h2>
            <p style='font-size: 0.7em;'>PROBABILITY_SYNC</p>
        </div>
        """, unsafe_allow_html=True)

# --- 4. TACTICAL RADAR & CHRONOS ---
st.write("---")
row4_c1, row4_c2 = st.columns([1, 1])
with row4_c1:
    st.markdown("### 🛰️ TACTICAL_CURRENCY_RADAR")
    selected_country = st.selectbox("Select Target:", df_hist['Country'].tolist())
    target_data = df_hist[df_hist['Country'] == selected_country].iloc[0]
    radar_df = pd.DataFrame(dict(
        r=[target_data['Risk'], target_data['Stability'], target_data['Faith'], 0.5],
        theta=['Risk', 'Stability', 'Faith', 'Meta-Volatility']
    ))
    fig_radar = px.line_polar(radar_df, r='r', theta='theta', line_close=True, template="plotly_dark")
    fig_radar.update_traces(fill='toself', line_color=primary_color)
    fig_radar.update_layout(polar=dict(bgcolor='rgba(0,0,0,0)'), paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=20, b=20), height=300)
    st.plotly_chart(fig_radar, use_container_width=True)

with row4_c2:
    st.markdown("### ⏳ HISTORICAL_CHRONOS")
    fig_timeline = px.scatter(df_hist, x="Year", y="Zeros", size="Zeros", color="Country",
                             hover_name="Country", size_max=40, template="plotly_dark")
    fig_timeline.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=300, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_timeline, use_container_width=True)

# --- 5. BREAD INDEX & GLOBAL SCANNER ---
st.write("---")
row5_c1, row5_c2 = st.columns([1, 1])
with row5_c1:
    st.markdown("### 🍞 BREAD_INDEX: THE EROSION")
    bread_data = pd.DataFrame({
        "Economy Phase": ["Stable", "Inflated", "Hyperactive", "Rebooted"],
        "Buying Power (Kg)": [10.0, 1.0, 0.0001, 9.5]
    })
    fig_bread = px.area(bread_data, x="Economy Phase", y="Buying Power (Kg)", 
                        color_discrete_sequence=[primary_color], template="plotly_dark")
    fig_bread.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=300)
    st.plotly_chart(fig_bread, use_container_width=True)

with row5_c2:
    st.markdown("### 🗺️ GLOBAL_SCANNER")
    fig_map = px.choropleth(df_hist, locations="ISO", color="Zeros",
                            color_continuous_scale="Reds" if st.session_state.alert_mode else "Viridis", template="plotly_dark")
    fig_map.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)', showframe=False), paper_bgcolor='rgba(0,0,0,0)', height=300, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_map, use_container_width=True)

# --- 6. PHANTOM VALUES (GRID) ---
st.write("---")
st.markdown("### 👻 PHANTOM_VALUES (Old Units / 1 USD)")
grid_cols = 4
for i in range(0, len(df_hist_data), grid_cols):
    cols = st.columns(grid_cols)
    for j in range(grid_cols):
        if i + j < len(df_hist_data):
            row = df_hist_data[i + j]
            current_rate = rates.get(row['BaseCurr'], 1.0)
            ghost = current_rate * (10 ** row['Zeros'])
            with cols[j]:
                st.markdown(f"""
                <div class='glass-card' style='margin-bottom: 15px;'>
                    <p style='color: #888; margin-bottom: 0; font-size: 0.7em;'>{row['Country']} ({row['Year']})</p>
                    <h3 style='color: {primary_color}; margin: 2px 0; font-size: 1.1em;'>{ghost:.1e}</h3>
                </div>
                """, unsafe_allow_html=True)

# --- 7. THE SHAVER (UPGRADED) ---
st.write("---")
st.markdown("### ✂️ ZERO_SHAVER_HYPERMOD")
s1, s2 = st.columns([1, 2])
with s1:
    u_val = st.number_input("INPUT_CREDITS:", value=1000000000, step=1000000)
    u_cut = st.select_slider("LEVEL_OF_REDACTION:", options=[3, 6, 9, 12, 15, 29])
    stabilize = st.button("EXECUTE_STABILIZATION")
with s2:
    if stabilize:
        new_val = u_val / (10**u_cut)
        st.balloons()
        st.markdown(f"""
        <div class='glass-card' style='text-align: center; border-color: {primary_color}; box-shadow: 0 0 20px {primary_color};'>
            <h2 style='color: {primary_color};'>STABILIZATION COMPLETE</h2>
            <p style='font-size: 1.5em;'>{u_val:,.0f} ➔ <span style='color: #00d4ff; font-weight: bold;'>{new_val:,.2f}</span></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<div class='glass-card' style='height: 150px; display: flex; align-items: center; justify-content: center;'><p>AWAITING INPUT COMMAND...</p></div>", unsafe_allow_html=True)

# Footer
st.divider()
st.markdown(f"""
<div style='text-align: center; opacity: 0.5; font-size: 0.8em;'>
    <p>ANTIGRAVITY SYSTEMS // 2026 // {"LEVEL_RED" if st.session_state.alert_mode else "SYSTEM_READY"}</p>
</div>
""", unsafe_allow_html=True)