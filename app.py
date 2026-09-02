import streamlit as st

st.set_page_config(
    page_title="Player Wellbeing Platform",
    page_icon="⚽",
    layout="wide"
)

if "page" not in st.session_state:
    st.session_state.page = "landing"


def show_landing_page():
    st.title("Oyuncularınızı Daha Yakından Anlayın")

    st.subheader(
        "Futbol kulüpleri için AI destekli oyuncu wellbeing "
        "ve performans takip platformu."
    )

    st.write(
        """
        Kısa oyuncu anketlerini, aktivite verilerini ve uzman
        değerlendirmelerini tek bir platformda birleştirin.
        Takımınızdaki önemli değişimleri daha erken fark edin.
        """
    )

    if st.button("Canlı Demoyu Gör", type="primary"):
        st.session_state.page = "demo"
        st.rerun()


def show_demo():
    st.title("Demo Kulübü Dashboard")

    if st.button("← Landing Page'e Dön"):
        st.session_state.page = "landing"
        st.rerun()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Toplam Oyuncu", "24")

    with col2:
        st.metric("Ortalama Motivasyon", "82", "+4")

    with col3:
        st.metric("Ortalama Enerji", "76", "-2")

    with col4:
        st.metric("Takip Edilmeli", "3")

    st.divider()

    st.subheader("Takımın Genel Durumu")

    chart_data = {
        "Motivasyon": [72, 74, 73, 77, 79, 80, 82],
        "Enerji": [80, 78, 79, 77, 75, 74, 76]
    }

    st.line_chart(chart_data)

    st.subheader("Son Oyuncu Değerlendirmeleri")

    st.dataframe(
        {
            "Oyuncu": [
                "Emre Demir",
                "Arda Kaya",
                "Kerem Yılmaz",
                "Mert Akın"
            ],
            "Pozisyon": [
                "Orta Saha",
                "Forvet",
                "Kaleci",
                "Defans"
            ],
            "Motivasyon": [86, 78, 91, 64],
            "Stres": [25, 42, 18, 72],
            "Durum": [
                "Dengeli",
                "Dengeli",
                "Dengeli",
                "Takip Edilmeli"
            ]
        },
        use_container_width=True,
        hide_index=True
    )


if st.session_state.page == "landing":
    show_landing_page()
else:
    show_demo()
