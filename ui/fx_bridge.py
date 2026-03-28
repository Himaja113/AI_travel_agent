"""Injects parent-document effects (spotlight, magnetic primary CTA, scroll-reveal) via Streamlit HTML component."""

from __future__ import annotations

import streamlit.components.v1 as components


def render_fx_bridge(*, landing: bool) -> None:
    """Run once per page; `landing` enables dual-gradient cursor spotlight on parent document."""
    land = "true" if landing else "false"
    components.html(
        f"""
<div id="va-fx-boot" data-landing="{land}" style="height:1px;width:1px;opacity:0;overflow:hidden;"></div>
<script>
(function () {{
  const boot = window.document.getElementById("va-fx-boot");
  const landing = boot && boot.getAttribute("data-landing") === "true";
  const W = window.parent;
  let doc;
  try {{
    doc = W.document;
  }} catch (e) {{
    return;
  }}

  function cleanup() {{
    if (W._vaFxMouseMove) {{
      doc.removeEventListener("mousemove", W._vaFxMouseMove);
      W._vaFxMouseMove = null;
    }}
    const old = doc.getElementById("va-fx-spotlight");
    if (old) old.remove();
    if (W._vaFxMagnetRaf) {{
      cancelAnimationFrame(W._vaFxMagnetRaf);
      W._vaFxMagnetRaf = null;
    }}
    if (W._vaFxMagnetHandler) {{
      doc.removeEventListener("mousemove", W._vaFxMagnetHandler);
      W._vaFxMagnetHandler = null;
    }}
    (W._vaFxMagnetBtns || []).forEach(function (b) {{
      b.style.transform = "";
    }});
    W._vaFxMagnetBtns = [];
  }}

  cleanup();

  doc.documentElement.classList.add("va-js");

  if (landing) {{
    const spot = doc.createElement("div");
    spot.id = "va-fx-spotlight";
    spot.setAttribute("aria-hidden", "true");
    spot.style.cssText =
      "pointer-events:none;position:fixed;inset:0;z-index:9997;opacity:1;" +
      "background:" +
      "radial-gradient(520px 460px ellipse at var(--spx,70vw) var(--spy,20vh), rgba(212,165,116,0.2) 0%, transparent 58%)," +
      "radial-gradient(420px 360px ellipse at var(--spx2,12vw) var(--spy2,88vh), rgba(77,220,198,0.12) 0%, transparent 55%);" +
      "transition:opacity .2s ease";
    doc.body.appendChild(spot);
    W._vaFxMouseMove = function (e) {{
      const x = e.clientX;
      const y = e.clientY;
      spot.style.setProperty("--spx", x + "px");
      spot.style.setProperty("--spy", y + "px");
      spot.style.setProperty("--spx2", Math.round(x * 0.75 + 60) + "px");
      spot.style.setProperty("--spy2", Math.round(doc.documentElement.clientHeight - y * 0.55) + "px");
    }};
    doc.addEventListener("mousemove", W._vaFxMouseMove);
  }}

  function attachScrollReveal() {{
    if (W._vaFxIo) {{
      W._vaFxIo.disconnect();
      W._vaFxIo = null;
    }}
    W._vaFxIo = new IntersectionObserver(
      function (entries) {{
        entries.forEach(function (en) {{
          if (en.isIntersecting) {{
            en.target.classList.add("va-reveal--visible");
            en.target.setAttribute("data-va-revealed", "1");
            W._vaFxIo.unobserve(en.target);
          }}
        }});
      }},
      {{ root: null, rootMargin: "0px 0px -6% 0px", threshold: 0.07 }}
    );
    doc.querySelectorAll(".va-scroll-reveal").forEach(function (el) {{
      if (el.getAttribute("data-va-revealed") === "1") return;
      if (el.classList.contains("va-reveal--visible")) return;
      W._vaFxIo.observe(el);
    }});
  }}

  function tagTargets() {{
    doc.querySelectorAll('.stApp [data-testid="stVerticalBlockBorderWrapper"]').forEach(function (el) {{
      el.classList.add("va-scroll-reveal", "va-panel-aurora-border");
    }});
    doc.querySelectorAll(".stApp .va-trip-header").forEach(function (el) {{
      el.classList.add("va-scroll-reveal");
    }});
  }}

  function magnetTick() {{
    const btn = W._vaFxMagnetBtn;
    if (!btn || !W._vaFxMagnetTarget) {{
      W._vaFxMagnetRaf = null;
      return;
    }}
    const r = btn.getBoundingClientRect();
    const cx = r.left + r.width / 2;
    const cy = r.top + r.height / 2;
    const dx = (W._vaFxMagnetTarget.x - cx) / (r.width / 2);
    const dy = (W._vaFxMagnetTarget.y - cy) / (r.height / 2);
    const mx = Math.max(-1, Math.min(1, dx));
    const my = Math.max(-1, Math.min(1, dy));
    btn.style.transform = "translate(" + mx * 7 + "px," + my * 7 + "px) scale(1.015)";
    W._vaFxMagnetRaf = requestAnimationFrame(magnetTick);
  }}

  function setupMagnet() {{
    W._vaFxMagnetHandler = function (e) {{
      const btns = doc.querySelectorAll('.stApp button[kind="primary"]');
      let hit = null;
      btns.forEach(function (b) {{
        const r = b.getBoundingClientRect();
        if (e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom) {{
          hit = b;
        }}
      }});
      if (hit !== W._vaFxMagnetBtn) {{
        if (W._vaFxMagnetBtn) W._vaFxMagnetBtn.style.transform = "";
        W._vaFxMagnetBtn = hit;
        if (!W._vaFxMagnetRaf && hit) {{
          W._vaFxMagnetRaf = requestAnimationFrame(magnetTick);
        }}
      }}
      if (hit) {{
        W._vaFxMagnetTarget = {{ x: e.clientX, y: e.clientY }};
        if (!W._vaFxMagnetRaf) W._vaFxMagnetRaf = requestAnimationFrame(magnetTick);
      }} else {{
        W._vaFxMagnetTarget = null;
        if (W._vaFxMagnetRaf) {{
          cancelAnimationFrame(W._vaFxMagnetRaf);
          W._vaFxMagnetRaf = null;
        }}
      }}
    }};
    doc.addEventListener("mousemove", W._vaFxMagnetHandler);
  }}

  function run() {{
    tagTargets();
    attachScrollReveal();
  }}

  setupMagnet();
  run();
  setTimeout(run, 350);
  setTimeout(run, 900);
  setTimeout(run, 1800);
}})();
</script>
""",
        height=0,
        width=0,
    )
