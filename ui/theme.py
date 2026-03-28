# Design tokens from Google Stitch — "Nomad Editorial" (VoyageAI dashboard concept).
# Project: projects/14304217635270814889

STITCH_PROJECT = "projects/14304217635270814889"

NOMAD_EDITORIAL_CSS = """
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Noto+Serif:ital,wght@0,400;0,600;0,700;1,400&display=swap');

    :root {
        --surface: #111319;
        --surface-low: #191c21;
        --surface-container: #1d2025;
        --surface-high: #272a30;
        --surface-highest: #32353b;
        --surface-lowest: #0b0e13;
        --surface-bright: #36393f;
        --on-surface: #e1e2ea;
        --on-surface-variant: #d4c4b7;
        --primary: #f2c08d;
        --primary-container: #d4a574;
        --on-primary: #472a03;
        --secondary: #4ddcc6;
        --secondary-dim: rgba(77, 220, 198, 0.14);
        --outline-ghost: rgba(80, 69, 59, 0.22);
        --glow-amber: rgba(255, 220, 188, 0.08);
        --radius-lg: 16px;
        --radius-pill: 9999px;
        --font-display: 'Noto Serif', Georgia, serif;
        --font-ui: 'Manrope', system-ui, sans-serif;
    }

    .stApp {
        font-family: var(--font-ui);
        color: var(--on-surface);
        background: var(--surface-lowest);
        background-image:
            radial-gradient(ellipse 120% 80% at 0% -20%, rgba(212, 165, 116, 0.12), transparent 50%),
            radial-gradient(ellipse 90% 60% at 100% 0%, rgba(77, 220, 198, 0.06), transparent 45%),
            linear-gradient(180deg, var(--surface-lowest) 0%, var(--surface) 40%, var(--surface-lowest) 100%);
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 20;
        opacity: 0.035;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
    }

    h1, h2, h3, h4 {
        font-family: var(--font-display) !important;
        font-weight: 600 !important;
        color: var(--on-surface) !important;
        letter-spacing: -0.02em;
    }

    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        font-family: var(--font-ui);
        color: var(--on-surface-variant);
    }

    /* --- Hero --- */
    .va-hero-wrap {
        text-align: left;
        max-width: 720px;
        margin: 0 auto 3rem;
        padding: 3rem 1rem 0;
    }

    @media (min-width: 900px) {
        .va-hero-wrap {
            padding-left: 8%;
            padding-right: 2rem;
        }
    }

    .va-eyebrow {
        display: inline-block;
        font-family: var(--font-ui);
        font-size: 0.6875rem;
        font-weight: 600;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--secondary);
        background: var(--secondary-dim);
        padding: 0.35rem 0.85rem;
        border-radius: var(--radius-pill);
        margin-bottom: 1.25rem;
    }

    .va-hero-title {
        font-family: var(--font-display);
        font-size: clamp(2.75rem, 6vw, 3.75rem);
        font-weight: 700;
        line-height: 1.08;
        margin: 0 0 1rem;
        background: linear-gradient(135deg, var(--on-surface) 0%, var(--primary) 55%, var(--secondary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .va-hero-lede {
        font-family: var(--font-ui);
        font-size: 1.125rem;
        line-height: 1.6;
        color: var(--on-surface-variant);
        max-width: 34rem;
        margin: 0;
    }

    /* --- Bento --- */
    .va-bento-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 1rem;
        margin-bottom: 2rem;
    }

    @media (min-width: 900px) {
        .va-bento-grid {
            grid-template-columns: 1fr 1fr 1.15fr;
            gap: 1.25rem;
        }
    }

    .va-bento {
        background: var(--surface-container);
        border-radius: var(--radius-lg);
        padding: 1.5rem 1.35rem;
        box-shadow:
            inset 0 1px 0 rgba(255, 220, 188, 0.06),
            0 24px 48px -12px rgba(0, 0, 0, 0.35),
            0 0 0 1px rgba(212, 165, 116, 0.06);
        transition: transform 0.35s ease, box-shadow 0.35s ease;
    }

    .va-bento:hover {
        box-shadow:
            inset 0 1px 0 rgba(255, 220, 188, 0.1),
            0 28px 56px -12px rgba(212, 165, 116, 0.12),
            0 0 0 1px rgba(77, 220, 198, 0.1);
    }

    .va-bento-num {
        font-family: var(--font-ui);
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        color: var(--primary-container);
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }

    .va-bento h3 {
        font-family: var(--font-display) !important;
        font-size: 1.25rem !important;
        margin: 0 0 0.5rem !important;
        color: var(--on-surface) !important;
    }

    .va-bento p {
        font-size: 0.9rem;
        line-height: 1.55;
        color: var(--on-surface-variant);
        margin: 0;
    }

    /* --- Panels (glass stack) --- */
    .va-panel {
        background: linear-gradient(145deg, rgba(39, 42, 48, 0.55), rgba(29, 32, 37, 0.85));
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border-radius: 20px;
        padding: 2rem 1.75rem;
        margin-bottom: 2rem;
        box-shadow:
            0 32px 64px -24px rgba(0, 0, 0, 0.45),
            inset 0 1px 0 rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(212, 165, 116, 0.08);
    }

    .va-panel-tight {
        padding: 1.35rem 1.25rem;
    }

    /* Bordered panels (map meta + metrics + highlights): full-width friendly */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(145deg, rgba(39, 42, 48, 0.55), rgba(29, 32, 37, 0.85)) !important;
        border-radius: 20px !important;
        border-color: rgba(212, 165, 116, 0.12) !important;
        padding: 1rem 1.25rem 1.35rem !important;
        margin-top: 1rem !important;
        min-width: 0;
        max-width: 100%;
        overflow-x: hidden;
    }

    [data-testid="stVerticalBlockBorderWrapper"] [data-testid="column"] {
        min-width: 0 !important;
    }

    /* Folium iframe: stretch to tab width */
    .stTabs [data-testid="stIFrame"] {
        width: 100% !important;
        max-width: 100% !important;
    }

    /* Flex columns must shrink so narrow sidebars wrap text instead of overflowing */
    .stTabs [data-testid="column"],
    .stTabs [data-testid="stHorizontalBlock"] {
        min-width: 0 !important;
    }

    /* Highlights (st.info): break LLM strings that omit spaces */
    [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stAlert"],
    [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stAlert"] p,
    [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stAlert"] span,
    [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"],
    [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"] p {
        overflow-wrap: anywhere;
        word-wrap: break-word;
        word-break: break-word;
        max-width: 100%;
    }

    /* Fallback if alert markup / test ids differ between Streamlit versions */
    .stTabs div[data-testid="stAlert"],
    .stTabs div[data-testid="stAlert"] p,
    .stTabs div[data-testid="stAlert"] span {
        overflow-wrap: anywhere !important;
        word-break: break-word !important;
        max-width: 100% !important;
    }

    /* --- Form chrome (Streamlit widgets) --- */
    .stTextInput label, .stDateInput label, .stNumberInput label,
    .stMultiSelect label, .stRadio > label, .stSelectbox label {
        font-family: var(--font-ui) !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        color: var(--on-surface-variant) !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .stTextInput input, .stNumberInput input,
    [data-baseweb="input"], [data-baseweb="textarea"] {
        font-family: var(--font-ui) !important;
        background: rgba(54, 57, 63, 0.4) !important;
        border: 1px solid var(--outline-ghost) !important;
        border-radius: 12px !important;
        color: var(--on-surface) !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }

    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: rgba(77, 220, 198, 0.45) !important;
        box-shadow: 0 0 0 3px rgba(77, 220, 198, 0.12) !important;
    }

    [data-baseweb="select"] > div {
        border-radius: 12px !important;
        border-color: var(--outline-ghost) !important;
        background: rgba(54, 57, 63, 0.4) !important;
    }

    /* Primary CTA — force dark label (Streamlit nests text; theme was washing it out) */
    .stButton > button[kind="primary"],
    .stButton > button[kind="primary"] *,
    .stButton > button[kind="primary"] p,
    .stButton > button[kind="primary"] span {
        font-family: var(--font-ui) !important;
        color: #1a0f08 !important;
        -webkit-text-fill-color: #1a0f08 !important;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #c9985a, #e8b87a) !important;
        border: none !important;
        border-radius: var(--radius-pill) !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.04em !important;
        text-transform: none !important;
        padding: 0.85rem 1.75rem !important;
        box-shadow:
            0 0 0 1px rgba(26, 15, 8, 0.12),
            0 20px 40px -12px rgba(212, 165, 116, 0.45) !important;
        transition: transform 0.25s ease, box-shadow 0.25s ease !important;
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow:
            0 0 0 1px rgba(26, 15, 8, 0.18),
            0 28px 48px -12px rgba(212, 165, 116, 0.5) !important;
    }

    .stButton > button[kind="secondary"],
    .stButton > button[kind="secondary"] *,
    .stButton > button[kind="secondary"] span,
    .stButton > button[kind="secondary"] p {
        font-family: var(--font-ui) !important;
        color: var(--on-surface) !important;
        -webkit-text-fill-color: var(--on-surface) !important;
    }

    .stButton > button[kind="secondary"] {
        background: var(--surface-high) !important;
        border: 1px solid rgba(77, 220, 198, 0.38) !important;
        border-radius: var(--radius-pill) !important;
        font-weight: 600 !important;
    }

    /* Tabs → pills */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.85rem;
        background: var(--surface-low);
        padding: 0.55rem 0.65rem;
        border-radius: var(--radius-pill);
        border: 1px solid rgba(212, 165, 116, 0.06);
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
    }

    .stTabs [data-baseweb="tab"] {
        height: auto;
        min-height: 44px;
        padding-left: 1.35rem !important;
        padding-right: 1.35rem !important;
        margin: 0 0.15rem !important;
        border-radius: var(--radius-pill) !important;
        color: var(--on-surface-variant) !important;
        font-family: var(--font-ui) !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        border: none !important;
        background: transparent !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(212, 165, 116, 0.2), rgba(77, 220, 198, 0.12)) !important;
        color: var(--on-surface) !important;
        box-shadow: inset 0 0 0 1px rgba(212, 165, 116, 0.25) !important;
    }

    /* Streamlit tab panel: a bit of air below the tab bar */
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 0.75rem;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: var(--font-display) !important;
        font-size: 1.65rem !important;
        color: var(--primary) !important;
    }

    [data-testid="stMetricLabel"] {
        font-family: var(--font-ui) !important;
        color: var(--on-surface-variant) !important;
        text-transform: uppercase;
        font-size: 0.65rem !important;
        letter-spacing: 0.08em !important;
    }

    /* Markdown prose (itinerary) */
    .va-prose {
        font-family: var(--font-ui);
    }

    .va-prose h1, .va-prose h2, .va-prose h3 {
        font-family: var(--font-display) !important;
        color: var(--on-surface) !important;
        margin-top: 1.5rem;
    }

    .va-prose h1:first-child, .va-prose h2:first-child {
        margin-top: 0;
    }

    .va-prose strong {
        color: var(--primary);
    }

    .va-prose ul, .va-prose ol {
        padding-left: 1.25rem;
    }

    /* Budget / markdown tables: balanced columns; cost column stays on one line */
    .va-prose table {
        width: 100%;
        max-width: 100%;
        table-layout: fixed;
        border-collapse: collapse;
        margin: 1rem 0;
        font-size: 0.9rem;
        line-height: 1.45;
    }

    .va-prose table th,
    .va-prose table td {
        padding: 0.65rem 0.85rem;
        vertical-align: top;
        border: 1px solid rgba(212, 165, 116, 0.15);
        overflow-wrap: anywhere;
        word-wrap: break-word;
        hyphens: auto;
    }

    .va-prose table thead th {
        font-family: var(--font-ui);
        font-weight: 700;
        font-size: 0.72rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--primary);
        background: rgba(212, 165, 116, 0.08);
    }

    .va-prose table tbody tr:nth-child(even) td {
        background: rgba(255, 255, 255, 0.02);
    }

    /* Column 1: category labels */
    .va-prose table th:nth-child(1),
    .va-prose table td:nth-child(1) {
        width: 20%;
        min-width: 7.5rem;
    }

    /* Column 2: details — majority of width */
    .va-prose table th:nth-child(2),
    .va-prose table td:nth-child(2) {
        width: 58%;
    }

    /* Column 3: currency — no mid-number breaks */
    .va-prose table th:nth-child(3),
    .va-prose table td:nth-child(3) {
        width: 22%;
        min-width: 5.5rem;
        white-space: nowrap;
        text-align: right;
        font-variant-numeric: tabular-nums;
        font-weight: 500;
    }

    .va-prose table tbody td:nth-child(3) {
        color: var(--on-surface);
    }

    /* If a table has fewer than 3 columns, don’t force last-col rules harmfully */
    .va-prose table th:only-child,
    .va-prose table td:only-child {
        width: auto !important;
        white-space: normal !important;
        text-align: left !important;
    }

    .va-panel.va-prose {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }

    /* Status + info */
    .va-status-line {
        font-family: var(--font-ui);
        font-size: 0.9rem;
        color: var(--on-surface-variant);
        padding: 0.65rem 0;
        border-bottom: 1px solid rgba(212, 165, 116, 0.08);
    }

    .va-status-line:last-child {
        border-bottom: none;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--surface-low) 0%, var(--surface-lowest) 100%);
        border-right: 1px solid rgba(212, 165, 116, 0.08);
    }

    [data-testid="stSidebar"] .va-panel {
        margin-top: 0.5rem;
    }

    div[data-testid="stExpander"] {
        background: var(--surface-container);
        border: 1px solid rgba(212, 165, 116, 0.08);
        border-radius: 14px;
    }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    @media (prefers-reduced-motion: reduce) {
        .va-bento, .stButton > button[kind="primary"] {
            transition: none !important;
        }
        .stButton > button[kind="primary"]:hover {
            transform: none !important;
        }
    }
"""
