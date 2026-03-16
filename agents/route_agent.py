from geopy.distance import geodesic


def optimize_route(attractions):

    if not attractions or len(attractions) <= 2:
        return attractions

    optimized = [attractions[0]]
    remaining = attractions[1:]

    while remaining:

        last = optimized[-1]

        nearest = min(
            remaining,
            key=lambda place: geodesic(
                (last["lat"], last["lng"]),
                (place["lat"], place["lng"])
            ).km
        )

        optimized.append(nearest)
        remaining.remove(nearest)

    return optimized


def route_agent(state):

    attractions = state["attractions"]

    optimized = optimize_route(attractions)

    state["attractions"] = optimized

    return state