import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import os
import math

# Başlık ekleme
st.title("🌍 Hava Kirliliğinin Başlıca Nedenleri - Matematik Dersi Performans Ödevi")

# Sağ üst köşeye metin ekleyelim (HTML ile)
st.markdown(
    """
    <div style="text-align: right; font-size: 14px; font-weight: bold;">
        Perihan Azra Kurt - 5B / 250
    </div>
    """,
    unsafe_allow_html=True
)

# Sabit seçenekler
static_options = [
    "Araç Egzozları",
    "Orman Yangınları",
    "Yoğun Hava Trafiği",
    "Sigara Dumanı",
    "Tarım Faaliyetleri",
    "Sanayi ve Fabrikalardan Çıkan Dumanlar"
]

# Sabit değerler 1 olarak ayarlandı
static_values = [1] * len(static_options)

# Dinamik seçenekler için başlangıçta boş liste
dynamic_options = []
dynamic_values = []

# Ekranı iki sütuna ayıralım
col1, col2 = st.columns([1, 2])  # Sol sütun (1 birim genişlik) ve sağ sütun (2 birim genişlik)

# Sol sütunda seçenekleri gir
with col1:
    # Sabit seçeneklerin değerlerini alalım
    for i in range(len(static_options)):
        value = st.number_input(f"{static_options[i]} Değeri:", min_value=0, step=1, value=static_values[i])
        static_values[i] = value

    # Dinamik seçenek ekleme formu
    st.subheader("Yeni Seçenek Ekle")
    new_option = st.text_input("Yeni Seçenek Adı:")
    new_value = st.number_input("Yeni Seçenek Değeri:", min_value=0, step=1, value=0)

    if st.button("Yeni Seçenek Ekle"):
        if new_option:
            dynamic_options.append(new_option)
            dynamic_values.append(new_value)
            st.success(f"{new_option} başarıyla eklendi!")
        else:
            st.warning("Lütfen yeni seçenek adı girin.")

    # Veriyi kaydetme butonu
    if st.button("Veriyi Kaydet"):
        all_options = static_options + dynamic_options
        all_values = static_values + dynamic_values
        data = pd.DataFrame({
            "Seçenekler": all_options,
            "Değerler": all_values
        })

        # Dosya yolu belirleyelim
        file_path = "anket_sonuc.csv"

        if os.path.exists(file_path):
            # Eğer dosya varsa, verileri ekleyelim
            data.to_csv(file_path, mode='a', header=False, index=False)
        else:
            # Eğer dosya yoksa, başlıklarla birlikte kaydedelim
            data.to_csv(file_path, mode='w', header=True, index=False)

        st.success("Veriler başarıyla kaydedildi.")

# Sağ sütunda daire grafiğini ve tabloyu göster
with col2:
    all_options = static_options + dynamic_options
    all_values = static_values + dynamic_values

    if sum(all_values) > 0:
        # Kesir formatında etiket oluşturma
        def frac_format(val):
            total = sum(all_values)
            # Kesir formatını oluşturmak için en yakın tam sayıya yuvarlıyoruz
            gcd = math.gcd(int(val), total)  # Kesirlerin paydasını bulmak için
            return f"{int(val // gcd)} / {int(total // gcd)}"


        # Grafik oluşturma
        fig, ax = plt.subplots()
        ax.pie(all_values, labels=all_options, autopct=lambda p: frac_format(p * sum(all_values) / 100), startangle=90)
        ax.axis('equal')  # Eşit oranlı daire grafik

        # Anlık grafiği göster
        st.pyplot(fig)

        # Seçenekleri tablo olarak ekleme
        st.subheader("Seçenekler Tablosu:")
        df = pd.DataFrame({
            "Seçenekler": all_options,
            "Değerler": all_values
        })
        st.table(df)

        # Açıklama ekleme
        st.markdown(
            """
            <div style="font-size: 12px; color: grey;">
                Bu grafik, hava kirliliğinin başlıca nedenleri ile alakalı kararların alındığı bir grafiktir ve bu grafik daire grafiğidir.
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("Lütfen verileri girin.")
