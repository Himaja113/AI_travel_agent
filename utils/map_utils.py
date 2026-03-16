import folium
from geopy.distance import geodesic


def create_map(attractions):

    if not attractions:
        return None

    first = attractions[0]

    m = folium.Map(
        location=[first["lat"], first["lng"]],
        zoom_start=13
    )

    total_distance = 0

    for i, place in enumerate(attractions):

        lat = place["lat"]
        lng = place["lng"]

        folium.Marker(
            location=[lat, lng],
            popup=f"{place['name']} ⭐ {place['rating']}",
            tooltip=place["name"]
        ).add_to(m)

        # Draw route and calculate distance
        if i > 0:

            prev = attractions[i - 1]

            prev_coords = (prev["lat"], prev["lng"])
            curr_coords = (lat, lng)

            distance = geodesic(prev_coords, curr_coords).km
            total_distance += distance

            # draw line between places
            folium.PolyLine(
                locations=[prev_coords, curr_coords],
                color="blue",
                weight=3
            ).add_to(m)

            # midpoint for distance label
            mid_lat = (prev["lat"] + lat) / 2
            mid_lng = (prev["lng"] + lng) / 2

            folium.Marker(
                location=[mid_lat, mid_lng],
                icon=folium.DivIcon(
                    html=f"""<div style="font-size: 12px; color:red;">
                             {distance:.2f} km
                             </div>"""
                )
            ).add_to(m)

    return m, total_distance