from datetime import date

import streamlit as st


def _trip_stats(start: date, end: date, budget: float, travelers: int) -> tuple[str | None, str | None]:
    if end < start:
        return None, None
    nights = (end - start).days
    nights_label = f"{nights} night{'s' if nights != 1 else ''}"
    per = budget / max(travelers, 1)
    per_label = f"${per:,.0f} / person"
    return nights_label, per_label


def get_user_input(*, compact: bool = False) -> dict:
    """compact=True when rendered in sidebar after a trip exists."""
    pad = "0.75rem 0 1.25rem" if compact else "0 0 1.75rem"

    st.markdown(
        f"""
        <div style='text-align: left; padding: {pad};'>
            <span class="va-eyebrow" style="margin-bottom: 0.5rem;">Trip essentials</span>
            <h2 style="font-family: var(--font-display); font-size: 1.5rem; margin: 0 0 0.35rem;
                color: var(--on-surface); font-weight: 600;">Plan your route</h2>
            <p style="color: var(--on-surface-variant); font-size: 0.9rem; margin: 0;
                font-family: var(--font-ui);">Destinations, dates, and how you like to travel.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        departure_city = st.text_input(
            "Departure",
            placeholder="e.g. Delhi",
            key="dep_city",
        )
        start_date = st.date_input("Start date", key="s_date")
        budget = st.number_input("Total budget (USD)", min_value=100, step=100, value=2000, key="bgt")

    with col2:
        destination = st.text_input(
            "Destination",
            placeholder="e.g. Lisbon",
            key="dest_city",
        )
        end_date = st.date_input("End date", key="e_date")
        travelers = st.number_input("Travelers", min_value=1, step=1, value=1, key="travs")

    nights_l, per_l = _trip_stats(start_date, end_date, float(budget), int(travelers))
    if nights_l and per_l:
        st.markdown(
            f"""
            <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0.25rem 0 1rem;">
                <span style="font-family: var(--font-ui); font-size: 0.72rem; font-weight: 600;
                    letter-spacing: 0.06em; text-transform: uppercase; color: var(--secondary);
                    background: var(--secondary-dim); padding: 0.35rem 0.75rem; border-radius: 9999px;">{nights_l}</span>
                <span style="font-family: var(--font-ui); font-size: 0.72rem; font-weight: 600;
                    letter-spacing: 0.06em; text-transform: uppercase; color: var(--primary-container);
                    background: rgba(212, 165, 116, 0.12); padding: 0.35rem 0.75rem; border-radius: 9999px;">{per_l}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif end_date < start_date:
        st.caption("End date must be on or after the start date.")

    st.markdown('<div style="height: 1.25rem;"></div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        interests = st.multiselect(
            "Interests",
            ["food", "culture", "nature", "shopping", "nightlife", "history"],
            default=["culture", "food"],
            key="ints",
        )
    with col4:
        travel_mode = st.radio(
            "Travel mode",
            ["Any", "Flight", "Train", "Bus", "Metro/Cab"],
            horizontal=False,
            key="t_mode",
        )

    st.markdown('<div style="height: 0.5rem;"></div>', unsafe_allow_html=True)

    book_tickets = st.checkbox(
        "Include booking links (when the workflow provides them)",
        value=True,
        key="book_tix",
    )

    generate = st.button(
        "Generate itinerary",
        use_container_width=True,
        type="primary",
    )

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
        "generate": generate,
    }
