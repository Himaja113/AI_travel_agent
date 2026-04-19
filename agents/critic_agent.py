from utils.llm import generate_response

def critic_agent(state):

    prompt = f"""
You are a ruthless travel plan reviewer.

Evaluate the following itinerary against the 9 Pillars of Travel Logic.

### 🔎 RUTHLESS AUDIT LIST (The 9 Pillars):
1. **OUTBOUND & RETURN AUDIT**: Did Day 1 start with travel from {state["departure_city"]} to {state["destination"]}? Does the final day include the return journey back to {state["departure_city"]}? If either is missing, FAIL THE PLAN (Score 1).
2. **UNDER-UTILIZATION AUDIT**: Does any full day in {state["destination"]} contain only 1 attraction and stop at lunch? If they didn't plan 2-3 geographically grouped attractions to fully use the day, FAIL THE PLAN (Score 1).
3. **MIGRATING HOTEL AUDIT**: Did the transport lines name specific, changing hotels (e.g. "Hotel in Fort" then "Hotel in Powai")? It MUST use the abstract phrase "your central hotel" every morning. If the hotel migrates or forces a specific zip-code in the morning step, FAIL THE PLAN (Score 1).
4. **DUPLICATE ATTRACTION AUDIT**: Manually count attractions. Any duplicates? FAIL THE PLAN (Score 1).
5. **INTEREST / TIMING AUDIT**: Did they respect the arrival time? Did they label a monument/statue as "Adventure"? FAIL THE PLAN (Score 1).
6. **ZIG-ZAG & OPTIMAL PATH AUDIT**: Did they travel 25km (e.g., Suburbs to South Mumbai) just for lunch and return? Are attractions within the same day visited in a geographically illogical/inefficient sequence? Did they claim a "Walk" for a 25km gap? FAIL THE PLAN (Score 1).
7. **GHOST DAY AUDIT**: Did they pad empty days (e.g., "No attractions found") instead of jumping to Extensions immediately? FAIL THE PLAN (Score 1).
8. **EXTENSION SUGGESTIONS AUDIT**: Extensions MUST have two separate sections: "Single-City Extensions" AND "Multi-City Chained Routes". They MUST precisely state the travel time AND optimal stay (e.g. "~ 3 hours from Mumbai, optimal stay: 2 days") and list specific landmarks. Single-city suggestions must be in the SAME STATE for city visits. FAIL THE PLAN (Score 1) if either section is missing or improperly formatted.
9. **ECHO AUDIT**: Did they copy-paste my rules, meta-text, or placeholders (like "(Check Transit Data)", "Stop the plan here") into the output? FAIL THE PLAN (Score 1).
9. **MATH & FORMAT AUDIT**: 
   - Does the budget table sum up correctly?
   - Is the daily hotel cost a CONSTANT, flat rate (e.g., strictly 2000 every day, not 2000, 2500, 2800)?
   - Are there `### 🏨 Recommended Accommodation` suggestions at the end?
   - If any of these are missing/hallucinated, FAIL THE PLAN (Score 1).

If ALL rules are perfectly followed, Score 10. Otherwise, Score 1 and explain the exact failure. DO NOT give intermediate scores if a rule is broken.

Itinerary:
{state["itinerary"]}

Attractions Data:
{state["attractions"]}

Provide:
1. Feasibility score (0–10)
2. Actionable Feedback

Format:
Score: [number]
Feedback: [your actionable instructions]
"""

    critique = generate_response(prompt)
    
    state["critique"] = critique
    state["feedback_summary"] = critique

    return state