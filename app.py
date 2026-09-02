import base64
import textwrap
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="Menteleven | Player Wellbeing Intelligence",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

VALID_PAGES = {"landing", "demo_login", "dashboard", "player_profile"}
route = st.query_params.get("page", "landing")
if route not in VALID_PAGES:
    route = "landing"
st.session_state.page = route

if "language" not in st.session_state:
    st.session_state.language = "TR — Türkçe"


def html(content):
    """Render HTML directly, without Markdown interpreting nested blocks as code."""
    st.html(textwrap.dedent(content))


def navigate(page):
    st.session_state.page = page
    st.query_params["page"] = page
    st.rerun()


def asset_data_uri(filename):
    path = Path(__file__).parent / "assets" / filename
    if not path.exists():
        return ""
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


HERO_IMAGE = asset_data_uri("hero-footballer.png")
PORTRAIT_SHEET = asset_data_uri("player-portraits.png")
HEATMAP_IMAGE = asset_data_uri("emotional-heatmap-base.png")


html(
    """
    <style>
    :root {
        --bg: #07111f;
        --surface: #0d1b2d;
        --surface-2: #12233a;
        --green: #39e58c;
        --purple: #9b6cff;
        --purple-2: #6f4be8;
        --cyan: #4cc9f0;
        --yellow: #f7c65b;
        --red: #ff6577;
        --text: #f5f7fb;
        --muted: #91a3b8;
        --border: rgba(255,255,255,.09);
    }

    .stApp {
        background:
            radial-gradient(circle at 50% -10%, rgba(155,108,255,.18), transparent 36%),
            radial-gradient(circle at 90% 25%, rgba(57,229,140,.08), transparent 28%),
            var(--bg);
        color: var(--text);
    }

    header[data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer { visibility: hidden; }
    .block-container { max-width: 1240px; padding-top: 1.25rem; padding-bottom: 3rem; }
    h1, h2, h3, p, span, label { font-family: Inter, Aptos, Arial, sans-serif; }
    h1, h2, h3 { color: var(--text); }
    p { color: var(--muted); }

    div[data-testid="stButton"] button {
        min-height: 46px;
        border-radius: 10px;
        border: 1px solid var(--purple);
        background: linear-gradient(135deg, var(--purple), var(--purple-2));
        color: #ffffff !important;
        font-weight: 750;
        box-shadow: 0 10px 28px rgba(111,75,232,.22);
    }

    div[data-testid="stButton"] button p,
    div[data-testid="stButton"] button span {
        color: #ffffff !important;
        font-weight: 750 !important;
    }

    div[data-testid="stButton"] button:hover {
        border-color: #b697ff;
        background: linear-gradient(135deg, #ad85ff, #805df0);
        color: #ffffff !important;
        transform: translateY(-1px);
    }

    div[data-testid="stSelectbox"] > div { border-radius: 10px; }

    .brand { display:flex; align-items:center; gap:11px; height:46px; }
    .brand-mark {
        width:35px; height:35px; display:grid; place-items:center;
        border-radius:10px; background:linear-gradient(145deg, var(--green), #18b96a);
        color:#07111f; font-weight:900; font-size:14px;
    }
    .brand-name { color:#fff; font-size:21px; font-weight:820; letter-spacing:-.5px; }
    .nav-links { color:#91a4ba; font-size:14px; padding-top:13px; text-align:center; white-space:nowrap; }

    .hero { text-align:center; padding:72px 0 34px; }
    .eyebrow {
        display:inline-flex; align-items:center; gap:8px; color:#c5adff;
        background:rgba(155,108,255,.1); border:1px solid rgba(155,108,255,.28);
        border-radius:999px; padding:7px 12px; font-size:12px; font-weight:780;
        letter-spacing:.55px; text-transform:uppercase;
    }
    .hero h1 {
        max-width:940px; margin:22px auto 18px; font-size:clamp(44px,6.3vw,78px);
        line-height:1.01; letter-spacing:-3.8px; font-weight:850;
    }
    .hero h1 .accent {
        background:linear-gradient(90deg, var(--green), #78efb0 40%, #b899ff 78%);
        -webkit-background-clip:text; background-clip:text; color:transparent;
    }
    .hero-copy { max-width:750px; margin:0 auto; font-size:18px; line-height:1.7; }
    .trust-row { display:flex; justify-content:center; flex-wrap:wrap; gap:9px; margin-top:18px; }
    .trust-chip {
        color:#a9b8ca; border:1px solid var(--border); background:rgba(255,255,255,.025);
        border-radius:999px; padding:7px 11px; font-size:12px;
    }

    .product-stage {
        position:relative; margin:24px auto 0; max-width:1100px; padding:18px;
        border:1px solid rgba(255,255,255,.12); border-radius:24px;
        background:linear-gradient(145deg, rgba(19,36,58,.97), rgba(9,23,39,.98));
        box-shadow:0 35px 100px rgba(0,0,0,.42);
        overflow:hidden;
    }
    .product-stage:before {
        content:""; position:absolute; width:320px; height:320px; left:35%; top:-210px;
        background:rgba(155,108,255,.3); filter:blur(90px); border-radius:50%;
    }
    .stage-top {
        position:relative; display:flex; justify-content:space-between; align-items:center;
        padding:2px 3px 15px; border-bottom:1px solid var(--border);
        color:#8fa1b7; font-size:11px; letter-spacing:.35px;
    }
    .live-dot { display:inline-block; width:7px; height:7px; border-radius:50%; background:var(--green); box-shadow:0 0 12px var(--green); margin-right:7px; }
    .stage-grid { position:relative; display:grid; grid-template-columns:1.25fr .75fr; gap:14px; margin-top:14px; }

    .visual-card { border:1px solid var(--border); border-radius:16px; background:#0a1727; overflow:hidden; }
    .card-head { display:flex; justify-content:space-between; align-items:center; padding:13px 15px; color:#e7edf5; font-size:12px; font-weight:700; }
    .card-head small { color:#8396ac; font-weight:500; }

    .hero-footballer {
        position:relative; min-height:390px;
        background:
            linear-gradient(90deg, rgba(5,14,25,.05), rgba(5,14,25,.08) 55%, rgba(5,14,25,.72)),
            url('__HERO_IMAGE__') center/cover;
        overflow:hidden;
    }
    .hero-caption {
        position:absolute; left:15px; bottom:15px; z-index:3; color:#fff; font-size:11px;
        padding:9px 11px; border-radius:10px; border:1px solid rgba(255,255,255,.13);
        background:rgba(6,15,26,.67); backdrop-filter:blur(10px);
    }
    .heatmap-photo {
        position:relative; min-height:390px;
        background:
            linear-gradient(0deg, rgba(5,14,25,.48), rgba(5,14,25,.04)),
            url('__HEATMAP_IMAGE__') center/cover;
        overflow:hidden;
    }
    .heatmap-photo:after {
        content:""; position:absolute; inset:0; opacity:.83; mix-blend-mode:screen;
        background:
            radial-gradient(circle at 53% 25%, rgba(255,30,60,.9) 0 4%, rgba(255,151,27,.65) 8%, rgba(255,238,76,.25) 14%, transparent 21%),
            radial-gradient(circle at 48% 52%, rgba(255,46,71,.92) 0 5%, rgba(255,153,35,.6) 10%, rgba(255,235,72,.22) 17%, transparent 25%),
            radial-gradient(circle at 62% 76%, rgba(255,61,79,.72) 0 3%, rgba(255,170,38,.48) 8%, transparent 18%),
            radial-gradient(circle at 31% 63%, rgba(57,229,140,.35) 0 4%, transparent 17%);
    }
    .heat-legend {
        position:absolute; z-index:3; left:15px; bottom:15px; display:flex; gap:7px; align-items:center;
        background:rgba(6,15,26,.8); border:1px solid var(--border); border-radius:999px;
        padding:7px 10px; color:#c7d2df; font-size:10px; backdrop-filter:blur(8px);
    }
    .legend-bar { width:90px; height:6px; border-radius:99px; background:linear-gradient(90deg, var(--green), #f7e75b, #ff9a29, #ff304f); }
    .signal-badge {
        position:absolute; z-index:3; right:15px; top:15px; background:rgba(8,18,31,.82);
        border:1px solid rgba(255,101,119,.35); border-radius:10px; padding:10px 12px;
        color:#fff; font-size:11px; backdrop-filter:blur(8px);
    }
    .signal-badge b { color:var(--red); font-size:17px; }

    .analysis-column { display:grid; gap:14px; }
    .radar-wrap { min-height:236px; padding:0 8px 6px; }
    .radar-svg { width:100%; height:210px; display:block; }
    .radar-grid { fill:none; stroke:rgba(255,255,255,.13); stroke-width:1; }
    .radar-axis { stroke:rgba(255,255,255,.1); stroke-width:1; }
    .radar-shape { fill:rgba(155,108,255,.3); stroke:#a77dff; stroke-width:2.2; }
    .radar-dot { fill:var(--green); stroke:#07111f; stroke-width:2; }
    .radar-label { fill:#91a3b8; font-size:9px; font-family:Arial,sans-serif; }

    .score-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:7px; padding:0 10px 10px; }
    .score { background:#102036; border:1px solid var(--border); border-radius:10px; padding:8px 9px; }
    .score span { display:block; color:#8194aa; font-size:7px; text-transform:uppercase; letter-spacing:.45px; white-space:nowrap; }
    .score b { display:block; color:#fff; font-size:17px; line-height:1.1; margin-top:4px; }
    .score.green b { color:var(--green); }
    .score.purple b { color:#b99cff; }
    .score.yellow b { color:#f7c65b; }
    .score.red b { color:#ff7b8a; }
    .score.cyan b { color:#4cc9f0; }

    .css-radar { position:relative; width:270px; height:222px; margin:0 auto; }
    .radar-hex {
        position:absolute; left:50%; top:50%; transform:translate(-50%,-50%);
        width:174px; height:164px; clip-path:polygon(50% 0,93% 25%,93% 75%,50% 100%,7% 75%,7% 25%);
        background:rgba(255,255,255,.14);
    }
    .radar-hex:after {
        content:""; position:absolute; inset:1.5px;
        clip-path:inherit; background:#0a1727;
    }
    .radar-hex.mid { transform:translate(-50%,-50%) scale(.69); }
    .radar-hex.inner { transform:translate(-50%,-50%) scale(.38); }
    .radar-fill {
        position:absolute; left:50%; top:50%; transform:translate(-50%,-50%);
        width:174px; height:164px;
        clip-path:polygon(50% 8%,86% 28%,80% 68%,50% 89%,17% 70%,25% 31%);
        background:linear-gradient(145deg,rgba(57,229,140,.5),rgba(155,108,255,.58));
        border:none; filter:drop-shadow(0 0 8px rgba(155,108,255,.28));
    }
    .radar-center { position:absolute; left:50%; top:50%; width:5px; height:5px; border-radius:50%; background:#fff; transform:translate(-50%,-50%); }
    .radar-label-css { position:absolute; color:#95a7bb; font-size:8px; font-weight:750; letter-spacing:.3px; }
    .rl-top { top:5px; left:50%; transform:translateX(-50%); }
    .rl-ur { top:52px; right:0; }
    .rl-lr { bottom:43px; right:5px; }
    .rl-bottom { bottom:1px; left:50%; transform:translateX(-50%); }
    .rl-ll { bottom:43px; left:0; }
    .rl-ul { top:52px; left:7px; }
    .alert {
        margin:0 12px 12px; border-left:3px solid var(--yellow); border-radius:9px;
        background:rgba(247,198,91,.07); color:#dbe4ee; padding:11px; font-size:11px; line-height:1.5;
    }

    .section { margin-top:86px; text-align:center; }
    .section h2 { max-width:760px; font-size:40px; letter-spacing:-1.7px; margin:12px auto 10px; }
    .section-copy { max-width:740px; line-height:1.7; margin:0 auto; }
    .visual-features { display:grid; grid-template-columns:repeat(3,1fr); gap:15px; margin-top:25px; }
    .feature-card {
        min-height:205px; border:1px solid var(--border); border-radius:17px; padding:22px;
        background:linear-gradient(145deg, rgba(255,255,255,.04), rgba(255,255,255,.015));
        text-align:left;
    }
    .feature-icon { width:46px; height:46px; display:grid; place-items:center; border-radius:12px; background:rgba(155,108,255,.13); border:1px solid rgba(155,108,255,.26); position:relative; overflow:hidden; }
    .heat-icon { display:grid; grid-template-columns:repeat(3,5px); gap:3px; }
    .heat-icon i { width:5px; height:5px; border-radius:50%; background:#39e58c; box-shadow:0 0 5px rgba(57,229,140,.4); }
    .heat-icon i:nth-child(2), .heat-icon i:nth-child(5), .heat-icon i:nth-child(6) { background:#f7c65b; }
    .heat-icon i:nth-child(4) { background:#ff6577; box-shadow:0 0 7px rgba(255,101,119,.65); }
    .mini-radar { width:25px; height:25px; position:relative; }
    .mini-radar:before { content:""; position:absolute; inset:1px; clip-path:polygon(50% 0,93% 25%,93% 75%,50% 100%,7% 75%,7% 25%); background:#8b68e8; }
    .mini-radar:after { content:""; position:absolute; inset:6px; clip-path:polygon(50% 0,93% 25%,93% 75%,50% 100%,7% 75%,7% 25%); background:#39e58c; opacity:.9; }
    .pitch-icon { width:28px; height:24px; border:1px solid rgba(255,255,255,.55); border-radius:3px; position:relative; }
    .pitch-icon:before { content:""; position:absolute; left:50%; top:0; bottom:0; width:1px; background:rgba(255,255,255,.4); }
    .pitch-icon:after { content:"•  •  •"; position:absolute; inset:3px 2px; color:#39e58c; font-size:9px; line-height:8px; letter-spacing:2px; }
    .feature-card h3 { font-size:18px; margin:18px 0 8px; }
    .feature-card p { font-size:14px; line-height:1.6; }
    .security-panel {
        margin-top:70px; border:1px solid rgba(155,108,255,.23); border-radius:20px; padding:32px;
        background:linear-gradient(120deg, rgba(155,108,255,.1), rgba(57,229,140,.045));
    }
    .pricing-section { margin-top:86px; text-align:center; }
    .pricing-section h2 { font-size:40px; letter-spacing:-1.7px; margin:12px auto 8px; }
    .pricing-section > p { max-width:680px; margin:0 auto; line-height:1.65; }
    .pricing-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:15px; margin-top:28px; text-align:left; align-items:stretch; }
    .price-card {
        position:relative; border:1px solid rgba(255,255,255,.1); border-radius:18px; padding:23px;
        background:linear-gradient(145deg,rgba(20,39,63,.78),rgba(10,24,41,.82));
        display:flex; flex-direction:column; min-height:390px;
    }
    .price-card.featured { border-color:rgba(155,108,255,.62); box-shadow:0 22px 60px rgba(111,75,232,.2); transform:translateY(-7px); }
    .popular-badge { position:absolute; right:18px; top:18px; color:#d5c5ff; background:rgba(155,108,255,.14); border:1px solid rgba(155,108,255,.35); border-radius:999px; padding:5px 8px; font-size:8px; font-weight:800; letter-spacing:.4px; }
    .plan-name { color:#fff; font-size:18px; font-weight:800; }
    .plan-desc { color:#8296ad; font-size:12px; line-height:1.55; min-height:38px; margin-top:6px; }
    .price { color:#fff; font-size:34px; font-weight:860; letter-spacing:-1.4px; margin:20px 0 3px; }
    .price small { color:#8fa1b7; font-size:11px; font-weight:500; letter-spacing:0; }
    .price-note { color:#73869b; font-size:9px; }
    .plan-line { height:1px; background:rgba(255,255,255,.08); margin:18px 0; }
    .feature-list { list-style:none; padding:0; margin:0; flex:1; }
    .feature-list li { position:relative; color:#aab8c8; font-size:12px; padding:7px 0 7px 20px; }
    .feature-list li:before { content:"✓"; position:absolute; left:0; color:#39e58c; font-weight:900; }
    .plan-button { margin-top:18px; border-radius:10px; padding:11px 12px; text-align:center; color:#fff; font-size:12px; font-weight:780; border:1px solid rgba(155,108,255,.38); background:rgba(155,108,255,.12); }
    .featured .plan-button { background:linear-gradient(135deg,#9b6cff,#6f4be8); border-color:#9b6cff; }
    .footer-note { margin-top:70px; border-top:1px solid var(--border); padding-top:25px; color:#73869b; font-size:12px; text-align:center; }

    div[data-testid="stMetric"] {
        background:linear-gradient(145deg, rgba(20,39,63,.78), rgba(11,26,44,.76));
        border:1px solid rgba(255,255,255,.1);
        border-radius:16px;
        padding:18px;
        box-shadow:0 16px 40px rgba(0,0,0,.18);
        backdrop-filter:blur(16px);
    }
    div[data-testid="stMetric"] label { color:#8fa1b7 !important; }
    div[data-testid="stMetricValue"] { color:#fff; }
    .glass-card {
        border:1px solid rgba(255,255,255,.1);
        background:linear-gradient(145deg, rgba(20,39,63,.79), rgba(10,24,41,.76));
        border-radius:18px; padding:18px; box-shadow:0 20px 55px rgba(0,0,0,.2);
        backdrop-filter:blur(16px);
    }
    .glass-title { display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; }
    .glass-title b { color:#eef3f9; font-size:14px; }
    .glass-title span { color:#8296ad; font-size:10px; }
    .analytics-grid { display:grid; grid-template-columns:1.12fr .88fr; gap:15px; margin:20px 0 18px; }
    .trend-svg { width:100%; height:255px; display:block; }
    .gridline { stroke:rgba(255,255,255,.08); stroke-width:1; }
    .trend-purple { fill:none; stroke:#9b6cff; stroke-width:3; stroke-linecap:round; stroke-linejoin:round; }
    .trend-green { fill:none; stroke:#39e58c; stroke-width:3; stroke-linecap:round; stroke-linejoin:round; }
    .area-purple { fill:url(#purpleArea); }
    .chart-label { fill:#8296ad; font:9px Arial,sans-serif; }
    .chart-legend { display:flex; gap:14px; color:#91a3b8; font-size:10px; margin-top:-8px; }
    .legend-dot { display:inline-block; width:7px; height:7px; border-radius:50%; margin-right:5px; }
    .player-strip { display:flex; gap:12px; align-items:center; }
    .avatar {
        width:43px; height:43px; display:grid; place-items:center; border-radius:12px;
        background:linear-gradient(145deg, rgba(155,108,255,.25), rgba(57,229,140,.12));
        border:1px solid rgba(155,108,255,.3); color:#fff; font-weight:800;
    }
    .player-info b { color:#fff; display:block; font-size:13px; }
    .player-info span { color:#8194aa; font-size:10px; }
    .status-pill { display:inline-block; border-radius:999px; padding:5px 8px; font-size:9px; font-weight:750; }
    .status-pill.good { color:#56efa0; background:rgba(57,229,140,.09); }
    .status-pill.watch { color:#ffd46f; background:rgba(247,198,91,.1); }
    .profile-head {
        display:grid; grid-template-columns:150px 1fr; gap:22px; align-items:center;
        border:1px solid rgba(255,255,255,.1); border-radius:20px; padding:20px;
        background:linear-gradient(130deg, rgba(155,108,255,.13), rgba(15,33,54,.75));
    }
    .profile-photo {
        width:150px; height:170px; border-radius:15px; background:
        url('__PORTRAIT_SHEET__') left center/500% 100% no-repeat;
    }
    .portrait-0 { background-position:0% center; }
    .portrait-1 { background-position:25% center; }
    .portrait-2 { background-position:50% center; }
    .portrait-3 { background-position:75% center; }
    .portrait-4 { background-position:100% center; }
    .profile-name { color:#fff; font-size:32px; font-weight:830; letter-spacing:-1px; }
    .profile-meta { color:#91a3b8; font-size:13px; margin-top:6px; }
    .profile-number { color:#a984ff; font-size:54px; font-weight:900; float:right; line-height:1; }
    .profile-grid { display:grid; grid-template-columns:.92fr 1.08fr; gap:15px; margin-top:17px; }

    @media (max-width:900px) {
        .analytics-grid, .profile-grid { grid-template-columns:1fr; }
        .profile-head { grid-template-columns:1fr; }
    }

    @media (max-width:900px) {
        .nav-links { display:none; }
        .stage-grid { grid-template-columns:1fr; }
        .visual-features, .pricing-grid { grid-template-columns:1fr; }
        .price-card.featured { transform:none; }
        .hero { padding-top:42px; }
        .hero h1 { letter-spacing:-2px; }
    }
    </style>
    """.replace("__HERO_IMAGE__", HERO_IMAGE)
       .replace("__HEATMAP_IMAGE__", HEATMAP_IMAGE)
       .replace("__PORTRAIT_SHEET__", PORTRAIT_SHEET)
)


def brand():
    html(
        """
        <div class="brand">
            <div class="brand-mark">M11</div>
            <div class="brand-name">Menteleven</div>
        </div>
        """
    )


def show_landing_page():
    logo_col, nav_col, language_col, button_col = st.columns(
        [1.3, 2.8, 1.25, 1.15], vertical_alignment="center"
    )
    with logo_col:
        brand()
    with nav_col:
        html('<div class="nav-links">Ürün &nbsp;&nbsp; Nasıl Çalışır &nbsp;&nbsp; Analizler &nbsp;&nbsp; Güvenlik</div>')
    with language_col:
        languages = [
            "TR — Türkçe",
            "EN — English",
            "ES — Español",
            "IT — Italiano",
            "FR — Français",
        ]
        selected = st.selectbox(
            "Dil",
            languages,
            index=languages.index(st.session_state.language),
            label_visibility="collapsed",
        )
        st.session_state.language = selected
    with button_col:
        if st.button("Canlı Demo", key="header_demo", use_container_width=True):
            navigate("demo_login")

    if st.session_state.language != "TR — Türkçe":
        st.info("Seçtiğiniz dil demo sürümünde yakında aktif olacaktır. İçerik şimdilik Türkçedir.")

    html(
        """
        <section class="hero">
            <div class="eyebrow">⚽ Futbolcu Wellbeing Intelligence</div>
            <h1>Oyuncuyu performansın <span class="accent">ötesinde anlayın.</span></h1>
            <p class="hero-copy">
                Menteleven; oyuncu bildirimlerini, aktivite verilerini ve uzman gözlemlerini
                birleştirerek takımınız için erken wellbeing sinyalleri oluşturur.
            </p>
        </section>
        """
    )

    left, cta, secondary, right = st.columns([1.5, 1.15, 1.25, 1.5])
    with cta:
        if st.button("Canlı Demoyu İncele →", key="hero_demo", use_container_width=True):
            navigate("demo_login")
    with secondary:
        html('<div style="color:#9aacbf;font-size:12px;text-align:left;padding:14px 0 0 5px;">Kurgusal verilerle çalışan demo</div>')

    html(
        """
        <div class="trust-row">
            <div class="trust-chip">Yüz tanıma kullanılmaz</div>
            <div class="trust-chip">Psikolojik teşhis değildir</div>
            <div class="trust-chip">Uzman denetimli</div>
        </div>

        <div class="product-stage">
            <div class="stage-top">
                <span><span class="live-dot"></span> OYUNCU ANALİZ MERKEZİ</span>
                <span>DEMO FC · ANTRENMAN GÜNÜ · 09:30</span>
            </div>

            <div class="stage-grid">
                <div class="visual-card">
                    <div class="card-head">
                        <span>Maç İçi Mücadele · Oyuncu Bağlamı</span>
                        <small>Kırmızı-Beyaz Takım</small>
                    </div>
                    <div class="hero-footballer">
                        <div class="hero-caption">Maç içi mücadele · 78. dakika</div>
                    </div>
                </div>

                <div class="analysis-column">
                    <div class="visual-card">
                        <div class="card-head">
                            <span>Oyuncu Wellbeing Profili</span>
                            <small>Son 7 gün</small>
                        </div>
                        <div class="radar-wrap">
                            <div class="css-radar" role="img" aria-label="Yorgunluk, stres, motivasyon, hazırlık, uyku ve enerji spider chart">
                                <div class="radar-hex"></div>
                                <div class="radar-hex mid"></div>
                                <div class="radar-hex inner"></div>
                                <div class="radar-fill"></div>
                                <div class="radar-center"></div>
                                <span class="radar-label-css rl-top">MOTİVASYON</span>
                                <span class="radar-label-css rl-ur">ENERJİ</span>
                                <span class="radar-label-css rl-lr">UYKU</span>
                                <span class="radar-label-css rl-bottom">HAZIRLIK</span>
                                <span class="radar-label-css rl-ll">YORGUNLUK</span>
                                <span class="radar-label-css rl-ul">STRES</span>
                            </div>
                        </div>
                        <div class="score-grid">
                            <div class="score green"><span>Motivasyon</span><b>82</b></div>
                            <div class="score cyan"><span>Enerji</span><b>76</b></div>
                            <div class="score purple"><span>Uyku</span><b>71</b></div>
                            <div class="score green"><span>Hazırlık</span><b>80</b></div>
                            <div class="score red"><span>Yorgunluk</span><b>44</b></div>
                            <div class="score yellow"><span>Stres</span><b>32</b></div>
                        </div>
                        <div class="alert"><b>Takip sinyali:</b> Son üç günde uyku ve enerji değerlerinde düşüş görüldü.</div>
                    </div>
                </div>
            </div>
        </div>

        <section class="section">
            <div class="eyebrow">TEK BİR KONTROL MERKEZİ</div>
            <h2>Futbolun içinden gelen, insan odaklı analiz deneyimi.</h2>
            <p class="section-copy">Oyuncu kartları, takım trendleri, görsel zaman çizelgesi ve uzman notları aynı futbol operasyonu diliyle sunulur.</p>
            <div class="visual-features">
                <div class="feature-card">
                    <div class="feature-icon"><div class="heat-icon"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div></div>
                    <h3>Isı haritalı görsel kayıt</h3>
                    <p>Antrenman ve maç görsellerini oyuncunun değerlendirme zaman çizelgesiyle ilişkilendirin.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon"><div class="mini-radar"></div></div>
                    <h3>Spider chart profilleri</h3>
                    <p>Motivasyon, enerji, uyku, stres ve hazırlık değerlerini tek bakışta karşılaştırın.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon"><div class="pitch-icon"></div></div>
                    <h3>Takım ve kadro görünümü</h3>
                    <p>Futbol menajerlik sistemlerini çağrıştıran kartlarla takımın genel durumunu yönetin.</p>
                </div>
            </div>
        </section>

        <section class="pricing-section">
            <div class="eyebrow">KULÜBÜNÜZE UYGUN PLAN</div>
            <h2>Sahanın dışında da takımınızı güçlendirin.</h2>
            <p>Amatör ve gelişmekte olan futbol kulüplerinin bütçesine uygun, aylık ve kulüp bazlı fiyatlandırma.</p>
            <div class="pricing-grid">
                <div class="price-card">
                    <div class="plan-name">Standart</div>
                    <div class="plan-desc">Temel wellbeing takibine başlamak isteyen amatör kulüpler için.</div>
                    <div class="price">990 TL <small>/ ay</small></div>
                    <div class="price-note">Kulüp başına · KDV hariç</div>
                    <div class="plan-line"></div>
                    <ul class="feature-list">
                        <li>30 oyuncuya kadar kullanım</li>
                        <li>Günlük kısa oyuncu anketleri</li>
                        <li>Temel takım dashboard'u</li>
                        <li>Oyuncu wellbeing skorları</li>
                        <li>2 ekip kullanıcısı</li>
                    </ul>
                    <div class="plan-button">Standart Planı İncele</div>
                </div>

                <div class="price-card featured">
                    <div class="popular-badge">EN ÇOK TERCİH EDİLEN</div>
                    <div class="plan-name">Profesyonel</div>
                    <div class="plan-desc">Daha ayrıntılı analiz ve uzman iş birliği isteyen kulüpler için.</div>
                    <div class="price">1.990 TL <small>/ ay</small></div>
                    <div class="price-note">Kulüp başına · KDV hariç</div>
                    <div class="plan-line"></div>
                    <ul class="feature-list">
                        <li>60 oyuncuya kadar kullanım</li>
                        <li>AI destekli değerlendirme özeti</li>
                        <li>Spider chart oyuncu profilleri</li>
                        <li>Görsel zaman çizelgesi ve ısı haritası</li>
                        <li>7 ekip kullanıcısı</li>
                        <li>PDF değerlendirme raporları</li>
                    </ul>
                    <div class="plan-button">Profesyonel Planı İncele</div>
                </div>

                <div class="price-card">
                    <div class="plan-name">Premium</div>
                    <div class="plan-desc">Akademi ve birden fazla takım yöneten kulüp yapıları için.</div>
                    <div class="price">3.490 TL <small>/ ay</small></div>
                    <div class="price-note">Kulüp başına · KDV hariç</div>
                    <div class="plan-line"></div>
                    <ul class="feature-list">
                        <li>150 oyuncuya kadar kullanım</li>
                        <li>A takım ve akademi yönetimi</li>
                        <li>Gelişmiş takım karşılaştırmaları</li>
                        <li>Özel rol ve erişim yetkileri</li>
                        <li>20 ekip kullanıcısı</li>
                        <li>Öncelikli destek ve onboarding</li>
                    </ul>
                    <div class="plan-button">Premium Planı İncele</div>
                </div>
            </div>
        </section>

        <div class="security-panel">
            <div class="eyebrow">GÜVENLİ VE İNSAN ODAKLI</div>
            <h2>Oyuncuyu etiketlemez, uzman ekibi destekler.</h2>
            <p>Menteleven yüz tanıma kullanmaz, fotoğraflardan psikolojik teşhis üretmez. Platform, oyuncunun kendi bildirimleri ile uzman gözlemlerini anlamlı bir zaman çizelgesinde birleştirir.</p>
        </div>
        <div class="footer-note">Menteleven · Futbol kulüpleri için oyuncu wellbeing platformu · Demo sürümü</div>
        """
    )


def show_demo_login():
    top_left, top_right = st.columns([4, 1])
    with top_left:
        brand()
    with top_right:
        if st.button("← Siteye Dön", use_container_width=True):
            navigate("landing")

    html('<div style="height:60px"></div><div style="text-align:center"><div class="eyebrow">CANLI ÜRÜN DEMOSU</div><h1>Demo Kulübüne Giriş</h1><p>Platformu farklı ekip rollerinden biriyle inceleyin.</p></div>')
    left, center, right = st.columns([1, 1.35, 1])
    with center:
        role = st.selectbox("Rolünüz", ["Teknik Direktör", "Spor Psikoloğu", "Performans Ekibi"])
        st.caption(f"{role} görünümüyle devam edeceksiniz. Tüm demo verileri kurgusaldır.")
        if st.button("Demo Hesabıyla Devam Et →", use_container_width=True):
            navigate("dashboard")


def show_dashboard():
    logo, title, back = st.columns([1.2, 2.8, 1], vertical_alignment="center")
    with logo:
        brand()
    with title:
        html('<div style="color:#8fa1b7;font-size:13px">DEMO FC · A TAKIM · ANTRENMAN GÜNÜ</div>')
    with back:
        if st.button("← Siteye Dön", use_container_width=True):
            navigate("landing")

    html('<div style="margin:24px 0 18px"><div class="eyebrow">KULÜP ANALİTİĞİ</div><h1 style="margin:12px 0 5px;font-size:36px">Takım Kontrol Merkezi</h1><p>2 Eylül · Son oyuncu değerlendirmesi bugün 09:30\'da tamamlandı.</p></div>')
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Toplam Oyuncu", "24")
    c2.metric("Takım Motivasyonu", "82", "+4")
    c3.metric("Ortalama Enerji", "76", "-2")
    c4.metric("Takip Edilmeli", "3", "+1", delta_color="inverse")

    html(
        """
        <div class="analytics-grid">
            <div class="glass-card">
                <div class="glass-title"><b>Son 7 Günlük Takım Trendi</b><span>MOTİVASYON · ENERJİ</span></div>
                <svg class="trend-svg" viewBox="0 0 600 260" aria-label="Takım trend grafiği">
                    <defs><linearGradient id="purpleArea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9b6cff" stop-opacity=".3"/><stop offset="1" stop-color="#9b6cff" stop-opacity="0"/></linearGradient></defs>
                    <line class="gridline" x1="45" y1="35" x2="570" y2="35"/><line class="gridline" x1="45" y1="90" x2="570" y2="90"/><line class="gridline" x1="45" y1="145" x2="570" y2="145"/><line class="gridline" x1="45" y1="200" x2="570" y2="200"/>
                    <path class="area-purple" d="M50 174 L135 160 L220 166 L305 130 L390 105 L475 90 L560 65 L560 215 L50 215 Z"/>
                    <polyline class="trend-purple" points="50,174 135,160 220,166 305,130 390,105 475,90 560,65"/>
                    <polyline class="trend-green" points="50,78 135,92 220,86 305,101 390,116 475,124 560,108"/>
                    <text class="chart-label" x="45" y="238">PZT</text><text class="chart-label" x="130" y="238">SAL</text><text class="chart-label" x="215" y="238">ÇAR</text><text class="chart-label" x="300" y="238">PER</text><text class="chart-label" x="385" y="238">CUM</text><text class="chart-label" x="470" y="238">CTS</text><text class="chart-label" x="550" y="238">PAZ</text>
                </svg>
                <div class="chart-legend"><span><i class="legend-dot" style="background:#9b6cff"></i>Motivasyon</span><span><i class="legend-dot" style="background:#39e58c"></i>Enerji</span></div>
            </div>
            <div class="glass-card">
                <div class="glass-title"><b>Takım Wellbeing Profili</b><span>BUGÜN</span></div>
                <svg class="radar-svg" viewBox="0 0 280 220" aria-label="Takım spider chart">
                    <polygon class="radar-grid" points="140,25 236,95 199,190 81,190 44,95"/><polygon class="radar-grid" points="140,50 212,102 184,172 96,172 68,102"/><polygon class="radar-grid" points="140,75 188,109 169,154 111,154 92,109"/>
                    <line class="radar-axis" x1="140" y1="110" x2="140" y2="25"/><line class="radar-axis" x1="140" y1="110" x2="236" y2="95"/><line class="radar-axis" x1="140" y1="110" x2="199" y2="190"/><line class="radar-axis" x1="140" y1="110" x2="81" y2="190"/><line class="radar-axis" x1="140" y1="110" x2="44" y2="95"/>
                    <polygon class="radar-shape" points="140,40 210,99 181,166 101,165 70,100"/>
                    <text class="radar-label" x="140" y="15" text-anchor="middle">MOTİVASYON</text><text class="radar-label" x="240" y="95">ENERJİ</text><text class="radar-label" x="201" y="207">UYKU</text><text class="radar-label" x="42" y="207">HAZIRLIK</text><text class="radar-label" x="5" y="95">STRES</text>
                </svg>
                <div class="alert"><b>3 oyuncu takip edilmeli.</b><br>Uyku ve enerji sinyallerinde takım ortalamasından sapma var.</div>
            </div>
        </div>
        """
    )

    html('<div style="margin:28px 0 12px"><h2 style="font-size:24px;margin:0">Oyuncular</h2><p style="margin:5px 0 0">Detaylı wellbeing profilini açmak için oyuncu adına tıklayın.</p></div>')
    players = [
        (0, "10", "Emre Demir", "10 Numara", 86, 76, 71, 80, 32, 44, "Dengeli"),
        (1, "8", "Arda Kaya", "Merkez Orta Saha", 78, 73, 75, 77, 42, 51, "Dengeli"),
        (2, "1", "Kerem Yılmaz", "Kaleci", 91, 88, 84, 89, 18, 29, "Dengeli"),
        (3, "9", "Mert Akın", "Santrafor", 64, 58, 55, 61, 72, 76, "Takip Edilmeli"),
        (4, "5", "Can Eren", "Stoper", 72, 68, 63, 69, 55, 66, "Takip Edilmeli"),
    ]
    for portrait_index, number, name, position, motivation, energy, sleep, readiness, stress, fatigue, status_text in players:
        info, score, status, action = st.columns([3.1, 1, 1.25, 1.15], vertical_alignment="center")
        with info:
            html(f'<div class="glass-card" style="padding:11px 13px;margin:4px 0"><div class="player-strip"><div class="avatar">{number}</div><div class="player-info"><b>{name}</b><span>{position}</span></div></div></div>')
        with score:
            st.metric("Motivasyon", motivation)
        with status:
            pill_class = "good" if status_text == "Dengeli" else "watch"
            html(f'<div style="padding-top:16px"><span class="status-pill {pill_class}">{status_text}</span></div>')
        with action:
            if st.button(f"{name} →", key=f"player_{number}", use_container_width=True):
                st.session_state.selected_player = {
                    "number": number,
                    "name": name,
                    "position": position,
                    "motivation": motivation,
                    "energy": energy,
                    "sleep": sleep,
                    "readiness": readiness,
                    "stress": stress,
                    "fatigue": fatigue,
                    "status": status_text,
                    "portrait_index": portrait_index,
                }
                st.query_params["player"] = str(portrait_index)
                navigate("player_profile")
    st.caption("Bu sonuçlar psikolojik veya tıbbi teşhis değildir; uzman karar sürecini destekler.")


def show_player_profile():
    player = st.session_state.get("selected_player", {
        "number": "10", "name": "Emre Demir", "position": "10 Numara",
        "motivation": 86, "energy": 76, "sleep": 71, "readiness": 80,
        "stress": 32, "fatigue": 44, "status": "Dengeli", "portrait_index": 0
    })
    logo, title, back = st.columns([1.2, 2.8, 1], vertical_alignment="center")
    with logo:
        brand()
    with title:
        html('<div style="color:#8fa1b7;font-size:13px">OYUNCU WELLBEING PROFİLİ</div>')
    with back:
        if st.button("← Dashboard", use_container_width=True):
            navigate("dashboard")

    html(f"""
    <div class="profile-head" style="margin-top:26px">
        <div class="profile-photo portrait-{player['portrait_index']}"></div>
        <div>
            <div class="profile-number">{player['number']}</div>
            <div class="eyebrow">{player['status']}</div>
            <div class="profile-name">{player['name']}</div>
            <div class="profile-meta">{player['position']} · Demo FC · Son değerlendirme bugün 09:30</div>
        </div>
    </div>
    """)

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Motivasyon", player["motivation"], "+4")
    c2.metric("Enerji", player["energy"], "-2")
    c3.metric("Uyku", player["sleep"], "-5")
    c4.metric("Hazırlık", player["readiness"], "+1")
    c5.metric("Stres", player["stress"], "-3")
    c6.metric("Yorgunluk", player["fatigue"], "+2", delta_color="inverse")

    html("""
    <div class="profile-grid">
        <div class="glass-card">
            <div class="glass-title"><b>Bireysel Spider Chart</b><span>SON 7 GÜN</span></div>
            <svg class="radar-svg" viewBox="0 0 280 220">
                <polygon class="radar-grid" points="140,25 214,67 214,153 140,195 66,153 66,67"/><polygon class="radar-grid" points="140,48 194,79 194,141 140,172 86,141 86,79"/><polygon class="radar-grid" points="140,72 174,91 174,129 140,148 106,129 106,91"/>
                <line class="radar-axis" x1="140" y1="110" x2="140" y2="25"/><line class="radar-axis" x1="140" y1="110" x2="214" y2="67"/><line class="radar-axis" x1="140" y1="110" x2="214" y2="153"/><line class="radar-axis" x1="140" y1="110" x2="140" y2="195"/><line class="radar-axis" x1="140" y1="110" x2="66" y2="153"/><line class="radar-axis" x1="140" y1="110" x2="66" y2="67"/>
                <polygon class="radar-shape" points="140,34 202,74 194,141 140,176 84,142 92,82"/>
                <text class="radar-label" x="140" y="14" text-anchor="middle">MOTİVASYON</text><text class="radar-label" x="218" y="62">ENERJİ</text><text class="radar-label" x="218" y="160">UYKU</text><text class="radar-label" x="140" y="211" text-anchor="middle">HAZIRLIK</text><text class="radar-label" x="18" y="160">YORGUNLUK</text><text class="radar-label" x="34" y="62">STRES</text>
            </svg>
        </div>
        <div class="glass-card">
            <div class="glass-title"><b>Öz-Bildirim İlişkili Duygusal Yük Haritası</b><span>BUGÜN</span></div>
            <div class="heatmap-photo" style="min-height:360px;border-radius:12px">
                <div class="signal-badge">Duygusal yük sinyali<br><b>Orta</b></div>
                <div class="heat-legend"><span>Düşük</span><span class="legend-bar"></span><span>Yüksek</span></div>
            </div>
        </div>
    </div>
    <div class="glass-card" style="margin-top:15px">
        <div class="glass-title"><b>AI Destekli Değerlendirme Özeti</b><span>UZMAN KONTROLÜ GEREKİR</span></div>
        <p style="line-height:1.7;margin:0">Oyuncunun motivasyonu dengeli seyrediyor. Son üç değerlendirmede uyku değerinde sınırlı düşüş gözlendi. Bu çıktı teşhis değildir; oyuncuyla kısa bir görüşme yapılması önerilir.</p>
    </div>
    """)


if st.session_state.page == "landing":
    show_landing_page()
elif st.session_state.page == "demo_login":
    show_demo_login()
elif st.session_state.page == "player_profile":
    show_player_profile()
else:
    show_dashboard()
