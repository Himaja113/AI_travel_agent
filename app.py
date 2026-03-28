import html
import re

import streamlit as st
from streamlit_folium import st_folium

from ui.effects import UI_EFFECTS_CSS
from ui.fx_bridge import render_fx_bridge
from ui.home_motion import HOME_LANDING_MOTION_CSS
from ui.theme import NOMAD_EDITORIAL_CSS
from ui.travel_form import get_user_input
from utils.map_utils import create_map
from workflows.travel_graph import build_travel_graph


def _escape_dollars_for_streamlit_markdown(text: str) -> str:
    if not isinstance(text, str) or "$" not in text:
        return text
    return re.sub(r"(?<!\\)\$", r"\\$", text)


def _validate_trip(data: dict) -> list[str]:
    errs: list[str] = []
    if not (data.get("departure_city") or "").strip():
        errs.append("Please enter a departure city.")
    if not (data.get("destination") or "").strip():
        errs.append("Please enter a destination.")
    if data["end_date"] < data["start_date"]:
        errs.append("End date must be on or after the start date.")
    return errs


def _safe_filename_part(name: str) -> str:
    s = re.sub(r"[^\w\-]+", "-", (name or "trip").strip())
    return s.strip("-")[:48] or "trip"


def _normalize_feedback_display(text: str) -> str:
    """Insert breaks where models often drop spaces so text wraps and reads cleanly."""
    if not isinstance(text, str) or not text.strip():
        return text if isinstance(text, str) else ""
    s = text
    s = re.sub(r"\)(?=[A-Za-z(])", ") ", s)
    s = re.sub(r"(\d)(?=[A-Za-z(])", r"\1 ", s)
    s = re.sub(r"([A-Za-z])(?=\()", r"\1 ", s)
    s = re.sub(r",(?=[^\s\d])", ", ", s)
    return s


@st.cache_resource
def _travel_graph():
    return build_travel_graph()


st.set_page_config(
    page_title="VoyageAI | Travel Studio",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

has_result = bool(st.session_state.get("result"))

_style = NOMAD_EDITORIAL_CSS + UI_EFFECTS_CSS
if not has_result:
    _style += HOME_LANDING_MOTION_CSS
st.markdown(f"<style>{_style}</style>", unsafe_allow_html=True)

if not has_result:
    st.markdown(
        """
        <div class="va-home-parallax-root">
            <div class="va-home-mesh va-home-mesh--a" aria-hidden="true"></div>
            <div class="va-home-mesh va-home-mesh--b" aria-hidden="true"></div>
            <div class="va-home-mesh va-home-mesh--c" aria-hidden="true"></div>
            <div class="va-hero-wrap va-home-hero-float">
                <span class="va-eyebrow">Multi-agent orchestration</span>
                <h1 class="va-hero-title">VoyageAI</h1>
                <p class="va-hero-lede">
                    A concierge-style trip planner: routes, weather, attractions, and budget reasoning
                    orchestrated through LangGraph—editorial clarity, instrument-panel precision.
                </p>
            </div>
            <div class="va-bento-grid">
                <div class="va-bento">
                    <div class="va-bento-num">01 — Discover</div>
                    <h3>Grounded places</h3>
                    <p>Attractions and pacing informed by real geography—not generic listicles.</p>
                </div>
                <div class="va-bento">
                    <div class="va-bento-num">02 — Curate</div>
                    <h3>Agent synergy</h3>
                    <p>Weather, logistics, and experience agents refine the loop until the plan holds up.</p>
                </div>
                <div class="va-bento">
                    <div class="va-bento-num">03 — Explore</div>
                    <h3>Budget you can trust</h3>
                    <p>Cost estimates and sanity checks so the itinerary stays within what you set.</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        user_data = get_user_input(compact=False)
else:
    with st.sidebar:
        st.markdown(
            """
            <div style="padding: 0.5rem 0 1rem;">
                <span class="va-eyebrow">Replan</span>
                <p style="font-family: var(--font-ui); color: var(--on-surface-variant);
                    font-size: 0.85rem; margin: 0.5rem 0 0;">Adjust inputs and generate a fresh itinerary.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.container(border=True):
            user_data = get_user_input(compact=True)

if user_data["generate"]:
    errors = _validate_trip(user_data)
    if errors:
        for msg in errors:
            st.error(msg)
    else:
        with st.status("Curating your journey…", expanded=True) as status:
            st.markdown(
                """
                <div class="va-status-line">Destination & interests → specialist agents</div>
                <div class="va-status-line">Weather sync · route efficiency · day-by-day structure</div>
                <div class="va-status-line">Quality pass on feasibility and budget</div>
                """,
                unsafe_allow_html=True,
            )
            graph = _travel_graph()
            result = graph.invoke(user_data)
            st.session_state.result = result
            st.session_state._va_show_celebration = True
            status.update(label="Itinerary ready", state="complete", expanded=False)

if st.session_state.get("result"):
    result = st.session_state.result
    dest = result.get("destination", "Your trip")
    dest_safe = html.escape(str(dest))

    if st.session_state.pop("_va_show_celebration", False):
        st.markdown(
            """
            <div class="va-celebrate-layer" aria-hidden="true">
                <div class="va-celebrate-confetti">
                    <span></span><span></span><span></span>
                    <span></span><span></span><span></span>
                </div>
                <div class="va-celebrate-ring"></div>
                <span class="va-celebrate-check">✓</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="va-trip-header va-scroll-reveal" style="display: flex; flex-wrap: wrap; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
            <h2 style="margin: 0; font-family: var(--font-display); font-size: clamp(1.5rem, 3vw, 2rem);">
                {dest_safe}
            </h2>
            <span style="font-family: var(--font-ui); font-size: 0.7rem; font-weight: 700;
                letter-spacing: 0.1em; text-transform: uppercase; color: var(--secondary);
                border: 1px solid rgba(77, 220, 198, 0.25); padding: 0.35rem 0.85rem; border-radius: 9999px;">
                Trip studio
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    act1, act2 = st.columns(2)
    with act1:
        st.download_button(
            label="Download itinerary (.md)",
            data=_escape_dollars_for_streamlit_markdown(result.get("itinerary", "")),
            file_name=f"voyageai-{_safe_filename_part(dest)}.md",
            mime="text/markdown",
            use_container_width=True,
            type="secondary",
            key="download_itinerary_md",
        )
    with act2:
        if st.button("New trip", use_container_width=True, type="secondary", key="reset_new_trip"):
            st.session_state.result = None
            st.rerun()

    tab1, tab2, tab3 = st.tabs(["Itinerary", "Map & distance", "Agent critique"])

    with tab1:
        _it = _escape_dollars_for_streamlit_markdown(result["itinerary"])
        st.markdown(
            f'<div class="va-panel va-prose va-panel-aurora va-scroll-reveal">\n\n{_it}\n\n</div>',
            unsafe_allow_html=True,
        )

    with tab2:
        map_obj, total_distance = create_map(result["attractions"])
        if map_obj:
            st_folium(map_obj, width=None, height=580, use_container_width=True)
        else:
            st.warning("No map data available for these attractions.")

        with st.container(border=True):
            m1, m2 = st.columns(2)
            with m1:
                st.metric("Route distance", f"{total_distance:.1f} km")
            with m2:
                st.metric("Refinement loops", result.get("iterations", 0))
            if result.get("feedback_summary"):
                st.markdown(
                    '<p style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.08em;'
                    'color:var(--on-surface-variant);margin:1.25rem 0 0.5rem;">Highlights</p>',
                    unsafe_allow_html=True,
                )
                st.info(
                    _escape_dollars_for_streamlit_markdown(
                        _normalize_feedback_display(result["feedback_summary"])
                    )
                )

    with tab3:
        with st.expander("About this review", expanded=False):
            st.caption(
                "Automated critique of feasibility, pacing, and budget alignment—use alongside your own judgment."
            )
        _cr = _escape_dollars_for_streamlit_markdown(result["critique"])
        st.markdown(
            f'<div class="va-panel va-prose va-panel-aurora va-scroll-reveal">\n\n{_cr}\n\n</div>',
            unsafe_allow_html=True,
        )

st.markdown(
    "<br><p style='text-align:center;color:var(--on-surface-variant);font-size:0.75rem;"
    "font-family:var(--font-ui);opacity:0.85;'>LangGraph · Stitch design system · Nomad Editorial</p>",
    unsafe_allow_html=True,
)

render_fx_bridge(landing=not bool(st.session_state.get("result")))
