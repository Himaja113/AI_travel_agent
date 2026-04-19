from utils.llm import generate_response

def chat_agent(state, user_message=None):
    if not user_message:
        return state
        
    print("--- Conversational Chat Agent Starting ---")
    
    # --- DYNAMIC ATTRACTION FETCHING FOR MULTI-CITY ---
    city_extraction_prompt = f"Extract ALL destination cities the user wants to visit next based on this message: '{user_message}'. Return the cities as a comma-separated list (e.g., Pune, Ahmedabad, Udaipur). Do NOT include the home/departure city '{state.get('departure_city', '')}' unless they explicitly want to do activities there. If no new cities are detected, return NONE."
    cities_str = generate_response(city_extraction_prompt).strip().strip(".'\"")
    
    if cities_str and cities_str.upper() != "NONE":
        from tools.places_tool import get_attractions
        city_list = [c.strip() for c in cities_str.split(',')]
        for new_city in city_list:
            if len(new_city) < 3: continue
            print(f"Detected city extension request: {new_city}. Fetching fresh attractions...")
            new_attractions = get_attractions(new_city)
            if new_attractions:
                for attr in new_attractions:
                    attr["city"] = new_city
                
                if "attractions" not in state:
                    state["attractions"] = []    
                state["attractions"].extend(new_attractions)
    
    current_itinerary = state.get('itinerary', '')
    
    prompt = f"""
You are an expert AI Travel Agent maintaining a continuous conversation with the user.

Trip Base Details:
Departure City: {state.get('departure_city')}
Original Destination: {state.get('destination')}
Dates: {state.get('start_date')} to {state.get('end_date')} ({(state['end_date'] - state['start_date']).days + 1} days total)
Travelers: {state.get('travelers')} | Interests: {state.get('interests')}
Budget Rules: Currency {state.get('currency', '$')} | Auto-Calculate: {state.get('auto_budget', False)}
Live Attractions Data: {state.get('attractions', [])}

User's Latest Chat Request:
"{user_message}"

Current Itinerary State:
{current_itinerary}

### 🚀 STRICT REBUILD INSTRUCTIONS (THE 10 PILLARS):

1. **IMPLICIT VS EXPLICIT**: Look at the chat history and the user's latest request. **ONLY** optimize/re-order/append cities that the user has EXPLICITLY requested to visit. Do NOT modify previously established good days unnecessarily.
2. **SEQUENTIAL MULTI-CITY PATHING**: When the user requests a chained multi-city route, plot them SEQUENTIALLY (e.g., Mumbai Days 1-3, Pune Days 4-5, Ahmedabad Days 6-8). **NEVER return to the departure city midway through the trip.** 
3. **MANDATORY OUTBOUND & RETURN TRAVEL**: 
   - Day 1 MUST start with travel from {state.get('departure_city')}.
   - The **Final Day** ONLY must contain the return journey back to {state.get('departure_city')}. 
4. **HIGH-DENSITY DAYS**: Maximize the schedule (Morning, Afternoon, Evening) for any new days generated using the provided Attractions Data.
5. **ABSTRACT MORNING RESET**: Every day starts with "Transport: Travel from your central hotel to [Attraction]". DO NOT migrate or specify ZIP-codes/names for the hotel in the morning step.
6. **ZERO-REPETITION**: No repeating attractions.
7. **END-OF-PLAN HOTEL RECOMMENDATION**: Provide `### 🏨 Recommended Accommodation` at the end for the various cities visited.
8. **DUAL-FORMAT EXTENSION SUGGESTIONS**: Overwrite the old suggestions with a fresh split menu exactly as shown below:
    - **Single-City Extensions**: List 2-3 cities. MUST be in the SAME STATE for city visits (or ANY STATE for country visits). Include "~X hours" and "optimal stay: Y days".
    - **Multi-City Chained Routes**: If remaining vacation days exceed the optimal stay of one city, you MUST suggest routes featuring AT LEAST TWO intermediate extension cities before returning home (e.g., Destination -> Ext City 1 -> Ext City 2 -> Home).
9. **NO ECHOING**: DO NOT echo the instructional text in your final output. ONLY provide the clean headers and routes.
10. **ECONOMIC FEASIBILITY (STRICT)**: Re-calculate the ENTIRE budget table. 
   - EVERY SINGLE COLUMN must be filled with numbers. No empty boxes.
   - The daily hotel cost MUST be a Constant, Flat Rate (e.g., strictly 2000 per day). No arbitrarily inflating costs.

### 📝 EXACT STRUCTURE EXAMPLE (Follow strictly for Extensions):
### 💬 Extension Suggestions

**📍 Single-City Extensions**
*   **[City Name]** (~ [X] hours from [Destination], optimal stay: [Y] days): Known for [reason], including landmarks like [Example Landmark 1] and [Example Landmark 2].

**🗺️ Multi-City Chained Routes**
*   **Route Option 1:** [Destination] -> [Extension City 1] -> [Extension City 2] -> {state.get('departure_city')} (Total extra optimal stay: [Z] days). [Brief reason why this geographic route makes sense].

**Master Update**: RETURN ONLY the completely updated Master Itinerary. Merge your new optimization seamlessly into the structure. Do not output conversational filler.
"""
    updated_itinerary = generate_response(prompt)
    state["itinerary"] = updated_itinerary
    
    return state
