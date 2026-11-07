import streamlit as st
from src.weather_tool import get_weather
from src.streamlit_agent import run_streamlit_agent


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Atmos AI",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =====================================================
# 2. SESSION STATE
# =====================================================

defaults = {
    "messages": [],
    "conversation_history": [],
    "token_usage": 0,
    "weather_data": None,
    "selected_theme": "Day",
    "theme_choice": "☀️ Day"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================================
# 3. THEME CONFIGURATION
# =====================================================

THEMES = {
    "Day": {
        "bg": "#F3F6FB",
        "surface": "#FFFFFF",
        "card": "#FFFFFF",
        "text": "#183153",
        "muted": "#718096",
        "border": "#DFE7F1",
        "accent": "#2563EB",
        "accent_hover": "#1D4ED8",
        "banner1": "#1D4ED8",
        "banner2": "#0891B2",
        "input": "#FFFFFF"
    },

    "Night": {
        "bg": "#0B1220",
        "surface": "#131F32",
        "card": "#18263B",
        "text": "#F1F5F9",
        "muted": "#9AABC0",
        "border": "#293950",
        "accent": "#6366F1",
        "accent_hover": "#4F46E5",
        "banner1": "#312E81",
        "banner2": "#1D4ED8",
        "input": "#18263B"
    }
}


# =====================================================
# 4. TOP HEADER AND THEME TOGGLE
# =====================================================

header_left, header_right = st.columns([5, 1])

with header_left:
    st.markdown(
        """
        <div class="brand">
            🌤️ Atmos AI
            <span class="brand-tag">WEATHER INTELLIGENCE</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with header_right:
    st.radio(
        "Theme",
        ["☀️ Day", "🌙 Night"],
        horizontal=True,
        label_visibility="collapsed",
        key="theme_choice"
    )

st.session_state.selected_theme = (
    "Day"
    if st.session_state.theme_choice == "☀️ Day"
    else "Night"
)

theme = THEMES[st.session_state.selected_theme]


# =====================================================
# 5. CUSTOM CSS
# =====================================================

st.markdown(f"""
<style>

/* Application background */

.stApp {{
    background: {theme['bg']};
    color: {theme['text']};
}}

/* Main viewport */

.block-container {{
    max-width: 1500px;
    padding: 0.7rem 2rem 0.5rem 2rem;
}}

/* Remove sidebar */

section[data-testid="stSidebar"] {{
    display: none;
}}

button[data-testid="collapsedControl"] {{
    display: none;
}}

/* Hide Streamlit top toolbar */

header[data-testid="stHeader"] {{
    height: 0;
    min-height: 0;
    background: transparent;
}}

[data-testid="stToolbar"] {{
    display: none;
}}

#MainMenu, footer {{
    visibility: hidden;
}}

/* Header */

.brand {{
    font-size: 29px;
    font-weight: 850;
    letter-spacing: -1.2px;
    color: {theme['text']};
    padding: 3px 0;
}}

.brand-tag {{
    font-size: 9px;
    letter-spacing: 2px;
    font-weight: 700;
    color: {theme['muted']};
    margin-left: 10px;
    vertical-align: middle;
}}

/* Theme selector */

div[role="radiogroup"] {{
    justify-content: flex-end;
    gap: 5px;
}}

div[role="radiogroup"] label {{
    background: {theme['surface']};
    border: 1px solid {theme['border']};
    border-radius: 20px;
    padding: 5px 10px;
    font-size: 12px;
}}

/* Analytics */

.analytics-card {{
    background: {theme['surface']};
    border: 1px solid {theme['border']};
    border-radius: 11px;
    padding: 9px 14px;
    height: 62px;
}}

.analytics-label {{
    color: {theme['muted']};
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.5px;
}}

.analytics-value {{
    color: {theme['text']};
    font-size: 19px;
    font-weight: 800;
    margin-top: 3px;
}}

/* Section headings */

.section-title {{
    color: {theme['text']};
    font-size: 20px;
    font-weight: 800;
    margin-bottom: 2px;
}}

.section-subtitle {{
    color: {theme['muted']};
    font-size: 11px;
    margin-bottom: 9px;
}}

/* Weather banner */

.location-banner {{
    background: linear-gradient(
        110deg,
        {theme['banner1']},
        {theme['banner2']}
    );
    border-radius: 12px;
    padding: 11px 17px;
    margin: 8px 0 16px 0;
    color: white;
}}

.location-name {{
    font-size: 19px;
    font-weight: 800;
    color: white;
}}

.location-caption {{
    color: #DBEAFE;
    font-size: 10px;
}}

/* Weather cards */

.weather-card {{
    background: {theme['card']};
    border: 1px solid {theme['border']};
    border-radius: 12px;
    padding: 11px 14px;
    height: 91px;
    transition: 0.2s ease;
}}

.weather-card:hover {{
    border-color: {theme['accent']};
    transform: translateY(-2px);
}}

.card-icon {{
    font-size: 18px;
}}

.card-label {{
    color: {theme['muted']};
    font-size: 10px;
    margin-top: 3px;
}}

.card-value {{
    color: {theme['text']};
    font-size: 21px;
    font-weight: 800;
    margin-top: 1px;
}}


/* ==========================================
   INPUT FIELDS
========================================== */

.stTextInput input,
.stChatInput textarea,
[data-testid="stChatInput"] textarea {{

    background-color: {theme['input']} !important;
    color: {theme['text']} !important;

    border: 1px solid {theme['border']} !important;
    border-radius: 9px !important;

    font-weight: 500 !important;
    opacity: 1 !important;
}}

/* Always-visible placeholder hints */

.stTextInput input::placeholder,
.stChatInput textarea::placeholder,
[data-testid="stChatInput"] textarea::placeholder {{

    color: {theme['muted']} !important;
    opacity: 1 !important;
}}

/* Input focus */

.stTextInput input:focus,
.stChatInput textarea:focus,
[data-testid="stChatInput"] textarea:focus {{

    border: 1px solid {theme['accent']} !important;
    box-shadow: 0 0 0 2px {theme['accent']}22 !important;
    outline: none !important;
}}


/* ==========================================
   CHECK WEATHER BUTTON - BLUE
========================================== */

.stButton button[kind="primary"] {{

    background-color: #1D4ED8 !important;
    color: #FFFFFF !important;

    border: 1px solid #1D4ED8 !important;
    border-radius: 9px !important;

    font-weight: 700 !important;
    min-height: 37px;
}}

.stButton button[kind="primary"]:hover {{

    background-color: #1E40AF !important;
    border-color: #1E40AF !important;
    color: #FFFFFF !important;
}}


/* ==========================================
   CLEAR CHAT BUTTON - RED
========================================== */

.stButton button[kind="secondary"] {{

    background-color: #DC2626 !important;
    color: #FFFFFF !important;

    border: 1px solid #DC2626 !important;
    border-radius: 9px !important;

    font-weight: 700 !important;
    min-height: 37px;
}}

.stButton button[kind="secondary"]:hover {{

    background-color: #B91C1C !important;
    border-color: #B91C1C !important;
    color: #FFFFFF !important;
}}


/* Force button text and icons to remain white */

.stButton button[kind="primary"] *,
.stButton button[kind="secondary"] * {{
    color: #FFFFFF !important;
}}


/* ==========================================
   CHAT INTERFACE
========================================== */

.chat-panel {{
    background: {theme['surface']};
    border: 1px solid {theme['border']};
    border-radius: 12px;
    padding: 8px 12px;
    margin-bottom: 6px;
}}

[data-testid="stChatMessage"] {{
    background: {theme['surface']};
    border: 1px solid {theme['border']};
    border-radius: 10px;
    padding: 7px 12px;
    margin-bottom: 5px;
}}

[data-testid="stChatInput"] {{
    background: {theme['surface']} !important;
    border: 1px solid {theme['border']} !important;
    border-radius: 11px;
}}


/* Dividers */

hr {{
    border-color: {theme['border']};
    margin: 0.5rem 0;
}}

/* General text */

h1, h2, h3, h4, p {{
    color: {theme['text']};
}}

/* Compact spacing */

div[data-testid="stVerticalBlock"] {{
    gap: 0.45rem;
}}

.footer {{
    color: {theme['muted']};
    text-align: center;
    font-size: 10px;
    padding: 3px;
}}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 6. ANALYTICS ROW
# =====================================================

a1, a2, a3, a4 = st.columns(4)

analytics = [
    (a1, "⚡ TOTAL TOKENS", f"{st.session_state.token_usage:,}"),
    (a2, "💬 CHAT MESSAGES", str(len(st.session_state.messages))),
    (
        a3,
        "📍 SELECTED CITY",
        st.session_state.weather_data["city"]
        if st.session_state.weather_data else "Not selected"
    ),
    (a4, "🎨 ACTIVE THEME", st.session_state.selected_theme)
]

for col, label, value in analytics:
    with col:
        st.markdown(f"""
        <div class="analytics-card">
            <div class="analytics-label">{label}</div>
            <div class="analytics-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)


st.divider()


# =====================================================
# 7. WEATHER DASHBOARD
# =====================================================

st.markdown(
    '<div class="section-title">🌍 Weather Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Explore current weather conditions across the world.'
    '</div>',
    unsafe_allow_html=True
)

input_col, button_col = st.columns([5, 1])

with input_col:
    city = st.text_input(
        "City",
        placeholder="Enter city name: Patna, Delhi, London...",
        label_visibility="collapsed"
    )

with button_col:
    check_weather = st.button(
        "Check Weather",
        type="primary",
        use_container_width=True
    )


if check_weather:

    if city.strip():

        with st.spinner("Fetching weather..."):
            data = get_weather(city.strip())

        if "error" in data:
            st.error(data["error"])

        else:
            st.session_state.weather_data = data

            # Refresh the application so analytics
            # displays the newly selected city.
            st.rerun()

    else:
        st.warning("Please enter a city name.")


# =====================================================
# 8. WEATHER DISPLAY
# =====================================================

weather = st.session_state.weather_data

if weather:

    st.markdown(f"""
    <div class="location-banner">
        <div class="location-name">
            📍 {weather['city']}, {weather['country']}
        </div>
        <div class="location-caption">
            Current weather conditions · Open-Meteo
        </div>
    </div>
    """, unsafe_allow_html=True)

    metrics = [
        ("🌡️", "Temperature", f"{weather['temperature_celsius']} °C"),
        ("🤗", "Feels Like", f"{weather['feels_like_celsius']} °C"),
        ("💧", "Humidity", f"{weather['humidity_percent']}%"),
        ("💨", "Wind Speed", f"{weather['wind_speed_kmh']} km/h"),
        ("🌧️", "Precipitation", f"{weather['precipitation_mm']} mm"),
        ("☁️", "Cloud Cover", f"{weather['cloud_cover_percent']}%")
    ]

    cols = st.columns(6)

    for col, (icon, label, value) in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div class="weather-card">
                <div class="card-icon">{icon}</div>
                <div class="card-label">{label}</div>
                <div class="card-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

else:

    st.info("🌤️ Search for a city to view its current weather.")


# =====================================================
# 9. CHAT INTERFACE
# =====================================================

st.divider()

chat_col, clear_col = st.columns([5, 1])

with chat_col:
    st.markdown(
        '<div class="section-title">🤖 Chat with Atmos AI</div>',
        unsafe_allow_html=True
    )

with clear_col:
    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True,
        type="secondary"
    ):
        st.session_state.messages = []
        st.session_state.conversation_history = []
        st.session_state.token_usage = 0
        st.rerun()


st.markdown(
    '<div class="section-subtitle">'
    'Compare cities, ask weather questions and explore conditions naturally.'
    '</div>',
    unsafe_allow_html=True
)


# =====================================================
# 10. CHAT HISTORY
# =====================================================

with st.container(height=190, border=True):

    if not st.session_state.messages:

        st.markdown(
            f"""
            <div style="
                text-align:center;
                padding:35px 10px;
                color:{theme['muted']};
            ">
                <div style="font-size:30px;">🌤️</div>
                <b>Welcome to Atmos AI</b>
                <br>
                <small>Ask me about the weather anywhere in the world.</small>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        for message in st.session_state.messages:

            with st.chat_message(message["role"]):
                st.markdown(message["content"])


# =====================================================
# 11. CHAT INPUT AND AI AGENT
# =====================================================

user_query = st.chat_input(
    "Ask Atmos AI about the weather..."
)

if user_query:

    st.session_state.messages.append({
        "role": "user",
        "content": user_query
    })

    with st.spinner("Atmos AI is thinking..."):

        try:

            result = run_streamlit_agent(
                user_query,
                st.session_state.conversation_history
            )

            answer = (
                result["answer"]
                or "I couldn't generate a response."
            )

            st.session_state.conversation_history = (
                result["conversation_history"]
            )

            st.session_state.token_usage += (
                result["total_tokens"]
            )

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as error:

            st.error(f"Something went wrong: {error}")


# =====================================================
# 12. FOOTER
# =====================================================

st.markdown(
    """
    <div class="footer">
        ATMOS AI · INTELLIGENT WEATHER ASSISTANT ·
        POWERED BY OPEN-METEO
    </div>
    """,
    unsafe_allow_html=True
)