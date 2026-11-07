# 🌤️ Atmos AI – Intelligent Weather Assistant

Atmos AI is an AI-powered weather assistant built with Python and Streamlit. It combines real-time weather information with conversational AI to provide users with an interactive way to explore weather conditions.

Ask about the weather in a city, check current weather metrics, or interact with the AI assistant through a clean, responsive dashboard.

## ✨ Features

- **AI-Powered Weather Assistant:** Ask weather-related questions in natural language.
- **Real-Time Weather Data:** Retrieve current weather information for locations worldwide.
- **Interactive Dashboard:** View weather information through a modern Streamlit interface.
- **Weather Metrics:**
  - Temperature
  - Feels-like temperature
  - Relative humidity
  - Wind speed
  - Precipitation
  - Cloud cover
- **Conversational Interface:** Maintain context across messages during a conversation.
- **Day & Night Themes:** Switch between light and dark dashboard appearances.
- **Token Usage Tracking:** Monitor AI model token consumption.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application |
| OpenAI Python SDK | AI model integration |
| OpenRouter | AI model access |
| Open-Meteo API | Weather and geocoding data |
| Requests | API communication |
| python-dotenv | Environment variable management |

## 📁 Project Structure

```text
atmos-ai-streamlit/
│
├── src/
│   ├── weather_tool.py
│   └── streamlit_agent.py
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/devaamirreza/atmos-ai-streamlit.git
cd atmos-ai-streamlit
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows CMD:

```cmd
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API credentials

Create a `.env` file in the project root.

Add your OpenRouter API key:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

You can obtain an API key from [OpenRouter](https://openrouter.ai/).

**Important:** Never commit your `.env` file or expose your API key publicly.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

## 🌍 Weather Data

Atmos AI uses the [Open-Meteo API](https://open-meteo.com/) for geocoding and current weather information.

## 🤖 AI Integration

The application integrates with AI models through OpenRouter using the OpenAI-compatible Python SDK.

The AI assistant can interpret user queries, invoke the weather tool when required, and generate conversational responses based on retrieved weather data.

## 🔮 Future Enhancements

- Multi-day weather forecasts
- Weather visualizations and trends
- Location-based weather detection
- Additional AI-powered weather insights
- Improved conversational capabilities

## 👨‍💻 Author

**MD Aamir Reza**

GitHub: [@devaamirreza](https://github.com/devaamirreza)

---

*Atmos AI – Making weather information more conversational.*