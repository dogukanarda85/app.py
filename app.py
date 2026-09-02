import textwrap

import streamlit as st


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
    """Render indented HTML without Streamlit treating it as source code."""
    st.markdown(textwrap.dedent(content), unsafe_allow_html=True)


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

    .heatmap-photo {
        position:relative; min-height:390px;
        background:
            linear-gradient(0deg, rgba(5,14,25,.64), rgba(5,14,25,.1)),
            url('https://images.unsplash.com/photo-1579952363873-27f3bade9f55?auto=format&fit=crop&w=1200&q=82') center/cover;
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
    .radar-wrap { min-height:242px; padding:0 12px 12px; }
    .radar-svg { width:100%; height:210px; display:block; }
    .radar-grid { fill:none; stroke:rgba(255,255,255,.13); stroke-width:1; }
    .radar-axis { stroke:rgba(255,255,255,.1); stroke-width:1; }
    .radar-shape { fill:rgba(155,108,255,.3); stroke:#a77dff; stroke-width:2.2; }
    .radar-dot { fill:var(--green); stroke:#07111f; stroke-width:2; }
    .radar-label { fill:#91a3b8; font-size:9px; font-family:Arial,sans-serif; }

    .score-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; padding:0 12px 12px; }
    .score { background:#102036; border:1px solid var(--border); border-radius:12px; padding:12px; }
    .score span { display:block; color:#8194aa; font-size:9px; text-transform:uppercase; letter-spacing:.6px; }
    .score b { display:block; color:#fff; font-size:22px; margin-top:4px; }
    .score.green b { color:var(--green); }
    .score.purple b { color:#b99cff; }
    .alert {
        margin:0 12px 12px; border-left:3px solid var(--yellow); border-radius:9px;
        background:rgba(247,198,91,.07); color:#dbe4ee; padding:11px; font-size:11px; line-height:1.5;
    }

    .section { margin-top:86px; }
    .section h2 { max-width:760px; font-size:40px; letter-spacing:-1.7px; margin:12px 0 10px; }
    .section-copy { max-width:740px; line-height:1.7; }
    .visual-features { display:grid; grid-template-columns:repeat(3,1fr); gap:15px; margin-top:25px; }
    .feature-card {
        min-height:205px; border:1px solid var(--border); border-radius:17px; padding:22px;
        background:linear-gradient(145deg, rgba(255,255,255,.04), rgba(255,255,255,.015));
    }
    .feature-icon { width:42px; height:42px; display:grid; place-items:center; border-radius:12px; background:rgba(155,108,255,.13); border:1px solid rgba(155,108,255,.26); font-size:19px; }
    .feature-card h3 { font-size:18px; margin:18px 0 8px; }
    .feature-card p { font-size:14px; line-height:1.6; }
    .security-panel {
        margin-top:70px; border:1px solid rgba(155,108,255,.23); border-radius:20px; padding:32px;
        background:linear-gradient(120deg, rgba(155,108,255,.1), rgba(57,229,140,.045));
    }
    .footer-note { margin-top:70px; border-top:1px solid var(--border); padding-top:25px; color:#73869b; font-size:12px; text-align:center; }

    @media (max-width:900px) {
        .nav-links { display:none; }
        .stage-grid { grid-template-columns:1fr; }
        .visual-features { grid-template-columns:1fr; }
        .hero { padding-top:42px; }
        .hero h1 { letter-spacing:-2px; }
    }
    </style>
    """
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
            st.session_state.page = "demo_login"
            st.rerun()

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
            st.session_state.page = "demo_login"
            st.rerun()
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
                        <span>Antrenman Görseli · Dikkat Haritası</span>
                        <small>AI destekli görsel bağlam</small>
                    </div>
                    <div class="heatmap-photo">
                        <div class="signal-badge">Gözlem sinyali<br><b>Orta</b></div>
                        <div class="heat-legend"><span>Düşük</span><span class="legend-bar"></span><span>Yüksek</span></div>
                    </div>
                </div>

                <div class="analysis-column">
                    <div class="visual-card">
                        <div class="card-head">
                            <span>Oyuncu Wellbeing Profili</span>
                            <small>Son 7 gün</small>
                        </div>
                        <div class="radar-wrap">
                            <svg class="radar-svg" viewBox="0 0 280 220" aria-label="Oyuncu spider chart">
                                <polygon class="radar-grid" points="140,25 236,95 199,190 81,190 44,95"/>
                                <polygon class="radar-grid" points="140,50 212,102 184,172 96,172 68,102"/>
                                <polygon class="radar-grid" points="140,75 188,109 169,154 111,154 92,109"/>
                                <line class="radar-axis" x1="140" y1="110" x2="140" y2="25"/>
                                <line class="radar-axis" x1="140" y1="110" x2="236" y2="95"/>
                                <line class="radar-axis" x1="140" y1="110" x2="199" y2="190"/>
                                <line class="radar-axis" x1="140" y1="110" x2="81" y2="190"/>
                                <line class="radar-axis" x1="140" y1="110" x2="44" y2="95"/>
                                <polygon class="radar-shape" points="140,40 214,99 178,162 96,169 67,99"/>
                                <circle class="radar-dot" cx="140" cy="40" r="4"/>
                                <circle class="radar-dot" cx="214" cy="99" r="4"/>
                                <circle class="radar-dot" cx="178" cy="162" r="4"/>
                                <circle class="radar-dot" cx="96" cy="169" r="4"/>
                                <circle class="radar-dot" cx="67" cy="99" r="4"/>
                                <text class="radar-label" x="140" y="15" text-anchor="middle">MOTİVASYON</text>
                                <text class="radar-label" x="246" y="96">ENERJİ</text>
                                <text class="radar-label" x="204" y="207">UYKU</text>
                                <text class="radar-label" x="43" y="207">HAZIRLIK</text>
                                <text class="radar-label" x="5" y="96">STRES</text>
                            </svg>
                        </div>
                        <div class="score-grid">
                            <div class="score green"><span>Motivasyon</span><b>82</b></div>
                            <div class="score purple"><span>Hazırlık</span><b>76</b></div>
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
                    <div class="feature-icon">◉</div>
                    <h3>Isı haritalı görsel kayıt</h3>
                    <p>Antrenman ve maç görsellerini oyuncunun değerlendirme zaman çizelgesiyle ilişkilendirin.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">◇</div>
                    <h3>Spider chart profilleri</h3>
                    <p>Motivasyon, enerji, uyku, stres ve hazırlık değerlerini tek bakışta karşılaştırın.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">▦</div>
                    <h3>Takım ve kadro görünümü</h3>
                    <p>Futbol menajerlik sistemlerini çağrıştıran kartlarla takımın genel durumunu yönetin.</p>
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
            st.session_state.page = "landing"
            st.rerun()

    html('<div style="height:60px"></div><div style="text-align:center"><div class="eyebrow">CANLI ÜRÜN DEMOSU</div><h1>Demo Kulübüne Giriş</h1><p>Platformu farklı ekip rollerinden biriyle inceleyin.</p></div>')
    left, center, right = st.columns([1, 1.35, 1])
    with center:
        role = st.selectbox("Rolünüz", ["Teknik Direktör", "Spor Psikoloğu", "Performans Ekibi"])
        st.caption(f"{role} görünümüyle devam edeceksiniz. Tüm demo verileri kurgusaldır.")
        if st.button("Demo Hesabıyla Devam Et →", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()


def show_dashboard():
    logo, title, back = st.columns([1.2, 2.8, 1], vertical_alignment="center")
    with logo:
        brand()
    with title:
        html('<div style="color:#8fa1b7;font-size:13px">DEMO FC · A TAKIM · ANTRENMAN GÜNÜ</div>')
    with back:
        if st.button("← Siteye Dön", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()

    st.title("Takım Kontrol Merkezi")
    st.caption("2 Eylül · Son oyuncu değerlendirmesi bugün 09:30'da tamamlandı.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Toplam Oyuncu", "24")
    c2.metric("Takım Motivasyonu", "82", "+4")
    c3.metric("Ortalama Enerji", "76", "-2")
    c4.metric("Takip Edilmeli", "3", "+1", delta_color="inverse")

    chart, status = st.columns([1.65, 1], gap="large")
    with chart:
        st.subheader("Son 7 Günlük Takım Trendi")
        st.line_chart({"Motivasyon": [72,74,73,77,79,80,82], "Enerji": [80,78,79,77,75,74,76], "Hazırlık": [74,75,75,76,77,79,81]}, color=["#39e58c", "#9b6cff", "#f7c65b"], height=320)
    with status:
        st.subheader("Kadro Durumu")
        st.progress(.87, text="21 / 24 oyuncu maça hazır")
        st.progress(.75, text="18 oyuncu dengeli")
        st.progress(.12, text="3 oyuncu takip edilmeli")
        st.warning("3 oyuncunun uyku, enerji veya stres değerlerinde değişim bulunuyor.")

    st.subheader("Son Oyuncu Değerlendirmeleri")
    st.dataframe({
        "No": [10,8,1,9,5],
        "Oyuncu": ["Emre Demir","Arda Kaya","Kerem Yılmaz","Mert Akın","Can Eren"],
        "Pozisyon": ["10 Numara","Merkez Orta Saha","Kaleci","Santrafor","Stoper"],
        "Motivasyon": [86,78,91,64,72],
        "Enerji": [82,73,88,58,68],
        "Stres": [25,42,18,72,55],
        "Durum": ["Dengeli","Dengeli","Dengeli","Takip Edilmeli","Takip Edilmeli"],
    }, use_container_width=True, hide_index=True)
    st.caption("Bu sonuçlar psikolojik veya tıbbi teşhis değildir; uzman karar sürecini destekler.")


if st.session_state.page == "landing":
    show_landing_page()
elif st.session_state.page == "demo_login":
    show_demo_login()
else:
    show_dashboard()
