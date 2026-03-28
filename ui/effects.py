# UI-only effects (Nomad Editorial): borders, buttons, tabs, celebration, focus, map glow, scroll-reveal hooks.

UI_EFFECTS_CSS = """
    /* --- Scroll reveal (needs html.va-js from fx bridge; no JS = fully visible) --- */
    html.va-js .va-scroll-reveal {
        opacity: 0;
        transform: translateY(26px);
        transition: opacity 0.6s cubic-bezier(0.22, 1, 0.36, 1),
                    transform 0.65s cubic-bezier(0.22, 1, 0.36, 1);
    }
    html.va-js .va-scroll-reveal.va-reveal--visible {
        opacity: 1;
        transform: none;
    }

    /* --- Cursor spotlight (injected above page bg, below widgets; pointer-events none) --- */
    #va-fx-spotlight {
        pointer-events: none !important;
        z-index: 9997 !important;
    }

    /* --- Rotating aurora border for prose panels + Streamlit bordered blocks --- */
    @property --va-border-angle {
        syntax: "<angle>";
        initial-value: 0deg;
        inherits: false;
    }

    .va-panel.va-prose.va-panel-aurora {
        position: relative;
        border: 2px solid transparent;
        background:
            linear-gradient(145deg, rgba(32, 35, 40, 0.96), rgba(24, 26, 31, 0.98)) padding-box,
            conic-gradient(
                from var(--va-border-angle),
                rgba(77, 220, 198, 0.45),
                rgba(212, 165, 116, 0.55),
                rgba(77, 220, 198, 0.25),
                rgba(242, 192, 141, 0.4),
                rgba(77, 220, 198, 0.45)
            ) border-box;
        animation: va-border-spin 7s linear infinite;
    }

    @keyframes va-border-spin {
        to { --va-border-angle: 360deg; }
    }

    /* Bordered containers (form / map meta): conic ring without @property fallback */
    [data-testid="stVerticalBlockBorderWrapper"].va-panel-aurora-border {
        position: relative;
        border: 2px solid transparent !important;
        background:
            linear-gradient(145deg, rgba(39, 42, 48, 0.92), rgba(29, 32, 37, 0.96)) padding-box,
            conic-gradient(
                from var(--va-border-angle),
                rgba(77, 220, 198, 0.35),
                rgba(212, 165, 116, 0.45),
                rgba(77, 220, 198, 0.2),
                rgba(212, 165, 116, 0.35)
            ) border-box !important;
        animation: va-border-spin 9s linear infinite;
    }

    /* --- Buttons: press + ripple flash --- */
    .stButton > button {
        position: relative;
        overflow: hidden;
    }

    .stButton > button::after {
        content: "";
        position: absolute;
        inset: 0;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.35) 0%, transparent 55%);
        opacity: 0;
        transform: scale(0.2);
        pointer-events: none;
    }

    .stButton > button:active::after {
        animation: va-btn-ripple 0.55s ease-out forwards;
    }

    .stButton > button:active {
        transform: scale(0.97) !important;
    }

    @keyframes va-btn-ripple {
        0% { opacity: 0.45; transform: scale(0.2); }
        100% { opacity: 0; transform: scale(2.2); }
    }

    /* --- Tab panels: light enter transition --- */
    .stTabs [data-baseweb="tab-panel"] {
        animation: va-tab-enter 0.38s ease-out;
    }

    @keyframes va-tab-enter {
        from {
            opacity: 0.35;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* --- Map iframe soft pulse --- */
    .stTabs [data-testid="stIFrame"] {
        border-radius: 14px !important;
        box-shadow:
            0 0 0 1px rgba(212, 165, 116, 0.12),
            0 12px 40px -12px rgba(0, 0, 0, 0.5);
        animation: va-map-pulse 4s ease-in-out infinite;
    }

    @keyframes va-map-pulse {
        0%, 100% {
            box-shadow:
                0 0 0 1px rgba(212, 165, 116, 0.12),
                0 12px 40px -12px rgba(0, 0, 0, 0.5);
        }
        50% {
            box-shadow:
                0 0 0 1px rgba(77, 220, 198, 0.22),
                0 18px 48px -8px rgba(77, 220, 198, 0.08);
        }
    }

    /* --- Success celebration overlay --- */
    .va-celebrate-layer {
        position: fixed;
        inset: 0;
        z-index: 99999;
        pointer-events: none;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: va-celebrate-fade 1.35s ease forwards;
    }

    @keyframes va-celebrate-fade {
        0% { opacity: 1; }
        75% { opacity: 1; }
        100% { opacity: 0; visibility: hidden; }
    }

    .va-celebrate-ring {
        position: absolute;
        width: min(120px, 22vw);
        height: min(120px, 22vw);
        border-radius: 50%;
        border: 3px solid rgba(77, 220, 198, 0.55);
        animation: va-celebrate-ring 0.9s cubic-bezier(0.22, 1, 0.36, 1) forwards;
        box-shadow: 0 0 40px rgba(212, 165, 116, 0.35);
    }

    @keyframes va-celebrate-ring {
        0% { transform: scale(0.2); opacity: 0; }
        40% { opacity: 1; }
        100% { transform: scale(4.5); opacity: 0; }
    }

    .va-celebrate-check {
        position: relative;
        z-index: 2;
        font-size: clamp(2.5rem, 8vw, 3.5rem);
        line-height: 1;
        color: var(--secondary, #4ddcc6);
        text-shadow: 0 0 28px rgba(77, 220, 198, 0.6);
        animation: va-celebrate-check 0.55s cubic-bezier(0.34, 1.56, 0.64, 1) 0.12s both;
    }

    @keyframes va-celebrate-check {
        from { transform: scale(0) rotate(-25deg); opacity: 0; }
        to { transform: scale(1) rotate(0deg); opacity: 1; }
    }

    .va-celebrate-confetti {
        position: absolute;
        inset: 0;
        overflow: hidden;
    }

    .va-celebrate-confetti span {
        position: absolute;
        width: 8px;
        height: 8px;
        border-radius: 2px;
        top: 50%;
        left: 50%;
        opacity: 0;
        animation: va-confetti 1s ease-out forwards;
    }

    .va-celebrate-confetti span:nth-child(1) { background: #4ddcc6; animation-delay: 0.05s; --dx: -120px; --dy: -80px; }
    .va-celebrate-confetti span:nth-child(2) { background: #d4a574; animation-delay: 0.08s; --dx: 100px; --dy: -90px; }
    .va-celebrate-confetti span:nth-child(3) { background: #f2c08d; animation-delay: 0.1s; --dx: -40px; --dy: -130px; }
    .va-celebrate-confetti span:nth-child(4) { background: #4ddcc6; animation-delay: 0.12s; --dx: 130px; --dy: -40px; }
    .va-celebrate-confetti span:nth-child(5) { background: #d4a574; animation-delay: 0.06s; --dx: -100px; --dy: 60px; }
    .va-celebrate-confetti span:nth-child(6) { background: #e1e2ea; animation-delay: 0.14s; --dx: 90px; --dy: 70px; }

    @keyframes va-confetti {
        0% { opacity: 1; transform: translate(-50%, -50%) scale(1) rotate(0deg); }
        100% { opacity: 0; transform: translate(calc(-50% + var(--dx, 0px)), calc(-50% + var(--dy, 0px))) scale(0.3) rotate(180deg); }
    }

    /* --- Staggered form columns (landing only; no va-js gate — avoids flash when bridge runs late) --- */
    body:has(.va-home-parallax-root) [data-testid="stMain"] [data-testid="column"] {
        animation: va-stagger-col 0.55s cubic-bezier(0.22, 1, 0.36, 1) backwards;
    }

    body:has(.va-home-parallax-root) [data-testid="stMain"] [data-testid="column"]:nth-child(1) {
        animation-delay: 0.06s;
    }

    body:has(.va-home-parallax-root) [data-testid="stMain"] [data-testid="column"]:nth-child(2) {
        animation-delay: 0.16s;
    }

    body:has(.va-home-parallax-root) [data-testid="stMain"] [data-testid="column"]:nth-child(3) {
        animation-delay: 0.26s;
    }

    @keyframes va-stagger-col {
        from {
            opacity: 0;
            transform: translateY(18px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* --- Focus rings (keyboard) --- */
    .stButton > button:focus-visible,
    .stTextInput input:focus-visible,
    .stNumberInput input:focus-visible,
    [data-baseweb="input"]:focus-visible,
    [data-baseweb="textarea"]:focus-visible,
    [data-baseweb="select"]:focus-within,
    div[data-testid="stDateInput"] input:focus-visible {
        outline: 2px solid rgba(77, 220, 198, 0.85) !important;
        outline-offset: 3px !important;
    }

    .stTabs [data-baseweb="tab"]:focus-visible {
        outline: 2px solid rgba(212, 165, 116, 0.9) !important;
        outline-offset: 3px !important;
    }

    @media (prefers-reduced-motion: reduce) {
        body:has(.va-home-parallax-root) [data-testid="stMain"] [data-testid="column"] {
            animation: none !important;
        }

        html.va-js .va-scroll-reveal {
            opacity: 1 !important;
            transform: none !important;
            transition: none !important;
        }
        .va-panel-aurora,
        [data-testid="stVerticalBlockBorderWrapper"].va-panel-aurora-border {
            animation: none !important;
        }
        .stTabs [data-baseweb="tab-panel"] {
            animation: none !important;
        }
        .stTabs [data-testid="stIFrame"] {
            animation: none !important;
        }
        .stButton > button::after {
            display: none !important;
        }
        .stButton > button:active {
            transform: none !important;
        }
        .va-celebrate-layer,
        .va-celebrate-ring,
        .va-celebrate-check,
        .va-celebrate-confetti span {
            animation: none !important;
            opacity: 0 !important;
        }
    }
"""
