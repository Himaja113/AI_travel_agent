import streamlit as st

def get_user_input():
    st.markdown("""
        <div style='text-align: center; padding-bottom: 20px;'>
            <h2 style='color: #3b82f6; margin-bottom: 0;'>📝 Trip Essentials</h2>
            <p style='color: #64748b; font-size: 0.9rem;'>Where do you want to go?</p>
        </div>
    """, unsafe_allow_html=True)

    # Use columns for a more horizontal form in main area
    col1, col2 = st.columns(2)
    with col1:
        departure_city = st.text_input("Departure City", placeholder="e.g. Delhi", key="dep_city")
        start_date = st.date_input("Start Date", key="s_date")
        budget = st.number_input("Total Budget ($)", min_value=100, step=100, value=2000, key="bgt")
    
    with col2:
        destination = st.text_input("Destination City", placeholder="e.g. Tokyo", key="dest_city")
        end_date = st.date_input("End Date", key="e_date")
        travelers = st.number_input("Number of Travelers", min_value=1, step=1, value=1, key="travs")

    st.markdown("---")
    
    col3, col4 = st.columns(2)
    with col3:
        interests = st.multiselect(
            "Interests & Vibes",
            ["food", "culture", "nature", "shopping", "nightlife", "history"],
            default=["culture", "food"],
            key="ints"
        )
    with col4:
        travel_mode = st.radio(
            "Preferred Travel Mode",
            ["Any", "Flight", "Train", "Bus", "Metro/Cab"],
            horizontal=True,
            key="t_mode"
        )

    st.markdown("<br>", unsafe_allow_html=True)
    book_tickets = st.checkbox("🎟️ Include Booking Links?", value=True, help="We'll generate direct links to book your flights, trains, or buses.", key="book_tix")
    generate = st.button("✨ Generate My Masterpiece", use_container_width=True)

    return {
        "departure_city": departure_city,
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
        "budget": budget,
        "travelers": travelers,
        "interests": interests,
        "travel_mode": travel_mode,
        "book_tickets": book_tickets,
        "generate": generate
    }