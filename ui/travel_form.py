import streamlit as st

def get_user_input():

    st.sidebar.header("Trip Details")

    departure_city = st.sidebar.text_input("Departure City")

    destination = st.sidebar.text_input("Destination")

    start_date = st.sidebar.date_input("Start Date")

    end_date = st.sidebar.date_input("End Date")

    budget = st.sidebar.number_input("Budget ($)", min_value=100)

    travelers = st.sidebar.number_input("Number of Travelers", min_value=1)

    interests = st.sidebar.multiselect(
        "Interests",
        ["food", "culture", "nature", "shopping", "nightlife", "history"]
    )

    generate = st.sidebar.button("Generate Travel Plan")

    return {
        "departure_city": departure_city,
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
        "budget": budget,
        "travelers": travelers,
        "interests": interests,
        "generate": generate
    }