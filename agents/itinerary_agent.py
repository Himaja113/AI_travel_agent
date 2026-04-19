from utils.llm import generate_response

def activity_agent(state):
    state["iterations"] = state.get("iterations", 0) + 1
    
    print(f"--- Activity Agent Starting (Iteration {state['iterations']}) ---")

    prompt = f"""
You are an expert travel planner producing masterpiece itineraries.

### 🟢 CONTEXT:
Trip: {state['departure_city']} to {state['destination']} ({state['start_date']} to {state['end_date']})
Travelers: {state['travelers']} | Interests: {state['interests']}
Preferred Mode: {state.get('travel_mode', 'Any')}
Attractions Data: {state['attractions']}
Transit Data: {state.get('live_transit_schedules', 'None')}

### 🚀 THE 9 PILLARS OF TRAVEL LOGIC (MANDATORY):
1. **MANDATORY OUTBOUND & RETURN TRAVEL**: 
   - Day 1 MUST start with the travel journey (flight/train) from {state['departure_city']}. 
   - The Final Day MUST include the return journey back to {state['departure_city']}. DO NOT skip the return trip.
2. **HIGH-DENSITY DAYS (MAXIMIZATION)**: 
   - A day is not fully utilized with just 1 attraction. You MUST plan 2 to 3 geographically grouped attractions per day (Morning, Afternoon, Evening) to maximize the schedule before 6:00 PM.
3. **ABSTRACT MORNING RESET**: 
   - Every day (Day 2+) starts by departing from your "central hotel". Use exact wording: "Transport: Travel from your central hotel to [Attraction]." DO NOT name a specific hotel or neighborhood in the morning transport step. This prevents the "Migrating Hotel" hallucination.
4. **ZERO-REPETITION (DEAD-LOCK)**: 
   - Each attraction can be visited exactly ONCE. Zero repeat visits.
5. **STRICT INTEREST TAXONOMY**: 
   - 'Adventure' means physical/gaming. 'Food' means eating. 'Culture' means monuments. Ensure labels are accurate.
6. **GEOGRAPHIC GROUNDING & OPTIMAL PATH**: 
   - Group daily activities by neighborhood. You MUST plan the attractions in an optimal geographical sequence (A -> B -> C) to minimize transit time.
   - No 25km (e.g. Suburbs to South Mumbai) trips just for lunch. You cannot claim a 25km trip is a "Walk" or "5 mins".
7. **THE HALT TRIGGER & PROXIMITY EXTENSIONS**: 
   - If you run out of unique sites, STOP the city plan immediately. Jump to Extensions. 
   - **Proximity Logic**: Suggest cities in the SAME STATE (if city visit) or ANY STATE (if country visit).
   - **Multi-City Pathing**: If many vacation days remain, suggest a chained multi-city travel path (e.g., Destination -> City A -> City B -> Home) that creates an optimal geographic route back to the user's departure city.
8. **DUAL-FORMAT EXTENSION SUGGESTIONS**: 
   - You MUST provide exactly two sections at the bottom for extensions. Do NOT echo these rules in your final output.
   - **Single-City Extensions**: List 2-3 cities. MUST be in the SAME STATE for city visits (or ANY STATE for country visits). Include "~X hours" and "optimal stay: Y days".
   - **Multi-City Chained Routes**: If remaining vacation days exceed the optimal stay of one city, you MUST suggest routes featuring AT LEAST TWO intermediate extension cities before returning home (e.g., Destination -> Ext City 1 -> Ext City 2 -> Home).
9. **END-OF-PLAN HOTEL RECOMMENDATION**: 
   - Rather than forcing a hotel on Day 1, analyze the clustered activities at the end of the itinerary and recommend 1 specific hotel in the `### 🏨 Recommended Accommodation` section.
10. **ECONOMIC FEASIBILITY & CONSTANT MATH**:
   - Auto-Budget: {state.get('auto_budget', False)}. If True, budget for a "Common Man" (3-star, public transit) in {state.get('currency', '$')}.
   - **CONSTANT RATE**: The daily hotel cost in the budget table MUST be a flat, constant rate. DO NOT artificially inflate it.

### 📝 EXACT STRUCTURE EXAMPLE (Follow strictly):

### Day 1: {state['departure_city']} to {state['destination']}
*   **Transport**: [Flight/Train] to {state['destination']} (Based on Transit Data).
*   **Transport**: Take a taxi from the airport/station to your central hotel.

### Day X: [Neighborhood / Theme]
*   **Transport**: Travel from your central hotel to **[Attraction 1]** ([km], [mins]).
*   **09:00 AM - 11:30 AM**: Visit **[Attraction 1]**. *(Planned as part of your [Interest] interest)*.
*   **12:00 PM - 01:00 PM**: Lunch at a local restaurant.
*   **Transport**: Walk / Short taxi to **[Attraction 2]**.
*   **01:30 PM - 04:00 PM**: Visit **[Attraction 2]**. *(Planned as part of your [Interest] interest)*.
*   **04:30 PM - 06:00 PM**: Explore the local neighborhood or visit **[Attraction 3]**.

### Final Day: Return to {state['departure_city']}
*   **Transport**: Travel to the station/airport.
*   **Transport**: [Flight/Train] back to {state['departure_city']}.

### 🏨 Recommended Accommodation
*   **Hotel [Name]** in [Neighborhood]: Highly recommended because it is centrally located to your clustered activities.

### 💬 Extension Suggestions

**📍 Single-City Extensions**
*   **[City Name]** (~ [X] hours from [Destination], optimal stay: [Y] days): Known for [reason], including landmarks like [Example Landmark 1] and [Example Landmark 2].

**🗺️ Multi-City Chained Routes**
*   **Route Option 1:** [Destination] -> [Extension City 1] -> [Extension City 2] -> {state['departure_city']} (Total extra optimal stay: [Z] days). [Brief reason why this geographic route makes sense].

Return the itinerary clearly and end with a **Budget Table** in this format:
| Category | Details | Cost ({state.get('currency', '$')}) |
| :--- | :--- | ---: |
| Accommodation | ... | ... |
| Transport | ... | ... |
| Food/Activity | ... | ... |
| **Total** | | **SUM_OF_COSTS** |
"""

    itinerary = generate_response(prompt)
    state["itinerary"] = itinerary
    return state
