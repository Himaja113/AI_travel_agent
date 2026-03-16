import streamlit as st
from ui.travel_form import get_user_input
from workflows.travel_graph import build_travel_graph
from utils.map_utils import create_map
from streamlit_folium import st_folium

st.title("🌍 AI Multi-Agent Travel Planner")

if "result" not in st.session_state:
    st.session_state.result = None

user_data = get_user_input()

if user_data["generate"]:

    graph = build_travel_graph()

    result = graph.invoke(user_data)

    st.session_state.result = result

if st.session_state.result:

    result = st.session_state.result

    st.subheader("📅 Your Travel Plan")
    st.write(result["itinerary"])

    st.subheader("🗺 Attractions Map")
    map_obj, total_distance = create_map(result["attractions"])

    st_folium(map_obj, width=700)

    st.info(f"Total travel distance: {total_distance:.2f} km")
# import streamlit as st

# from ui.travel_form import get_user_input
# from workflows.travel_graph import build_travel_graph
# from utils.map_utils import create_map
# from streamlit_folium import st_folium
# st.title("🌍 AI Multi-Agent Travel Planner")

# user_data = get_user_input()

# if user_data["generate"]:

#     graph = build_travel_graph()

#     result = graph.invoke(user_data)

#     st.subheader("📅 Your Travel Plan")

#     st.write(result["itinerary"])
#     st.subheader("🗺 Attractions Map")

#     map_obj = create_map(result["attractions"])

#     if map_obj:
#         st_folium(map_obj, width=700)
    

# import streamlit as st
# from ui.travel_form import get_user_input
# from agents.itinerary_agent import create_itinerary

# st.set_page_config(page_title="AI Travel Planner")

# st.title("🌍 AI Multi-Agent Travel Planner")

# user_data = get_user_input()

# if user_data["generate"]:

#     st.subheader("Generating itinerary...")

#     itinerary = create_itinerary(user_data)

#     st.subheader("📅 Your Travel Plan")

#     st.write(itinerary)