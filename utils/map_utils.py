import folium
from folium.plugins import AntPath
from tools.google_maps_tool import get_routing_data
import polyline

def create_map(attractions):
    if not attractions:
        return None, 0

    # Center map on first attraction
    first = attractions[0]

    m = folium.Map(
        location=[first["lat"], first["lng"]],
        zoom_start=12,
        tiles="CartoDB positron"  # clean English map
    )

    total_distance = 0

    for i, place in enumerate(attractions):
        lat = place["lat"]
        lng = place["lng"]

        # Add numbered marker with detailed popup
        popup_html = f"""
        <div style="font-family: 'Outfit', sans-serif; min-width: 150px;">
            <h4 style="margin: 0; color: #1e3a8a;">{i+1}. {place['name']}</h4>
            <p style="margin: 5px 0;">⭐ <b>{place.get('rating','N/A')}</b></p>
            <p style="margin: 0; font-size: 12px; color: #64748b;">{place.get('address', '')}</p>
        </div>
        """
        
        folium.Marker(
            location=[lat, lng],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=place["name"],
            icon=folium.Icon(color="cadetblue", icon="map-pin", prefix='fa')
        ).add_to(m)

        # Draw real routes between places
        if i > 0:
            prev = attractions[i - 1]
            origin = (prev["lat"], prev["lng"])
            dest = (lat, lng)

            route_data = get_routing_data(origin, dest)

            if route_data:
                distance = route_data["distance_km"]
                total_distance += distance
                
                # Decode polyline for real road route
                path_coords = polyline.decode(route_data["polyline"])
                
                AntPath(
                    locations=path_coords,
                    color="#3b82f6",
                    weight=5,
                    delay=1000,
                    dash_array=[1, 10],
                    pulse_color='#1d4ed8'
                ).add_to(m)

                # midpoint for distance label
                mid_point = path_coords[len(path_coords)//2]
                
                label_html = f"""
                <div style="
                    font-size:11px;
                    color:white;
                    font-weight:bold;
                    background:#1e40af;
                    padding:3px 6px;
                    border-radius:10px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                    white-space: nowrap;">
                    {distance:.1f} km ({route_data['duration_text']})
                </div>
                """
                
                folium.Marker(
                    location=mid_point,
                    icon=folium.DivIcon(html=label_html)
                ).add_to(m)
            else:
                # Fallback to straight line if API fails
                from geopy.distance import geodesic
                distance = geodesic(origin, dest).km
                total_distance += distance
                
                folium.PolyLine(
                    locations=[origin, dest],
                    color="gray",
                    weight=2,
                    dash_array='5, 5'
                ).add_to(m)

    return m, total_distance