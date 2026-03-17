# 🌍 VoyageAI: Multi-Agent Travel Planner

VoyageAI is a sophisticated travel orchestration system that uses multiple specialized AI agents to craft realistic, optimized, and feasible travel itineraries. Built with **LangGraph** and powered by **Groq**, it simulates a team of travel experts collaborating to build your perfect journey.

![VoyageAI Preview](https://img.shields.io/badge/AI-Multi--Agent-blueviolet?style=for-the-badge)
![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red?style=for-the-badge)

---

## ✨ Key Features

- **🤖 Multi-Agent Collaboration**: Features specialized agents for Attractions, Weather, Routing, and Itinerary Design.
- **🛣️ Precision Routing**: Uses **Google Maps Directions API** to calculate real-world road distances and travel times.
- **🌦️ Weather-Aware Planning**: Integrates **OpenWeather API** to suggest activities based on real-time forecasts.
- **🗺️ Interactive Road Maps**: Visualizes actual road paths (not just straight lines) using animated polylines.
- **🧠 Automated Critique & Refinement**: A "Critic" agent reviews every plan for feasibility, budget math, and travel logic, triggering a refinement loop if issues are found.
- **💎 Premium UI/UX**: A modern Glassmorphism interface with dark mode, interactive progress tracking, and a dashboard-style layout.
- **💰 Smart Budgeting**: Precise cost estimation with automatic arithmetic verification.

---

## 🛠️ Technology Stack

- **Orchestration**: [LangGraph](https://python.langchain.com/docs/langgraph/)
- **LLM Inference**: [Groq API](https://groq.com/) (Llama-3.1-8b-instant)
- **Frontend**: [Streamlit](https://streamlit.io/)
- **Geospatial Tools**: 
  - Google Places API (Attractions)
  - Google Maps Directions API (Routing)
  - Folium & Streamlit-Folium (Maps)
  - Geopy (Coordinates)
- **Weather**: OpenWeather API

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- API Keys for:
  - [Groq](https://console.groq.com/)
  - [Google Maps Platform](https://console.cloud.google.com/) (Places & Directions enabled)
  - [OpenWeatherMap](https://openweathermap.org/api)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Himaja113/AI_travel_agent.git
   cd AI_travel_agent
   ```

2. **Setup environment variables**:
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_key
   GOOGLE_PLACES_API_KEY=your_google_key
   WEATHER_API_KEY=your_weather_key
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

---

## 🧠 System Architecture

The workflow follows a directed acyclic graph (DAG) managed by LangGraph:

1. **Destinations**: Fetches top-rated attractions via Google Places.
2. **Weather**: Retrieves forecasts for the destination.
3. **Routing**: Optimizes the visit order using real-world road data (Nearest Neighbor).
4. **Itinerary**: Crafts a day-by-day plan using LLM reasoning.
5. **Critic**: Evaluates the plan against 5+ feasibility criteria.
6. **Refiner (Optional)**: If rejected, summarizes issues and loops back to Re-plan.

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

---
*Built with ❤️ by the VoyageAI Team*
