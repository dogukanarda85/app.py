import streamlit as st

# --------------------------------------------------
# SAYFA AYARLARI
# --------------------------------------------------

st.set_page_config(
    page_title="Menteleven | Player Wellbeing Intelligence",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# OTURUM DURUMU
# --------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "landing"

if "language" not in st.session_state:
    st.session_state.language = "TR — Türkçe"


# --------------------------------------------------
# TASARIM SİSTEMİ
# --------------------------------------------------

st.markdown(
    """
    <style>
    :root {
        --background: #07111f;
        --surface: #0d1b2d;
        --surface-light: #13243a;
        --border: rgba(255, 255, 255, 0.09);
        --primary: #39e58c;
        --primary-dark: #20bc6b;
        --text: #f4f7fb;
        --muted: #8fa1b7;
        --warning: #f4bf4f;
        --danger: #f66d6d;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 80% 8%,
                rgba(57, 229, 140, 0.08),
                transparent 30%
            ),
            #07111f;
        color: var(--text);
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }

    .block-container {
        max-width: 1240px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, p, span, label {
        font-family: Inter, Aptos, Arial, sans-serif;
    }

    h1, h2, h3 {
        color: var(--text);
    }

    p {
        color: var(--muted);
    }

    div[data-testid="stButton"] button {
        min-height: 46px;
        border-radius: 10px;
        border: 1px solid rgba(57, 229, 140, 0.35);
        background: #39e58c;
        color: #07111f;
        font-weight: 700;
        padding-left: 1.3rem;
        padding-right: 1.3rem;
        transition: all 0.2s ease;
    }

    div[data-testid="stButton"] button:hover {
        background: #54ee9e;
        border-color: #54ee9e;
        color: #07111f;
        transform: translateY(-1px);
    }

    div[data-testid="stSelectbox"] > div {
        border-radius: 10px;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 11px;
        height: 46px;
    }

    .brand-mark {
        width: 34px;
        height: 34px;
        display: grid;
        place-items: center;
        border-radius: 9px;
        background: #39e58c;
        color: #07111f;
        font-weight: 900;
        font-size: 16px;
    }

    .brand-name {
        color: #ffffff;
        font-size: 21px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    .nav-links {
        color: #91a4ba;
        font-size: 14px;
        padding-top: 13px;
        text-align: center;
        word-spacing: 17px;
        white-space: nowrap;
    }

    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        color: #39e58c;
        background: rgba(57, 229, 140, 0.08);
        border: 1px solid rgba(57, 229, 140, 0.22);
        border-radius: 999px;
        padding: 7px 12px;
        font-size: 12px;
        font-weight: 750;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 18px;
    }

    .hero-title {
        color: #f5f8fc;
        font-size: clamp(42px, 5vw, 69px);
        line-height: 1.02;
        letter-spacing: -3px;
        font-weight: 820;
        max-width: 710px;
        margin: 0 0 22px 0;
    }

    .hero-title span {
        color: #39e58c;
    }

    .hero-copy {
        color: #91a4ba;
        font-size: 18px;
        line-height: 1.7;
        max-width: 650px;
        margin-bottom: 23px;
    }

    .trust-row {
        display: flex;
        flex-wrap: wrap;
        gap: 9px;
        margin-top: 20px;
    }

    .trust-chip {
        color: #a8b7c9;
        border: 1px solid var(--border);
        background: rgba(255,255,255,0.025);
        border-radius: 999px;
        padding: 7px 11px;
        font-size: 12px;
    }

    .app-preview {
        position: relative;
        overflow: hidden;
        min-height: 470px;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 22px;
        background: #0b1929;
        box-shadow: 0 28px 80px rgba(0,0,0,0.33);
        padding: 18px;
    }

    .preview-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #8fa1b7;
        font-size: 11px;
        border-bottom: 1px solid var(--border);
        padding-bottom: 13px;
        margin-bottom: 15px;
    }

    .live-dot {
        display: inline-block;
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #39e58c;
        box-shadow: 0 0 12px #39e58c;
        margin-right: 6px;
    }

    .preview-grid {
        display: grid;
        grid-template-columns: 1.25fr 0.75fr;
        gap: 13px;
    }

    .pitch {
        position: relative;
        min-height: 365px;
        border-radius: 15px;
        overflow: hidden;
        border: 1px solid rgba(57,229,140,0.18);
        background:
            linear-gradient(
                90deg,
                rgba(57,229,140,0.025) 50%,
                transparent 50%
            ),
            #0b2a27;
        background-size: 60px 100%;
    }

    .pitch::before {
        content: "";
        position: absolute;
        inset: 15px;
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 3px;
    }

    .half-line {
        position: absolute;
        width: 1px;
        top: 15px;
        bottom: 15px;
        left: 50%;
        background: rgba(255,255,255,0.16);
    }

    .center-circle {
        position: absolute;
        width: 72px;
        height: 72px;
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 50%;
        left: calc(50% - 36px);
        top: calc(50% - 36px);
    }

    .player {
        position: absolute;
        width: 33px;
        height: 33px;
        display: grid;
        place-items: center;
        border-radius: 50%;
        background: #132b39;
        border: 2px solid #39e58c;
        color: #ffffff;
        font-size: 10px;
        font-weight: 800;
        box-shadow: 0 7px 18px rgba(0,0,0,0.3);
    }

    .player.warning {
        border-color: #f4bf4f;
    }

    .player.risk {
        border-color: #f66d6d;
    }

    .p1 { left: 7%; top: 45%; }
    .p2 { left: 27%; top: 18%; }
    .p3 { left: 27%; top: 45%; }
    .p4 { left: 27%; top: 72%; }
    .p5 { left: 52%; top: 25%; }
    .p6 { left: 52%; top: 65%; }
    .p7 { left: 73%; top: 18%; }
    .p8 { left: 73%; top: 45%; }
    .p9 { left: 73%; top: 72%; }
    .p10 { left: 88%; top: 45%; }

    .side-panel {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .mini-card {
        border: 1px solid var(--border);
        background: #102136;
        border-radius: 13px;
        padding: 13px;
    }

    .mini-label {
        color: #8194aa;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.7px;
    }

    .mini-value {
        color: #f5f8fc;
        font-size: 22px;
        font-weight: 800;
        margin-top: 5px;
    }

    .mini-change {
        color: #39e58c;
        font-size: 10px;
    }

    .alert-card {
        border-left: 3px solid #f4bf4f;
        background: rgba(244,191,79,0.07);
        border-radius: 9px;
        padding: 11px;
        color: #d9e1ea;
        font-size: 11px;
        line-height: 1.45;
    }

    .section-heading {
        margin-top: 85px;
        margin-bottom: 25px;
    }

    .section-heading h2 {
        font-size: 38px;
        letter-spacing: -1.5px;
        margin-bottom: 10px;
    }

    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
    }

    .feature-card {
        min-height: 180px;
        border-radius: 16px;
        border: 1px solid var(--border);
        background: linear-gradient(
            145deg,
            rgba(255,255,255,0.04),
            rgba(255,255,255,0.015)
        );
        padding: 23px;
    }

    .feature-number {
        color: #39e58c;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1px;
    }

    .feature-title {
        color: #f5f8fc;
        font-size: 19px;
        font-weight: 750;
        margin: 15px 0 8px;
    }

    .feature-copy {
        color: #899bb0;
        font-size: 14px;
        line-height: 1.6;
    }

    .security-panel {
        margin-top: 70px;
        border: 1px solid rgba(57,229,140,0.19);
        background: linear-gradient(
            120deg,
            rgba(57,229,140,0.08),
            rgba(255,255,255,0.02)
        );
        border-radius: 20px;
        padding: 33px;
    }

    .footer-note {
        margin-top: 70px;
        border-top: 1px solid var(--border);
        padding-top: 25px;
        color: #73869b;
        font-size: 12px;
        text-align: center;
    }

    .dashboard-header {
        border-bottom: 1px solid var(--border);
        padding-bottom: 20px;
        margin-bottom: 25px;
    }

    .player-row {
        border: 1px solid var(--border);
        background: #0d1b2d;
        border-radius: 13px;
        padding: 14px;
        margin-bottom: 10px;
    }

    .status-good {
        color: #39e58c;
        font-weight: 700;
    }

    .status-warning {
        color: #f4bf4f;
        font-weight: 700;
    }

    @media (max-width: 900px) {
        .nav-links {
            display: none;
        }

        .preview-grid {
            grid-template-columns: 1fr;
        }

        .side-panel {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
        }

        .feature-grid {
            grid-template-columns: 1fr;
        }

        .hero-title {
            letter-spacing: -1.8px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# LANDING PAGE
# --------------------------------------------------

def show_landing_page():

    logo_col, nav_col, language_col, button_col = st.columns(
        [1.35, 2.8, 1.25, 1.15],
        vertical_alignment="center"
    )

    with logo_col:
        st.markdown(
            """
            <div class="brand">
                <div class="brand-mark">M11</div>
                <div class="brand-name">Menteleven</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with nav_col:
        st.markdown(
            """
            <div class="nav-links">
                Ürün &nbsp; Nasıl-Çalışır &nbsp; Özellikler &nbsp; Güvenlik
            </div>
            """,
            unsafe_allow_html=True
        )

    with language_col:
        selected_language = st.selectbox(
            "Dil",
            [
                "TR — Türkçe",
                "EN — English",
                "ES — Español",
                "IT — Italiano",
                "FR — Français"
            ],
            index=[
                "TR — Türkçe",
                "EN — English",
                "ES — Español",
                "IT — Italiano",
                "FR — Français"
            ].index(st.session_state.language),
            label_visibility="collapsed"
        )

        if selected_language != st.session_state.language:
            st.session_state.language = selected_language

    with button_col:
        if st.button(
            "Canlı Demo",
            key="header_demo",
            use_container_width=True
        ):
            st.session_state.page = "demo_login"
            st.rerun()

    if st.session_state.language != "TR — Türkçe":
        st.info(
            "Seçtiğiniz dil, demo sürümünde yakında aktif olacaktır. "
            "İçerik şimdilik Türkçe görüntülenmektedir."
        )

    st.markdown("<div style='height:55px'></div>", unsafe_allow_html=True)

    hero_text, hero_visual = st.columns(
        [1.04, 0.96],
        gap="large",
        vertical_alignment="center"
    )

    with hero_text:
        st.markdown(
            """
            <div class="eyebrow">
                ⚽ Futbolcu Wellbeing Intelligence
            </div>

            <h1 class="hero-title">
                Oyuncuyu performansın
                <span>ötesinde anlayın.</span>
            </h1>

            <p class="hero-copy">
                Menteleven; oyuncu bildirimlerini, aktivite verilerini ve
                uzman gözlemlerini tek platformda birleştirerek takımınız
                için erken wellbeing sinyalleri oluşturur.
            </p>
            """,
            unsafe_allow_html=True
        )

        cta_col, secondary_col = st.columns([1, 1.2])

        with cta_col:
            if st.button(
                "Canlı Demoyu İncele →",
                key="hero_demo",
                use_container_width=True
            ):
                st.session_state.page = "demo_login"
                st.rerun()

        with secondary_col:
            st.markdown(
                """
                <div style="
                    color:#91a4ba;
                    font-size:13px;
                    padding:14px 0 0 8px;
                ">
                    Kredi kartı gerekmez · Kurgusal demo verileri
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            """
            <div class="trust-row">
                <div class="trust-chip">Yüz tanıma kullanılmaz</div>
                <div class="trust-chip">Psikolojik teşhis değildir</div>
                <div class="trust-chip">Uzman denetimli</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with hero_visual:
        st.markdown(
            """
            <div class="app-preview">
                <div class="preview-top">
                    <span>
                        <span class="live-dot"></span>
                        TAKIM KONTROL MERKEZİ
                    </span>
                    <span>4-2-3-1 · ANTRENMAN GÜNÜ</span>
                </div>

                <div class="preview-grid">
                    <div class="pitch">
                        <div class="half-line"></div>
                        <div class="center-circle"></div>

                        <div class="player p1">1</div>
                        <div class="player p2">4</div>
                        <div class="player warning p3">5</div>
                        <div class="player p4">3</div>
                        <div class="player p5">6</div>
                        <div class="player p6">8</div>
                        <div class="player p7">7</div>
                        <div class="player warning p8">10</div>
                        <div class="player p9">11</div>
                        <div class="player risk p10">9</div>
                    </div>

                    <div class="side-panel">
                        <div class="mini-card">
                            <div class="mini-label">Takım motivasyonu</div>
                            <div class="mini-value">82</div>
                            <div class="mini-change">↑ Son 7 günde +4</div>
                        </div>

                        <div class="mini-card">
                            <div class="mini-label">Hazır oyuncu</div>
                            <div class="mini-value">21 / 24</div>
                            <div class="mini-change">Kadronun %87'si</div>
                        </div>

                        <div class="alert-card">
                            <strong>3 oyuncu takip edilmeli</strong><br>
                            Uyku, enerji ve stres sinyallerinde değişim var.
                        </div>

                        <div class="mini-card">
                            <div class="mini-label">Son değerlendirme</div>
                            <div class="mini-value" style="font-size:15px;">
                                Bugün · 09:30
                            </div>
                            <div class="mini-change">24 oyuncu tamamladı</div>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="section-heading">
            <div class="eyebrow">NASIL ÇALIŞIR?</div>
            <h2>Takımın insani tarafını görünür hale getirin.</h2>
            <p>
                Kısa oyuncu bildirimlerinden uzman değerlendirmesine
                kadar bütün süreç tek bir kontrol merkezinde.
            </p>
        </div>

        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-number">01 · TOPLA</div>
                <div class="feature-title">30 saniyelik oyuncu bildirimi</div>
                <div class="feature-copy">
                    Oyuncular enerji, uyku, stres, yorgunluk ve motivasyon
                    seviyelerini hızlıca bildirir.
                </div>
            </div>

            <div class="feature-card">
                <div class="feature-number">02 · KARŞILAŞTIR</div>
                <div class="feature-title">Değişimleri erken görün</div>
                <div class="feature-copy">
                    Sistem günlük değerleri oyuncunun kendi geçmişi ve
                    takım trendleriyle karşılaştırır.
                </div>
            </div>

            <div class="feature-card">
                <div class="feature-number">03 · DEĞERLENDİR</div>
                <div class="feature-title">Uzman destekli karar alın</div>
                <div class="feature-copy">
                    Teknik ekip ve spor psikoloğu, risk sinyallerini birlikte
                    değerlendirerek gerekli takibi planlar.
                </div>
            </div>
        </div>

        <div class="security-panel">
            <div class="eyebrow">GÜVENLİ VE İNSAN ODAKLI</div>
            <h2 style="margin-top:4px;">
                Oyuncuyu etiketlemez, uzman ekibi destekler.
            </h2>
            <p style="max-width:850px; line-height:1.7;">
                Menteleven yüz tanıma kullanmaz, fotoğraflardan psikolojik
                durum çıkarmaya çalışmaz ve tıbbi teşhis üretmez. Platform,
                oyuncunun kendi bildirimleri ile yetkili uzmanların
                gözlemlerini anlamlı bir zaman çizelgesinde birleştirir.
            </p>
        </div>

        <div class="footer-note">
            Menteleven · Futbol kulüpleri için oyuncu wellbeing platformu
            · Demo sürümü
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# DEMO GİRİŞ
# --------------------------------------------------

def show_demo_login():

    top_left, top_right = st.columns([4, 1])

    with top_left:
        st.markdown(
            """
            <div class="brand">
                <div class="brand-mark">M11</div>
                <div class="brand-name">Menteleven</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with top_right:
        if st.button("← Siteye Dön", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()

    st.markdown("<div style='height:65px'></div>", unsafe_allow_html=True)

    left_space, login_area, right_space = st.columns([1, 1.4, 1])

    with login_area:
        st.markdown(
            """
            <div style="text-align:center;">
                <div class="eyebrow">CANLI ÜRÜN DEMOSU</div>
                <h1 style="font-size:38px; margin-bottom:10px;">
                    Demo Kulübüne Giriş
                </h1>
                <p>
                    Platformu farklı ekip rollerinden biriyle inceleyin.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        selected_role = st.selectbox(
            "Rolünüz",
            [
                "Teknik Direktör",
                "Spor Psikoloğu",
                "Performans Ekibi"
            ]
        )

        st.caption(
            f"{selected_role} görünümüyle devam edeceksiniz. "
            "Demo verilerinin tamamı kurgusaldır."
        )

        if st.button(
            "Demo Hesabıyla Devam Et →",
            use_container_width=True
        ):
            st.session_state.page = "dashboard"
            st.rerun()


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

def show_dashboard():

    top_logo, top_title, top_button = st.columns(
        [1.2, 2.8, 1],
        vertical_alignment="center"
    )

    with top_logo:
        st.markdown(
            """
            <div class="brand">
                <div class="brand-mark">M11</div>
                <div class="brand-name">Menteleven</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with top_title:
        st.markdown(
            """
            <div style="color:#8fa1b7; font-size:13px;">
                DEMO FC · A TAKIM · ANTRENMAN GÜNÜ
            </div>
            """,
            unsafe_allow_html=True
        )

    with top_button:
        if st.button("← Siteye Dön", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()

    st.markdown(
        """
        <div class="dashboard-header">
            <h1 style="font-size:35px; margin-bottom:4px;">
                Takım Kontrol Merkezi
            </h1>
            <p>
                2 Eylül · Son oyuncu değerlendirmesi bugün 09:30'da tamamlandı.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    metric_1, metric_2, metric_3, metric_4 = st.columns(4)

    with metric_1:
        st.metric("Toplam Oyuncu", "24")

    with metric_2:
        st.metric("Takım Motivasyonu", "82", "+4")

    with metric_3:
        st.metric("Ortalama Enerji", "76", "-2")

    with metric_4:
        st.metric("Takip Edilmeli", "3", "+1", delta_color="inverse")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    chart_col, status_col = st.columns([1.65, 1], gap="large")

    with chart_col:
        st.subheader("Son 7 Günlük Takım Trendi")

        chart_data = {
            "Motivasyon": [72, 74, 73, 77, 79, 80, 82],
            "Enerji": [80, 78, 79, 77, 75, 74, 76],
            "Hazırlık": [74, 75, 75, 76, 77, 79, 81]
        }

        st.line_chart(
            chart_data,
            color=["#39e58c", "#4ea8de", "#f4bf4f"],
            height=320
        )

    with status_col:
        st.subheader("Kadro Durumu")

        st.markdown("**Maça hazır oyuncular**")
        st.progress(0.87, text="21 / 24 oyuncu")

        st.markdown("**Dengeli durumda**")
        st.progress(0.75, text="18 oyuncu")

        st.markdown("**Takip edilmeli**")
        st.progress(0.12, text="3 oyuncu")

        st.warning(
            "3 oyuncunun uyku, enerji veya stres değerlerinde "
            "dikkat edilmesi gereken değişim bulunuyor."
        )

    st.subheader("Son Oyuncu Değerlendirmeleri")

    st.dataframe(
        {
            "No": [10, 8, 1, 9, 5],
            "Oyuncu": [
                "Emre Demir",
                "Arda Kaya",
                "Kerem Yılmaz",
                "Mert Akın",
                "Can Eren"
            ],
            "Pozisyon": [
                "10 Numara",
                "Merkez Orta Saha",
                "Kaleci",
                "Santrafor",
                "Stoper"
            ],
            "Motivasyon": [86, 78, 91, 64, 72],
            "Enerji": [82, 73, 88, 58, 68],
            "Stres": [25, 42, 18, 72, 55],
            "Durum": [
                "Dengeli",
                "Dengeli",
                "Dengeli",
                "Takip Edilmeli",
                "Takip Edilmeli"
            ]
        },
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Bu değerlendirmeler psikolojik veya tıbbi teşhis değildir. "
        "Yetkili uzmanların karar sürecini desteklemek amacıyla gösterilir."
    )


# --------------------------------------------------
# SAYFA YÖNLENDİRME
# --------------------------------------------------

if st.session_state.page == "landing":
    show_landing_page()

elif st.session_state.page == "demo_login":
    show_demo_login()

elif st.session_state.page == "dashboard":
    show_dashboard()
