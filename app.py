import base64
import textwrap
from datetime import date, timedelta
from pathlib import Path

import streamlit as st
import numpy as np
import plotly.graph_objects as go


st.set_page_config(
    page_title="Menteleven | Player Wellbeing Intelligence",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "page" not in st.session_state:
    st.session_state.page = "landing"

if "language" not in st.session_state:
    st.session_state.language = "TR — Türkçe"


def html(content):
    """Render HTML directly, without Markdown interpreting nested blocks as code."""
    st.html(textwrap.dedent(content))


def navigate(page):
    st.session_state.page = page
    st.rerun()


def set_page(page):
    """Streamlit button callback: runs before the page rerenders."""
    st.session_state.page = page


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
BODY_MAP_IMAGE = asset_data_uri("scientific-body-map.png")

SURVEY = {
    "Stres": [
        "Bugünkü antrenman veya maç öncesinde kendimi baskı altında hissediyorum.",
        "Son günlerde saha içindeki hatalarımı gereğinden fazla düşünüyorum.",
        "Teknik ekibin beklentileri bende gerginlik yaratıyor.",
        "Takım içindeki rolüm konusunda endişe hissediyorum.",
        "Maç sırasında sakin kalmakta zorlanıyorum.",
        "Son günlerde zihnimi futboldan uzaklaştırmakta zorlanıyorum.",
        "Rekabet ve kadro seçimi üzerimde baskı oluşturuyor.",
        "Antrenman sonrasında zihinsel olarak rahatlayamıyorum.",
        "Performansımla ilgili düşünceler uykumu etkiliyor.",
        "Şu anda stresimi kontrol edebildiğimi hissediyorum.",
    ],
    "Motivasyon": [
        "Bugünkü antrenmana yüksek istekle katılıyorum.",
        "Takım hedefleri için ekstra çaba göstermeye hazırım.",
        "Kendimi geliştirme isteğim yüksek.",
        "Sahaya çıktığımda mücadele etme arzum güçlü.",
        "Teknik ekibin geri bildirimleri beni motive ediyor.",
        "Takımdaki rolüm bana anlamlı geliyor.",
        "Zorlu antrenmanlarda odağımı koruyabiliyorum.",
        "Yaklaşan maç için heyecan ve istek duyuyorum.",
        "Bireysel hedeflerime ulaşabileceğime inanıyorum.",
        "Bugün elimden gelenin en iyisini vermek istiyorum.",
    ],
    "Enerji": [
        "Sabah uyandığımda kendimi enerjik hissettim.",
        "Isınma sırasında vücudum hızlı şekilde hazırlandı.",
        "Antrenmanın tamamında enerji seviyemi koruyabiliyorum.",
        "Koşu ve sprintlerde kendimi canlı hissediyorum.",
        "Gün içinde ani enerji düşüşleri yaşamıyorum.",
        "Kaslarım hareketlere güçlü tepki veriyor.",
        "Zihinsel olarak uyanık ve odaklanmış hissediyorum.",
        "Antrenman sonuna kadar tempomu koruyabilirim.",
        "Beslenme ve sıvı tüketimim enerji seviyemi destekliyor.",
        "Bugün fiziksel olarak aktif olmaya hazırım.",
    ],
    "Yorgunluk": [
        "Kaslarımda belirgin bir ağırlık hissediyorum.",
        "Önceki antrenmanın yorgunluğunu hâlâ taşıyorum.",
        "Sprint ve yön değiştirmelerde normalden çabuk yoruluyorum.",
        "Antrenman sonrasında toparlanmam uzun sürüyor.",
        "Bacaklarımda güç kaybı hissediyorum.",
        "Zihinsel olarak tükenmiş hissediyorum.",
        "Günlük aktivitelerde normalden fazla yoruluyorum.",
        "Dinlenmeme rağmen yorgunluğum devam ediyor.",
        "Konsantrasyonumu sürdürmekte zorlanıyorum.",
        "Bugünkü yüklenmenin benim için fazla olabileceğini düşünüyorum.",
    ],
    "Uyku": [
        "Geçen gece yeterli süre uyudum.",
        "Uykuya kolayca geçebildim.",
        "Gece boyunca sık sık uyanmadım.",
        "Sabah dinlenmiş şekilde uyandım.",
        "Uyku düzenim son bir haftadır istikrarlı.",
        "Uyku öncesinde zihnimi rahatlatabildim.",
        "Kas ağrıları uykumu bozmadı.",
        "Uyandığımda tekrar uyuma ihtiyacı hissetmedim.",
        "Uyku kalitem antrenmana hazır olmamı destekliyor.",
        "Bugünkü uyku seviyemden memnunum.",
    ],
    "Hazırlık": [
        "Bugünkü antrenman veya maç için fiziksel olarak hazırım.",
        "Taktik görevlerimi net şekilde biliyorum.",
        "Zihinsel odağım saha içi görevlerime hazır.",
        "Vücudumda performansımı sınırlayacak bir ağrı hissetmiyorum.",
        "Takım arkadaşlarımla iletişim kurmaya hazırım.",
        "Maç temposuna uyum sağlayabileceğime inanıyorum.",
        "Karar verme hızımın iyi olduğunu hissediyorum.",
        "Isınma sonrasında kendimi tamamen hazır hissediyorum.",
        "Teknik ve fiziksel hedeflerimi biliyorum.",
        "Bugün yüksek performans gösterebileceğime inanıyorum.",
    ],
}

ANSWER_OPTIONS = [
    "1 · Kesinlikle katılmıyorum",
    "2 · Katılmıyorum",
    "3 · Kararsızım",
    "4 · Katılıyorum",
    "5 · Kesinlikle katılıyorum",
]


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
    .route-button {
        min-height:46px; display:flex; align-items:center; justify-content:center;
        border-radius:10px; padding:0 18px; text-decoration:none !important;
        color:#fff !important; font-size:13px; font-weight:780;
        border:1px solid #9b6cff;
        background:linear-gradient(135deg,#9b6cff,#6f4be8);
        box-shadow:0 10px 28px rgba(111,75,232,.22);
        transition:all .2s ease;
    }
    .route-button:hover { color:#fff !important; border-color:#b697ff; transform:translateY(-1px); }
    .route-button.secondary { background:rgba(155,108,255,.09); border-color:rgba(155,108,255,.35); box-shadow:none; }

    .brand { display:flex; align-items:center; gap:11px; height:46px; }
    .brand-mark {
        width:35px; height:35px; display:grid; place-items:center;
        border-radius:10px; background:linear-gradient(145deg, var(--green), #18b96a);
        color:#07111f; font-weight:900; font-size:14px;
    }
    .brand-name { color:#fff; font-size:21px; font-weight:820; letter-spacing:-.5px; }
    .nav-links { color:#91a4ba; font-size:14px; height:46px; display:flex; align-items:center; justify-content:center; gap:30px; white-space:nowrap; }
    .nav-links span { display:inline-block; }
    .lang-menu { position:relative; height:46px; display:flex; align-items:center; justify-content:center; }
    .lang-menu summary { list-style:none; cursor:pointer; display:flex; align-items:center; gap:8px; color:#d8e0ea; font-size:12px; font-weight:700; padding:8px 5px; user-select:none; }
    .lang-menu summary::-webkit-details-marker { display:none; }
    .globe-icon { width:16px; height:16px; border:1.4px solid #a8b6c7; border-radius:50%; display:inline-block; position:relative; }
    .globe-icon:before { content:""; position:absolute; left:3px; right:3px; top:-1px; bottom:-1px; border-left:1px solid #a8b6c7; border-right:1px solid #a8b6c7; border-radius:50%; }
    .globe-icon:after { content:""; position:absolute; left:1px; right:1px; top:7px; height:1px; background:#a8b6c7; }
    .lang-chevron { color:#7f91a7; font-size:12px; transition:transform .2s ease; }
    .lang-menu[open] .lang-chevron { transform:rotate(180deg); }
    .lang-options { position:absolute; z-index:40; top:43px; right:0; width:145px; padding:7px; border:1px solid rgba(255,255,255,.1); border-radius:12px; background:#101f33; box-shadow:0 18px 45px rgba(0,0,0,.35); }
    .lang-options div { color:#9fb0c2; padding:8px 9px; border-radius:7px; font-size:11px; }
    .lang-options div:first-child { color:#fff; background:rgba(155,108,255,.13); }
    .st-key-login_cta button { background:linear-gradient(135deg,#39e58c,#20bc6b) !important; border-color:#39e58c !important; color:#07111f !important; box-shadow:0 10px 26px rgba(57,229,140,.18) !important; }
    .st-key-login_cta button p, .st-key-login_cta button span { color:#07111f !important; }
    .st-key-login_cta button:hover { background:linear-gradient(135deg,#57ef9f,#2dce7b) !important; border-color:#57ef9f !important; }
    .st-key-signup_cta button { background:rgba(255,255,255,.025) !important; border-color:rgba(235,241,247,.55) !important; color:#f1f5f9 !important; box-shadow:none !important; }
    .st-key-signup_cta button p, .st-key-signup_cta button span { color:#f1f5f9 !important; }
    .st-key-signup_cta button:hover { background:rgba(255,255,255,.08) !important; border-color:#fff !important; }

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
    .auth-shell { max-width:500px; margin:40px auto 0; padding:28px; border:1px solid rgba(255,255,255,.1); border-radius:20px; background:linear-gradient(145deg,rgba(20,39,63,.82),rgba(10,24,41,.86)); box-shadow:0 28px 80px rgba(0,0,0,.28); }
    .auth-title { text-align:center; }
    .auth-title h1 { margin:12px 0 6px; font-size:32px; }
    .auth-title p { margin:0 0 20px; font-size:13px; }
    .auth-divider { display:flex; align-items:center; gap:12px; color:#71849a; font-size:10px; margin:17px 0; }
    .auth-divider:before,.auth-divider:after { content:""; height:1px; background:rgba(255,255,255,.09); flex:1; }
    .st-key-forgot_password button { background:transparent!important; border:0!important; box-shadow:none!important; color:#e6eaf0!important; padding:4px 0!important; justify-content:flex-start!important; }
    .st-key-forgot_password button:hover { color:#fff!important; text-decoration:underline!important; }
    .st-key-google_login button,.st-key-apple_login button { background:#f7f8fa!important; border:1px solid #d9dee7!important; color:#17131f!important; box-shadow:none!important; opacity:1!important; }
    div.st-key-google_login div[data-testid="stButton"] button p,div.st-key-google_login div[data-testid="stButton"] button span,div.st-key-apple_login div[data-testid="stButton"] button p,div.st-key-apple_login div[data-testid="stButton"] button span { color:#17131f!important; -webkit-text-fill-color:#17131f!important; opacity:1!important; }
    .st-key-google_login button:hover,.st-key-apple_login button:hover { background:#fff!important; border-color:#fff!important; }
    div.st-key-google_login div[data-testid="stButton"] button p:before { content:""; display:inline-block; width:18px; height:18px; margin-right:8px; vertical-align:-4px; background:center/contain no-repeat url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 18 18'%3E%3Cpath fill='%234285F4' d='M17.64 9.205c0-.638-.057-1.252-.164-1.841H9v3.481h4.844a4.14 4.14 0 01-1.797 2.715v2.258h2.909c1.702-1.567 2.684-3.875 2.684-6.613z'/%3E%3Cpath fill='%2334A853' d='M9 18c2.43 0 4.468-.806 5.956-2.182l-2.91-2.258c-.805.54-1.835.86-3.046.86-2.344 0-4.328-1.585-5.037-3.715H.956v2.333A9 9 0 009 18z'/%3E%3Cpath fill='%23FBBC05' d='M3.963 10.705A5.41 5.41 0 013.682 9c0-.592.102-1.168.281-1.705V4.962H.956A9 9 0 000 9c0 1.45.347 2.824.956 4.038l3.007-2.333z'/%3E%3Cpath fill='%23EA4335' d='M9 3.58c1.321 0 2.507.454 3.44 1.345l2.582-2.582C13.464.891 11.426 0 9 0A9 9 0 00.956 4.962l3.007 2.333C4.672 5.165 6.656 3.58 9 3.58z'/%3E%3C/svg%3E"); }
    div.st-key-apple_login div[data-testid="stButton"] button p:before { content:""; display:inline-block; width:19px; height:19px; margin-right:8px; vertical-align:-4px; background:center/contain no-repeat url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='%23000000' d='M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.21.07 2.05.66 2.76.71 1.06-.21 2.08-.82 3.21-.74 1.35.11 2.37.64 3.04 1.61-2.78 1.67-2.12 5.33.43 6.35-.51 1.34-1.17 2.67-1.44 3.04zM12.03 7.25C11.88 5.26 13.51 3.62 15.37 3.46c.26 2.3-2.09 4.02-3.34 3.79z'/%3E%3C/svg%3E"); }
    .st-key-login_back button { background:rgba(255,255,255,.04)!important; border:1px solid rgba(255,255,255,.18)!important; color:#eef2f7!important; box-shadow:none!important; }
    .st-key-add_injury_record button { background:rgba(148,163,184,.08)!important; border:1px solid rgba(203,213,225,.20)!important; color:#eef2f7!important; box-shadow:none!important; }
    .st-key-add_injury_record button p,.st-key-add_injury_record button span { color:#eef2f7!important; }
    .admin-card { display:grid; grid-template-columns:auto 1fr auto; gap:16px; align-items:center; padding:18px; margin:18px 0; border:1px solid rgba(255,255,255,.1); border-radius:17px; background:linear-gradient(120deg,rgba(155,108,255,.13),rgba(15,33,54,.75)); }
    .admin-avatar { width:58px; height:58px; display:grid; place-items:center; border-radius:16px; background:linear-gradient(145deg,#9b6cff,#39e58c); color:#07111f; font-size:18px; font-weight:900; }
    .admin-name { color:#fff; font-size:17px; font-weight:800; }
    .admin-meta { color:#8799ad; font-size:11px; line-height:1.55; margin-top:3px; }
    .club-badge { padding:8px 10px; border-radius:10px; border:1px solid rgba(57,229,140,.25); background:rgba(57,229,140,.08); color:#59eca0; font-size:10px; font-weight:800; }
    .step-track { display:grid; grid-template-columns:repeat(6,1fr); gap:8px; margin:18px 0 24px; }
    .step-item { height:5px; border-radius:99px; background:rgba(255,255,255,.08); }
    .step-item.done { background:#39e58c; }
    .step-item.active { background:#9b6cff; box-shadow:0 0 12px rgba(155,108,255,.42); }
    .survey-head { text-align:center; max-width:700px; margin:24px auto; }
    .survey-head h1 { margin:10px 0 7px; }
    .question-card { border:1px solid rgba(255,255,255,.08); background:rgba(16,32,54,.72); border-radius:13px; padding:12px 14px; margin:8px 0; }
    .body-stage { height:430px; display:grid; place-items:center; perspective:900px; border:1px solid rgba(255,255,255,.09); border-radius:18px; background:radial-gradient(circle at 50% 35%,rgba(155,108,255,.12),transparent 45%),#0a1727; overflow:hidden; }
    .injury-soft-note { padding:12px 14px; border:1px solid rgba(152,169,192,.16); border-radius:12px; background:rgba(255,255,255,.035); color:#9dacbf; font-size:12px; line-height:1.55; margin-top:10px; }
    .anatomy-render { position:relative; height:545px; overflow:hidden; border:1px solid rgba(255,255,255,.10); border-radius:18px; background:radial-gradient(circle at 50% 33%,rgba(124,102,214,.18),transparent 43%),linear-gradient(180deg,#111c2b,#07111d); }
    .anatomy-model { position:absolute; left:50%; top:10px; width:285px; height:525px; transform-origin:50% 50%; transition:transform .18s ease; }
    .anatomy-model svg { width:100%; height:100%; display:block; overflow:visible; }
    .anatomy-view { position:absolute; right:14px; top:14px; z-index:3; padding:6px 9px; border:1px solid rgba(255,255,255,.12); border-radius:8px; background:rgba(5,12,22,.66); color:#9cabc0; font-size:10px; letter-spacing:.08em; }
    .anatomy-ground { position:absolute; left:22%; right:22%; bottom:13px; height:22px; border-radius:50%; background:radial-gradient(ellipse,rgba(0,0,0,.48),transparent 68%); }
    .body-hit { filter:drop-shadow(0 0 7px rgba(255,54,91,.92)); }
    .scientific-map { position:relative; width:100%; aspect-ratio:1/1; overflow:hidden; border:1px solid rgba(53,230,197,.20); border-radius:18px; background:radial-gradient(circle at 50% 40%,rgba(26,72,91,.32),transparent 56%),#050b13; }
    .scientific-map img { position:absolute; inset:0; width:100%; height:100%; object-fit:contain; display:block; }
    .map-marker { position:absolute; width:17px; height:17px; margin:-8.5px 0 0 -8.5px; border-radius:50%; background:#ff365b; border:2px solid #ffd7de; box-shadow:0 0 0 9px rgba(255,54,91,.18),0 0 18px rgba(255,54,91,.95); z-index:3; }
    .map-marker:after { content:""; position:absolute; inset:4px; border-radius:50%; background:#fff; opacity:.75; }
    .map-caption { display:flex; justify-content:space-around; margin-top:8px; color:#7f91a8; font-size:10px; letter-spacing:.12em; }
    .body-model { position:relative; width:180px; height:360px; transform-style:preserve-3d; transition:transform .35s ease; filter:drop-shadow(0 18px 28px rgba(0,0,0,.35)); }
    .mesh-part { position:absolute; left:50%; transform:translateX(-50%); border:1px solid rgba(150,205,220,.62); background:repeating-linear-gradient(45deg,rgba(57,229,140,.08) 0 2px,rgba(155,108,255,.13) 2px 5px); box-shadow:inset 0 0 18px rgba(76,201,240,.08); }
    .mesh-head { top:5px; width:54px; height:65px; border-radius:45%; }
    .mesh-torso { top:76px; width:95px; height:125px; clip-path:polygon(15% 0,85% 0,100% 100%,0 100%); }
    .mesh-arm { top:83px; width:28px; height:145px; border-radius:45%; }
    .mesh-arm.left { left:22px; transform:rotate(8deg); }
    .mesh-arm.right { left:auto; right:22px; transform:rotate(-8deg); }
    .mesh-leg { top:205px; width:38px; height:150px; border-radius:35% 35% 28% 28%; }
    .mesh-leg.left { left:44px; transform:rotate(2deg); }
    .mesh-leg.right { left:auto; right:44px; transform:rotate(-2deg); }
    .injury-dot { position:absolute; width:16px; height:16px; border-radius:50%; background:#ff5368; border:3px solid rgba(255,255,255,.85); box-shadow:0 0 18px #ff5368; z-index:4; }
    .injury-shoulder { top:85px; left:34px; }
    .injury-knee { top:270px; right:45px; }
    .injury-ankle { top:333px; left:49px; }

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
    logo_col, nav_col, language_col, login_col, signup_col = st.columns(
        [1.25, 2.65, .62, .9, .9], vertical_alignment="center"
    )
    with logo_col:
        brand()
    with nav_col:
        html('<div class="nav-links"><span>Ürün</span><span>Nasıl Çalışır</span><span>Analizler</span><span>Güvenlik</span></div>')
    with language_col:
        html('''
        <details class="lang-menu">
            <summary><span class="globe-icon"></span><span>TR</span><span class="lang-chevron">⌄</span></summary>
            <div class="lang-options">
                <div>TR · Türkçe</div><div>EN · English</div><div>ES · Español</div><div>IT · Italiano</div><div>FR · Français</div>
            </div>
        </details>
        ''')
    with login_col:
        st.button(
            "Giriş Yap",
            key="login_cta",
            use_container_width=True,
            on_click=set_page,
            args=("demo_login",),
        )
    with signup_col:
        st.button(
            "Üye Ol",
            key="signup_cta",
            use_container_width=True,
            on_click=set_page,
            args=("demo_login",),
        )

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
            <div class="trust-chip">Duygusal analiz</div>
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
            <p>Menteleven duygusal analiz verilerini oyuncunun kendi bildirimleri ve uzman gözlemleriyle birlikte değerlendirir; psikolojik veya tıbbi teşhis üretmez. Platform, bütün sinyalleri anlamlı bir zaman çizelgesinde birleştirir.</p>
        </div>
        <div class="footer-note">Menteleven · Futbol kulüpleri için oyuncu wellbeing platformu · Demo sürümü</div>
        """
    )


def show_demo_login():
    top_left, top_right = st.columns([4, 1])
    with top_left:
        brand()
    with top_right:
        st.button(
            "← Siteye Dön",
            key="login_back",
            use_container_width=True,
            on_click=set_page,
            args=("landing",),
        )

    html('<div style="height:35px"></div>')
    left, center, right = st.columns([1, 1.25, 1])
    with center:
        html('''
        <div class="auth-title">
            <div class="eyebrow">KULÜP HESABI</div>
            <h1>Menteleven'a giriş yapın</h1>
            <p>Takımınızın wellbeing kontrol merkezine güvenli şekilde erişin.</p>
        </div>
        ''')
        email = st.text_input("E-posta adresi", placeholder="admin@demofc.com")
        password = st.text_input("Şifre", type="password", placeholder="••••••••")
        forgot_col, empty_col = st.columns([1, 1])
        with forgot_col:
            if st.button("Şifremi unuttum", key="forgot_password"):
                st.info("Demo sürümünde şifre yenileme bağlantısı gönderilmez.")
        kvkk_ok = st.checkbox(
            "KVKK Aydınlatma Metni'ni okudum; verilerimin demo kapsamında işlenmesini kabul ediyorum.",
            key="kvkk_consent",
        )
        if st.button("Giriş Yap →", key="form_login", use_container_width=True, disabled=not kvkk_ok):
            st.session_state.admin_email = email or "admin@demofc.com"
            navigate("dashboard")
        html('<div class="auth-divider">VEYA ŞUNUNLA DEVAM ET</div>')
        google_col, apple_col = st.columns(2)
        with google_col:
            if st.button("Google", key="google_login", use_container_width=True, disabled=not kvkk_ok):
                st.session_state.admin_email = "admin@demofc.com"
                navigate("dashboard")
        with apple_col:
            if st.button("Apple", key="apple_login", use_container_width=True, disabled=not kvkk_ok):
                st.session_state.admin_email = "admin@demofc.com"
                navigate("dashboard")
        st.caption("Demo için alanları boş bırakarak da giriş yapabilirsiniz.")


def show_dashboard():
    logo, title, back = st.columns([1.2, 2.8, 1], vertical_alignment="center")
    with logo:
        brand()
    with title:
        html('<div style="color:#8fa1b7;font-size:13px">DEMO FC · A TAKIM · ANTRENMAN GÜNÜ</div>')
    with back:
        st.button(
            "← Landing Page",
            key="dashboard_back",
            use_container_width=True,
            on_click=set_page,
            args=("landing",),
        )

    html('''
    <div class="admin-card">
        <div class="admin-avatar">TD</div>
        <div>
            <div class="admin-name">Murat Demir</div>
            <div class="admin-meta">Teknik Direktör · 44 yaş · UEFA Pro Lisans<br>admin@demofc.com · İstanbul, Türkiye</div>
        </div>
        <div class="club-badge">DEMO FC · A TAKIM</div>
    </div>
    ''')

    html('<div style="margin:24px 0 18px"><div class="eyebrow">KULÜP ANALİTİĞİ</div><h1 style="margin:12px 0 5px;font-size:36px">Takım Kontrol Merkezi</h1><p>2 Eylül · Son oyuncu değerlendirmesi bugün 09:30\'da tamamlandı.</p></div>')
    filter_col, status_col, add_col = st.columns([1.7, 1, 1.15], vertical_alignment="bottom")
    with filter_col:
        st.date_input(
            "Analiz tarih aralığı",
            value=(date.today() - timedelta(days=7), date.today()),
            format="DD.MM.YYYY",
        )
    with status_col:
        st.selectbox("Oyuncu durumu", ["Tüm oyuncular", "Dengeli", "Takip edilmeli"])
    with add_col:
        if st.button("＋ Yeni Oyuncu Girişi", key="new_player_cta", use_container_width=True):
            navigate("new_player")

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
                navigate("player_profile")
    st.caption("Bu sonuçlar psikolojik veya tıbbi teşhis değildir; uzman karar sürecini destekler.")


def render_player_analysis(player):
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Motivasyon", player["motivation"], "+4")
    c2.metric("Enerji", player["energy"], "-2")
    c3.metric("Uyku", player["sleep"], "-5")
    c4.metric("Hazırlık", player["readiness"], "+1")
    c5.metric("Stres", player["stress"], "-3")
    c6.metric("Yorgunluk", player["fatigue"], "+2", delta_color="inverse")
    html(f"""
    <div class="profile-grid">
        <div class="glass-card">
            <div class="glass-title"><b>Bireysel Spider Chart</b><span>SON 7 GÜN</span></div>
            <div class="radar-wrap"><div class="css-radar" role="img" aria-label="Oyuncunun altı metrikli spider chart görünümü">
                <div class="radar-hex"></div><div class="radar-hex mid"></div><div class="radar-hex inner"></div><div class="radar-fill"></div><div class="radar-center"></div>
                <span class="radar-label-css rl-top">MOTİVASYON</span><span class="radar-label-css rl-ur">ENERJİ</span><span class="radar-label-css rl-lr">UYKU</span><span class="radar-label-css rl-bottom">HAZIRLIK</span><span class="radar-label-css rl-ll">YORGUNLUK</span><span class="radar-label-css rl-ul">STRES</span>
            </div></div>
            <div class="score-grid">
                <div class="score green"><span>Motivasyon</span><b>{player['motivation']}</b></div><div class="score cyan"><span>Enerji</span><b>{player['energy']}</b></div><div class="score purple"><span>Uyku</span><b>{player['sleep']}</b></div>
                <div class="score green"><span>Hazırlık</span><b>{player['readiness']}</b></div><div class="score red"><span>Yorgunluk</span><b>{player['fatigue']}</b></div><div class="score yellow"><span>Stres</span><b>{player['stress']}</b></div>
            </div>
        </div>
        <div class="glass-card"><div class="glass-title"><b>Öz-Bildirim İlişkili Duygusal Yük Haritası</b><span>BUGÜN</span></div><div class="heatmap-photo" style="min-height:360px;border-radius:12px"><div class="signal-badge">Duygusal yük sinyali<br><b>Orta</b></div><div class="heat-legend"><span>Düşük</span><span class="legend-bar"></span><span>Yüksek</span></div></div></div>
    </div>
    <div class="glass-card" style="margin-top:15px"><div class="glass-title"><b>AI Destekli Değerlendirme Özeti</b><span>UZMAN KONTROLÜ GEREKİR</span></div><p style="line-height:1.7;margin:0">Oyuncunun motivasyonu ve hazırlık seviyesi diğer metriklerle birlikte değerlendirildi. Bu çıktı teşhis değildir; gerektiğinde oyuncuyla görüşme yapılması önerilir.</p></div>
    """)


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
        st.button(
            "← Dashboard",
            key="profile_back",
            use_container_width=True,
            on_click=set_page,
            args=("dashboard",),
        )

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
    render_player_analysis(player)


INJURY_ZONES = {
    "Baş / Yüz": (0.0, 0.0, 3.78), "Boyun": (0.0, 0.0, 3.25),
    "Sağ omuz": (0.72, 0.0, 2.86), "Sol omuz": (-0.72, 0.0, 2.86),
    "Sağ üst kol": (1.05, 0.0, 2.25), "Sol üst kol": (-1.05, 0.0, 2.25),
    "Sağ dirsek": (1.22, 0.0, 1.65), "Sol dirsek": (-1.22, 0.0, 1.65),
    "Sağ ön kol / bilek": (1.35, 0.0, 1.05), "Sol ön kol / bilek": (-1.35, 0.0, 1.05),
    "Göğüs / Kaburga": (0.0, 0.35, 2.45), "Sırt": (0.0, -0.35, 2.35),
    "Bel": (0.0, -0.25, 1.55), "Karın": (0.0, 0.33, 1.72),
    "Sağ kalça / kasık": (0.45, 0.2, 1.08), "Sol kalça / kasık": (-0.45, 0.2, 1.08),
    "Sağ uyluk / adduktor": (0.48, 0.12, 0.25), "Sol uyluk / adduktor": (-0.48, 0.12, 0.25),
    "Sağ hamstring": (0.5, -0.24, 0.15), "Sol hamstring": (-0.5, -0.24, 0.15),
    "Sağ diz": (0.48, 0.2, -0.68), "Sol diz": (-0.48, 0.2, -0.68),
    "Sağ baldır": (0.48, -0.05, -1.35), "Sol baldır": (-0.48, -0.05, -1.35),
    "Sağ aşil": (0.48, -0.22, -2.03), "Sol aşil": (-0.48, -0.22, -2.03),
    "Sağ ayak bileği": (0.48, 0.0, -2.18), "Sol ayak bileği": (-0.48, 0.0, -2.18),
    "Sağ ayak / parmak": (0.48, 0.36, -2.42), "Sol ayak / parmak": (-0.48, 0.36, -2.42),
}


def append_low_poly_part(buffers, center, radii, angle=0, rings=7, segments=10):
    """Append a faceted anatomical volume to one combined, lightweight mesh."""
    x_values, y_values, z_values, i_values, j_values, k_values = buffers
    start = len(x_values)
    angle = np.deg2rad(angle)
    for ring in range(rings + 1):
        phi = np.pi * ring / rings
        for segment in range(segments):
            theta = 2 * np.pi * segment / segments
            local_x = radii[0] * np.sin(phi) * np.cos(theta)
            local_y = radii[1] * np.sin(phi) * np.sin(theta)
            local_z = radii[2] * np.cos(phi)
            rotated_x = local_x * np.cos(angle) + local_z * np.sin(angle)
            rotated_z = -local_x * np.sin(angle) + local_z * np.cos(angle)
            x_values.append(center[0] + rotated_x)
            y_values.append(center[1] + local_y)
            z_values.append(center[2] + rotated_z)
    for ring in range(rings):
        for segment in range(segments):
            current = start + ring * segments + segment
            following = start + ring * segments + (segment + 1) % segments
            upper = current + segments
            upper_following = following + segments
            i_values.extend([current, current])
            j_values.extend([following, upper_following])
            k_values.extend([upper_following, upper])


def build_body_figure(selected_zones, rotation=0):
    buffers = ([], [], [], [], [], [])
    # Referanstaki atletik fakat cinsiyetsiz oranlara yakın, tek parça low-poly gövde.
    central_parts = [
        ((0, 0, 3.78), (.34, .30, .47), 0), ((0, 0, 3.30), (.16, .16, .24), 0),
        ((0, 0, 2.68), (.84, .34, .66), 0), ((0, 0, 2.08), (.61, .30, .52), 0),
        ((0, 0, 1.60), (.54, .29, .45), 0), ((0, 0, 1.20), (.63, .34, .38), 0),
    ]
    for center, radii, angle in central_parts:
        append_low_poly_part(buffers, center, radii, angle)
    for side in (-1, 1):
        # Omuzdan hafif dışa açılan kollar ve futbolcu oranlarında düz bacaklar.
        limb_parts = [
            ((side*.76, 0, 2.45), (.30, .25, .64), side*7),
            ((side*.91, 0, 1.80), (.25, .21, .57), side*8),
            ((side*1.04, 0, 1.22), (.20, .18, .53), side*7),
            ((side*1.12, .03, .72), (.17, .20, .27), side*5),
            ((side*.39, 0, .51), (.34, .29, .78), side*1),
            ((side*.40, 0, -.31), (.30, .26, .68), 0),
            ((side*.40, 0, -1.04), (.24, .22, .66), 0),
            ((side*.40, 0, -1.72), (.18, .18, .48), 0),
            ((side*.40, .18, -2.19), (.18, .38, .14), 0),
        ]
        for center, radii, angle in limb_parts:
            append_low_poly_part(buffers, center, radii, angle)
    x_values, y_values, z_values, i_values, j_values, k_values = buffers
    fig = go.Figure(go.Mesh3d(
        x=x_values, y=y_values, z=z_values, i=i_values, j=j_values, k=k_values,
        color="#9aa7b8", flatshading=True, hoverinfo="skip", opacity=1,
        lighting=dict(ambient=.42, diffuse=.78, specular=.24, roughness=.72, fresnel=.08),
        lightposition=dict(x=110, y=180, z=220),
    ))
    if selected_zones:
        coords = [INJURY_ZONES[zone] for zone in selected_zones]
        fig.add_trace(go.Scatter3d(
            x=[p[0] for p in coords], y=[p[1] for p in coords], z=[p[2] for p in coords],
            mode="markers", text=selected_zones, hovertemplate="<b>%{text}</b><extra></extra>",
            marker=dict(size=10, color="#ff365b", opacity=1, line=dict(color="#ffd5dc", width=2)),
        ))
        # İşaretler modelin içinde kaybolmasın diye dış halo katmanı.
        fig.add_trace(go.Scatter3d(
            x=[p[0] for p in coords], y=[p[1] for p in coords], z=[p[2] for p in coords],
            mode="markers", hoverinfo="skip",
            marker=dict(size=17, color="rgba(255,54,91,.20)", line=dict(width=0)),
        ))
    angle = np.deg2rad(rotation)
    fig.update_layout(
        height=545, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="rgba(0,0,0,0)",
        scene=dict(
            bgcolor="rgba(8,17,29,.96)", aspectmode="data",
            xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
            camera=dict(eye=dict(x=2.45*np.sin(angle), y=2.45*np.cos(angle), z=.12)),
            dragmode=False,
        ),
        showlegend=False,
    )
    return fig


def render_anatomy_model(selected_zones, rotation):
    """Stable browser-native low-poly mannequin; no WebGL dependency."""
    radians = np.deg2rad(rotation)
    width_scale = .34 + .66 * abs(np.cos(radians))
    direction = -1 if 90 < rotation < 270 else 1
    view = "ARKA" if 135 <= rotation <= 225 else "YAN" if 45 < rotation < 315 else "ÖN"
    marker_html = ""
    for zone in selected_zones:
        x3d, _, z3d = INJURY_ZONES[zone]
        x = 160 + x3d * 78
        y = 70 + (3.8 - z3d) * 78
        marker_html += f'''<g class="body-hit"><circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="rgba(255,54,91,.20)"/><circle cx="{x:.1f}" cy="{y:.1f}" r="6.5" fill="#ff365b" stroke="#ffd7de" stroke-width="2"/></g>'''
    return f'''
    <div class="anatomy-render">
      <div class="anatomy-view">{view} · {rotation}°</div>
      <div class="anatomy-model" style="transform:translateX(-50%) scaleX({direction * width_scale:.3f});">
        <svg viewBox="0 0 320 620" role="img" aria-label="Cinsiyetsiz bütünsel low-poly insan modeli">
          <g stroke="#dce5ef" stroke-opacity=".26" stroke-width="1.2" stroke-linejoin="round">
            <!-- Head and neck -->
            <path fill="#aab5c4" d="M130 37 L145 18 L174 17 L191 36 L194 72 L180 101 L161 112 L141 100 L127 72 Z"/>
            <path fill="#7e8da1" d="M145 101 L178 101 L184 137 L137 137 Z"/>
            <!-- One continuous shoulder, torso and pelvis core -->
            <path fill="#9aa7b8" d="M137 125 L105 137 L82 158 L96 198 L111 188 L119 248 L128 320 L116 354 L128 383 L160 394 L193 383 L205 354 L193 320 L202 248 L210 188 L225 198 L239 158 L216 137 L181 124 L160 139 Z"/>
            <!-- Left arm, deliberately overlapping shoulder -->
            <path fill="#7d8ca0" d="M108 137 L81 150 L61 194 L45 241 L31 291 L42 303 L60 282 L76 244 L96 207 L119 181 Z"/>
            <path fill="#a8b3c2" d="M42 291 L27 319 L22 348 L31 365 L39 350 L43 371 L50 366 L51 344 L58 365 L64 357 L59 327 L60 282 Z"/>
            <!-- Right arm -->
            <path fill="#748398" d="M212 137 L239 150 L259 194 L275 241 L289 291 L278 303 L260 282 L244 244 L224 207 L201 181 Z"/>
            <path fill="#9eabba" d="M278 291 L293 319 L298 348 L289 365 L281 350 L277 371 L270 366 L269 344 L262 365 L256 357 L261 327 L260 282 Z"/>
            <!-- Pelvis-to-feet continuous legs -->
            <path fill="#9facbb" d="M128 372 L158 385 L153 438 L145 490 L143 552 L134 590 L103 595 L111 579 L119 548 L114 486 L107 430 L116 354 Z"/>
            <path fill="#758499" d="M192 372 L162 385 L167 438 L175 490 L177 552 L186 590 L217 595 L209 579 L201 548 L206 486 L213 430 L204 354 Z"/>
            <!-- Low-poly anatomical facets -->
            <path fill="#e4e8ee" fill-opacity=".24" d="M137 125 L160 139 L142 192 L111 188 L105 137 Z"/>
            <path fill="#596a80" fill-opacity=".35" d="M181 124 L216 137 L210 188 L178 192 L160 139 Z"/>
            <path fill="#dfe6ee" fill-opacity=".18" d="M119 248 L160 232 L160 320 L128 320 Z"/>
            <path fill="#526278" fill-opacity=".27" d="M160 232 L202 248 L193 320 L160 320 Z"/>
            <path fill="#e5ebf2" fill-opacity=".20" d="M128 383 L160 394 L153 438 L107 430 Z"/>
            <path fill="#536379" fill-opacity=".30" d="M160 394 L193 383 L213 430 L167 438 Z"/>
          </g>
          <g>{marker_html}</g>
        </svg>
      </div>
      <div class="anatomy-ground"></div>
    </div>'''


def render_scientific_body_map(selected_zones):
    """Render a stable front/back PNG map and overlay every selected injury."""
    back_terms = ("Sırt", "hamstring", "aşil")
    markers = []
    for zone in selected_zones:
        x3d, _, z3d = INJURY_ZONES[zone]
        is_back = any(term.lower() in zone.lower() for term in back_terms)
        center_x = 74.5 if is_back else 25.5
        left = center_x + x3d * 10.8
        top = 5.2 + (3.8 - z3d) * 14.25
        markers.append(
            f'<span class="map-marker" style="left:{left:.1f}%;top:{top:.1f}%" title="{zone}" aria-label="{zone}"></span>'
        )
    return f'''
    <div class="scientific-map">
        <img src="{BODY_MAP_IMAGE}" alt="Ön ve arka görünüşlü bilimsel insan vücut haritası">
        {''.join(markers)}
    </div>
    <div class="map-caption"><span>ÖN GÖRÜNÜM</span><span>ARKA GÖRÜNÜM</span></div>
    '''


def show_new_player():
    logo, title, back = st.columns([1.2, 2.8, 1], vertical_alignment="center")
    with logo:
        brand()
    with title:
        html('<div style="color:#8fa1b7;font-size:13px">YENİ OYUNCU KAYDI</div>')
    with back:
        st.button("← Dashboard", key="new_player_back", use_container_width=True, on_click=set_page, args=("dashboard",))

    html('<div class="survey-head"><div class="eyebrow">OYUNCU PROFİLİ</div><h1>Yeni oyuncu oluşturun</h1><p>Temel oyuncu bilgilerini ve geçmiş sakatlık bölgelerini kaydedin.</p></div>')
    form_col, body_col = st.columns([1, 1], gap="large")
    with form_col:
        first_name = st.text_input("Ad", placeholder="Emre")
        last_name = st.text_input("Soyad", placeholder="Demir")
        position = st.selectbox("Mevki", ["Kaleci", "Stoper", "Bek", "Defansif Orta Saha", "Merkez Orta Saha", "Kanat", "10 Numara", "Santrafor"])
        age = st.number_input("Yaş", min_value=15, max_value=50, value=23)
        injury_type = st.selectbox("Sakatlık türü", ["Kas zorlanması", "Bağ yaralanması", "Eklem yaralanması", "Kırık / çatlak", "Tendon problemi", "Darbe / kontüzyon", "Ameliyat geçmişi", "Diğer"])
        injury_date = st.date_input("Sakatlık tarihi", value=date.today(), format="DD.MM.YYYY")
        previous_injuries = st.text_area("Geçmiş sakatlık özeti", placeholder="Örn. 2024 sağ diz bağ zorlanması")
        injury_note = st.text_area("Sakatlık açıklaması", placeholder="Şiddeti, tedavi süreci ve mevcut durum")

    with body_col:
        st.markdown("**Sakatlık bölgeleri**")
        if "injury_zone_selector" not in st.session_state:
            st.session_state.injury_zone_selector = list(st.session_state.get("injury_zones", []))
        selected_zones = st.multiselect(
            "Bir veya daha fazla anatomik bölge seçin",
            options=list(INJURY_ZONES.keys()),
            placeholder="Örn. Sağ diz, sol hamstring…",
            key="injury_zone_selector",
        )
        st.session_state.injury_zones = list(selected_zones)
        if selected_zones:
            st.caption(f"{len(selected_zones)} bölge seçildi: " + " · ".join(selected_zones))
        html(render_scientific_body_map(selected_zones))
        html('<div class="injury-soft-note"><b>Vücut haritası:</b> Ön bölge sakatlıkları soldaki, sırt–hamstring–aşil bölgeleri sağdaki görünüm üzerinde işaretlenir. Birden fazla seçim aynı anda kırmızı noktalarla gösterilir.</div>')

    injury_records = st.session_state.setdefault("injury_records", [])
    if st.button("＋ Daha Fazla Sakatlık Ekle", key="add_injury_record", use_container_width=True):
        if not selected_zones:
            st.warning("Önce listeden en az bir sakatlık bölgesi seçin.")
        else:
            injury_records.append({
                "regions": list(selected_zones), "type": injury_type,
                "date": injury_date.strftime("%d.%m.%Y"),
                "summary": previous_injuries.strip(), "note": injury_note.strip(),
            })
            st.success(f"{len(injury_records)}. sakatlık kaydı listeye eklendi. Yeni bir bölge seçerek devam edebilirsiniz.")

    if injury_records:
        record_html = "".join(
            f'''<div class="injury-soft-note"><b>{index}. {record['type']}</b> · {record['date']}<br>
            <span style="color:#ff8092">{', '.join(record['regions'])}</span><br>{record['note'] or record['summary'] or 'Açıklama eklenmedi.'}</div>'''
            for index, record in enumerate(injury_records, start=1)
        )
        html(f'<div style="margin:18px 0 10px"><b>Eklenen sakatlık kayıtları ({len(injury_records)})</b>{record_html}</div>')

    if st.button("Oyuncuyu Kaydet ve Ankete Geç →", key="save_player", use_container_width=True):
        full_name = f"{first_name.strip()} {last_name.strip()}".strip() or "Yeni Oyuncu"
        st.session_state.selected_player = {
            "number": "—", "name": full_name, "position": position,
            "age": age, "injuries": previous_injuries, "injury_note": injury_note,
            "injury_zones": selected_zones,
            "injury_records": injury_records,
            "motivation": 0, "energy": 0, "sleep": 0, "readiness": 0,
            "stress": 0, "fatigue": 0, "status": "Anket Bekleniyor", "portrait_index": 0,
        }
        st.session_state.survey_step = 0
        st.session_state.survey_answers = {}
        navigate("survey")


def show_survey():
    categories = list(SURVEY.keys())
    step = st.session_state.setdefault("survey_step", 0)
    answers = st.session_state.setdefault("survey_answers", {})
    category = categories[step]

    logo, title, exit_col = st.columns([1.2, 2.8, 1], vertical_alignment="center")
    with logo:
        brand()
    with title:
        html(f'<div style="color:#8fa1b7;font-size:13px">OYUNCU ANKETİ · {step + 1}/6</div>')
    with exit_col:
        st.button("Kaydet ve Çık", key="survey_exit", use_container_width=True, on_click=set_page, args=("dashboard",))

    progress_parts = "".join(
        f'<div class="step-item {"done" if i < step else "active" if i == step else ""}"></div>'
        for i in range(6)
    )
    html(f'<div class="step-track">{progress_parts}</div><div class="survey-head"><div class="eyebrow">{category.upper()}</div><h1>{category} değerlendirmesi</h1><p>Her ifade için son 7 gündeki durumunuzu en iyi anlatan seçeneği işaretleyin.</p></div>')

    def save_answer_and_advance(widget_key, answer_key, current_step):
        selected_answer = st.session_state.get(widget_key)
        if selected_answer:
            answers[answer_key] = int(selected_answer[0])
        current_category = categories[current_step]
        category_complete = all(f"{current_category}_{i}" in answers for i in range(1, 11))
        if category_complete and current_step < 5:
            st.session_state.survey_step = current_step + 1

    for index, question in enumerate(SURVEY[category], start=1):
        key = f"survey_{step}_{index}"
        answer_key = f"{category}_{index}"
        html(f'<div class="question-card"><b style="color:#f1f5f9">{index}. {question}</b></div>')
        answer = st.radio(
            "Yanıt", ANSWER_OPTIONS, index=None, key=key, horizontal=True,
            label_visibility="collapsed", on_change=save_answer_and_advance,
            args=(key, answer_key, step),
        )
        if answer:
            answers[answer_key] = int(answer[0])

    completed = all(f"{category}_{i}" in answers for i in range(1, 11))
    back_col, info_col, next_col = st.columns([1, 2, 1])
    with back_col:
        if step > 0 and st.button("← Önceki kategori", use_container_width=True):
            st.session_state.survey_step -= 1
            st.rerun()
    with info_col:
        answered_count = sum(1 for i in range(1, 11) if f"{category}_{i}" in answers)
        st.progress(answered_count / 10, text=f"Bu kategoride {answered_count}/10 soru tamamlandı")
    with next_col:
        if step < 5:
            if st.button("Sonraki kategori →", disabled=not completed, use_container_width=True):
                st.session_state.survey_step += 1
                st.rerun()
        elif st.button("Anketi Bitir", disabled=not completed, use_container_width=True):
            scores = {}
            for cat in categories:
                values = [answers[f"{cat}_{i}"] for i in range(1, 11)]
                # Stres kategorisindeki son ifade olumlu kurulduğu için ters puanlanır.
                if cat == "Stres":
                    values[-1] = 6 - values[-1]
                scores[cat] = round(sum(values) / len(values) * 20)
            player = st.session_state.selected_player
            player.update({
                "stress": scores["Stres"], "motivation": scores["Motivasyon"],
                "energy": scores["Enerji"], "fatigue": scores["Yorgunluk"],
                "sleep": scores["Uyku"], "readiness": scores["Hazırlık"],
                "status": "Takip Edilmeli" if scores["Stres"] >= 70 or scores["Yorgunluk"] >= 70 else "Dengeli",
            })
            navigate("player_profile")


if st.session_state.page == "landing":
    show_landing_page()
elif st.session_state.page == "demo_login":
    show_demo_login()
elif st.session_state.page == "player_profile":
    show_player_profile()
elif st.session_state.page == "new_player":
    show_new_player()
elif st.session_state.page == "survey":
    show_survey()
else:
    show_dashboard()
