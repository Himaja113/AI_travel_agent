# Landing motion — Nomad Editorial; tuned for visibility inside Streamlit markdown containers.

HOME_LANDING_MOTION_CSS = """
    /* Unclip landing layers (Streamlit stacks overflow:hidden on ancestors) */
    [data-testid="block-container"]:has(.va-home-parallax-root),
    [data-testid="stVerticalBlock"]:has(.va-home-parallax-root),
    div[data-testid="stMarkdownContainer"]:has(.va-home-parallax-root) {
        overflow: visible !important;
    }

    div[data-testid="stMarkdownContainer"]:has(.va-home-parallax-root) {
        background: transparent !important;
    }

    .element-container:has(.va-home-parallax-root) {
        overflow: visible !important;
    }

    .va-home-parallax-root {
        position: relative;
        isolation: isolate;
        min-height: min(78vh, 820px);
        margin: -0.5rem -1rem 2rem;
        padding: 2rem 1.25rem 3rem;
        overflow: visible !important;
    }

    @media (min-width: 900px) {
        .va-home-parallax-root {
            margin-left: -2rem;
            margin-right: -2rem;
            padding-left: 2.5rem;
            padding-right: 2.5rem;
        }
    }

    .va-home-mesh {
        position: absolute;
        pointer-events: none;
        z-index: 0;
        border-radius: 50%;
        will-change: transform;
    }

    /* Strong amber wash — visibly moves */
    .va-home-mesh--a {
        width: min(95vw, 640px);
        height: min(95vw, 640px);
        top: -8%;
        right: -18%;
        filter: blur(48px);
        opacity: 0.95;
        background: radial-gradient(
            circle at 30% 30%,
            rgba(242, 192, 141, 0.55) 0%,
            rgba(212, 165, 116, 0.28) 38%,
            transparent 72%
        );
        animation: va-mesh-drift-a 16s ease-in-out infinite;
    }

    /* Teal counter-drift */
    .va-home-mesh--b {
        width: min(85vw, 520px);
        height: min(85vw, 520px);
        bottom: 8%;
        left: -22%;
        filter: blur(52px);
        opacity: 0.9;
        background: radial-gradient(
            circle at 55% 45%,
            rgba(77, 220, 198, 0.42) 0%,
            rgba(77, 220, 198, 0.12) 42%,
            transparent 70%
        );
        animation: va-mesh-drift-b 12s ease-in-out infinite;
    }

    /* Warm core pulse between hero and cards */
    .va-home-mesh--c {
        width: min(70vw, 480px);
        height: min(70vw, 480px);
        top: 28%;
        left: 50%;
        filter: blur(64px);
        opacity: 0.75;
        background: radial-gradient(
            circle,
            rgba(212, 165, 116, 0.35) 0%,
            rgba(139, 90, 43, 0.12) 50%,
            transparent 68%
        );
        transform: translate(-50%, -40%);
        animation: va-mesh-drift-c 20s ease-in-out infinite;
    }

    @keyframes va-mesh-drift-a {
        0%, 100% { transform: translate(0, 0) scale(1); }
        33% { transform: translate(-14%, 10%) scale(1.12); }
        66% { transform: translate(10%, -12%) scale(0.92); }
    }

    @keyframes va-mesh-drift-b {
        0%, 100% { transform: translate(0, 0) scale(1); }
        50% { transform: translate(18%, -14%) scale(1.15); }
    }

    @keyframes va-mesh-drift-c {
        0%, 100% { transform: translate(-50%, -40%) scale(1); }
        40% { transform: translate(-58%, -48%) scale(1.18); }
        70% { transform: translate(-42%, -32%) scale(0.88); }
    }

    .va-home-parallax-root .va-hero-wrap,
    .va-home-parallax-root .va-bento-grid {
        position: relative;
        z-index: 2;
    }

    /* Obvious hero motion */
    .va-home-hero-float {
        animation: va-hero-float 5.5s ease-in-out infinite;
        will-change: transform;
    }

    @keyframes va-hero-float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-18px); }
    }

    /* Shifting gradient on the wordmark */
    .va-home-parallax-root .va-hero-title {
        background-size: 220% 220% !important;
        animation: va-title-flow 9s ease-in-out infinite !important;
    }

    @keyframes va-title-flow {
        0%, 100% { background-position: 0% 40%; }
        50% { background-position: 100% 60%; }
    }

    .va-home-parallax-root .va-eyebrow {
        animation: va-eyebrow-pulse 3.5s ease-in-out infinite;
        border: 1px solid rgba(77, 220, 198, 0.35);
    }

    @keyframes va-eyebrow-pulse {
        0%, 100% {
            box-shadow: 0 0 0 0 rgba(77, 220, 198, 0);
            border-color: rgba(77, 220, 198, 0.25);
        }
        50% {
            box-shadow:
                0 0 32px 6px rgba(77, 220, 198, 0.35),
                0 0 80px 20px rgba(212, 165, 116, 0.18);
            border-color: rgba(77, 220, 198, 0.65);
        }
    }

    /* Big entrance, then continuous subtle float (separate delays per card) */
    .va-home-parallax-root .va-bento {
        opacity: 0;
        transform: translateY(56px) scale(0.94);
        transition: none !important;
    }

    .va-home-parallax-root .va-bento:nth-child(1) {
        animation:
            va-bento-enter 1s cubic-bezier(0.16, 1, 0.3, 1) 0s forwards,
            va-bento-breathe 4.5s ease-in-out 1s infinite;
    }
    .va-home-parallax-root .va-bento:nth-child(2) {
        animation:
            va-bento-enter 1s cubic-bezier(0.16, 1, 0.3, 1) 0.15s forwards,
            va-bento-breathe 4.5s ease-in-out 1.15s infinite;
    }
    .va-home-parallax-root .va-bento:nth-child(3) {
        animation:
            va-bento-enter 1s cubic-bezier(0.16, 1, 0.3, 1) 0.3s forwards,
            va-bento-breathe 4.5s ease-in-out 1.3s infinite;
    }

    @keyframes va-bento-enter {
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    @keyframes va-bento-breathe {
        0%, 100% { transform: translateY(0) scale(1); }
        50% { transform: translateY(-8px) scale(1.02); }
    }

    /* Film grain drift (no mix-blend — keeps amber/teal meshes vivid) */
    .va-home-parallax-root::before {
        content: "";
        position: absolute;
        inset: 0;
        z-index: 1;
        pointer-events: none;
        opacity: 0.1;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23g)'/%3E%3C/svg%3E");
        animation: va-grain-pan 22s linear infinite;
    }

    @keyframes va-grain-pan {
        0% { transform: translate(0, 0); }
        100% { transform: translate(-4%, -3%); }
    }

    @media (prefers-reduced-motion: reduce) {
        div[data-testid="stMarkdownContainer"]:has(.va-home-parallax-root) {
            overflow: auto !important;
        }
        .va-home-mesh,
        .va-home-parallax-root::before,
        .va-home-hero-float,
        .va-home-parallax-root .va-hero-title,
        .va-home-parallax-root .va-eyebrow,
        .va-home-parallax-root .va-bento {
            animation: none !important;
        }
        .va-home-parallax-root .va-bento {
            opacity: 1 !important;
            transform: none !important;
        }
    }
"""
