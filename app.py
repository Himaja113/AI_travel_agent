import streamlit as st
from ui.travel_form import get_user_input
from workflows.travel_graph import build_travel_graph
from utils.map_utils import create_map
from streamlit_folium import st_folium
import time
import re


def _escape_dollars_for_streamlit_markdown(text: str) -> str:
    """
    Streamlit's Markdown treats `$...$` as LaTeX math, which makes text italic and
    collapses spaces. Escape dollar signs so currency renders as normal text.
    """
    if not isinstance(text, str) or "$" not in text:
        return text

    # Replace unescaped $ with \$
    return re.sub(r"(?<!\\)\$", r"\\$", text)

# Page Config
st.set_page_config(
    page_title="VoyageAI | Premium Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@400;700&display=swap');

    :root {
        --primary: #3b82f6;
        --secondary: #6366f1;
        --bg-glass: rgba(15, 23, 42, 0.7);
        --border-glass: rgba(255, 255, 255, 0.1);
        --text-pale: #94a3b8;
    }

    /* Main Container Styling */
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a);
        color: #f8fafc;
    }

    body {
        font-family: 'Outfit', sans-serif;
    }

    /* Typography */
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(to right, #60a5fa, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        color: var(--text-pale);
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: var(--bg-glass);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--border-glass);
        padding: 2rem;
        border-radius: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 2rem;
    }

    /* Custom Button */
    .stButton>button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 16px;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        width: 100%;
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .stButton>button:hover {
        transform: scale(1.02) translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(59, 130, 246, 0.5);
    }

    /* Tab Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: rgba(255, 255, 255, 0.03);
        padding: 0.5rem;
        border-radius: 18px;
        margin-bottom: 2rem;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent;
        border-radius: 14px;
        color: var(--text-pale);
        font-weight: 600;
        padding: 0 24px;
        transition: all 0.3s ease;
        border: 1px solid transparent;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(59, 130, 246, 0.1) !important;
        color: var(--primary) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
    }

    /* Metric Styling */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--primary);
    }
    
    .status-msg {
        background: rgba(59, 130, 246, 0.1);
        border-left: 4px solid var(--primary);
        padding: 1rem;
        border-radius: 0 12px 12px 0;
        margin: 1rem 0;
    }

    /* Hide Streamlit components for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Main Application Flow
if not st.session_state.get('result'):
    # Hero Section
    st.markdown('<div style="text-align: center; padding-top: 4rem;">', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">VoyageAI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Experience the future of travel planning with our Multi-Agent AI system.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Feature Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="glass-card" style="text-align: center; height: 100%;">
            <h3>📍 Precision Routing</h3>
            <p style="color: #94a3b8;">Real-world road distances and travel times using Google Maps architecture.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="glass-card" style="text-align: center; height: 100%;">
            <h3>🤖 Agent Synergy</h3>
            <p style="color: #94a3b8;">Specialized agents for weather, attractions, and logistics working in high-frequency loops.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="glass-card" style="text-align: center; height: 100%;">
            <h3>Smart Budgeting</h3>
            <p style="color: #94a3b8;">Precise cost estimations and math verification to keep your journey within limits.</p>
        </div>
        """, unsafe_allow_html=True)

    # Main Form Area
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    user_data = get_user_input()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Sidebar only shown when we have a result (to allow re-planning)
    with st.sidebar:
        user_data = get_user_input()

if user_data["generate"]:
    with st.status("🛠️ **Assembling Your Perfect Journey**", expanded=True) as status:
        st.markdown('<div class="status-msg">📍 <b>Destination Specialist:</b> Curating world-class attractions...</div>', unsafe_allow_html=True)
        time.sleep(1)
        
        st.markdown('<div class="status-msg">🚀 <b>Parallel Gatherer:</b> Fetching weather, routes, and live APIs concurrently...</div>', unsafe_allow_html=True)
        time.sleep(1)
        
        st.markdown('<div class="status-msg">📅 <b>Experience Designer:</b> Finalizing interactive daily itinerary...</div>', unsafe_allow_html=True)
        
        graph = build_travel_graph()
        result = graph.invoke(user_data)
        
        st.markdown('<div class="status-msg">🧠 <b>Quality Assurance:</b> Critiquing plan for maximum feasibility...</div>', unsafe_allow_html=True)
        st.markdown('<div class="status-msg">🎟️ <b>Booking Concierge:</b> Retrieving live ticket portals...</div>', unsafe_allow_html=True)
        st.session_state.result = result
        status.update(label="✨ **Voyage Masterpiece Complete**", state="complete", expanded=False)

if st.session_state.get('result'):
    result = st.session_state.result
    
    st.markdown(f'<h2 style="margin-bottom: 2rem;">🌟 Trip to {result["destination"]}</h2>', unsafe_allow_html=True)
    
    # Dashboard Layout
    tab1, tab2, tab3, tab4 = st.tabs(["🗓️ Master Itinerary", "🗺️ Smart Routes", "🔬 Agent Critique", "🎟️ Bookings"])

    with tab1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(_escape_dollars_for_streamlit_markdown(result["itinerary"]))
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        m_col, d_col = st.columns([3, 1])
        with m_col:
            map_obj, total_distance = create_map(result["attractions"])
            if map_obj:
                st_folium(map_obj, width=None, height=600, use_container_width=True)
        with d_col:
            st.markdown('<div class="glass-card" style="padding: 1.5rem;">', unsafe_allow_html=True)
            st.metric("Total Expedition", f"{total_distance:.1f} km")
            st.metric("Optimization Loops", result.get("iterations", 0))
            if "feedback_summary" in result:
                st.markdown("---")
                st.markdown("**Core Optimizations:**")
                st.info(result['feedback_summary'])
            st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(_escape_dollars_for_streamlit_markdown(result["critique"]))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if result.get("booking_links"):
            st.markdown(result["booking_links"])
        else:
            st.info("No booking links requested or generated.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔄 Create New Exploration"):
        st.session_state.result = None
        st.rerun()

st.markdown("<br><br><p style='text-align: center; color: #475569; font-size: 0.8rem;'>Powered by LangGraph & Premium Agentic Orchestration</p>", unsafe_allow_html=True)



