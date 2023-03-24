import streamlit as st
import pandas as pd
import openpyxl

st.set_page_config(page_title='Benim Sayfam')

profilTable = pd.read_excel("https://docs.google.com/spreadsheets/d/1faly1ExiwiQKu717yzDq2Tjcod4HAQe8/edit?usp=share_link&ouid=101454387806620253543&rtpof=true&sd=true", engine="openpyxl")
profil_df = pd.DataFrame(profilTable)
profil_names = profil_df["PROFİL"].to_list()

material_dict = {"S235": [235, 360], "S275": [275, 430], "S355": [355, 510], "S450": [440, 550]}

with st.sidebar:
    option = st.selectbox("Bir profil seçiniz", profil_names)
    materials = st.selectbox("Malzeme", material_dict.keys())
    L = st.number_input("L (cm)", step=1)

Fy = material_dict[materials][0]
Fu = material_dict[materials][1]

st.info(f"Seçtiğiniz profil : {option}")

option_index = profil_names.index(option)
option_row = profil_df.iloc[option_index]
print("Profil özelliklleri :", option_row[9])


with st.sidebar:
    narinlik = L / min(option_row[9], option_row[12])
    if narinlik <= 300:
        st.success(f"L/i = {narinlik}")
    else:
        st.warning(f"L/i = {narinlik}")
    An = st.number_input("Net Alan, An (cm4)")
    U = st.number_input('Gerilme düzensizliği etki katsayısı, U')
    st.info("Blok Kırılma Durumu için")
    Ubs = st.number_input("Çekme gerilmeleri yayılışını gözönüne alan bir katsayı")
    Agv = st.number_input("Kayma gerilmesi etkisindeki kayıpsız alan (cm2)")
    Anv = st.number_input("Kayma gerilmesi etkisindeki net alan (cm2)")
    Ant = st.number_input("Çekme gerilmesi etkisindeki net alan (cm2)")


with st.expander('Profil özellikleri'):
    st.table(option_row)

Tn_akma = round(Fy * option_row[1] * 100 / 1000, 3)
st.info(f"Akma sınır durumu için Tn = {Tn_akma} kN")

Ae = An * U
Tn_kirilma = round(Fu * Ae / 10, 3)
st.info(f"Kırılma sınır durumu için Tn = {Tn_kirilma} kN")
st.success(f"Tasarım çekme kuvveti dayanımı, ΦtTn = {min(0.9 * Tn_akma, .75 * Tn_kirilma)}")

Rn = min(.6 * Fu * Anv / 10 + Ubs * Fu * Ant / 10, .6 * Fy * Agv / 10 + Ubs * Fu * Ant / 10)
st.success(f"Tasarım blok kırılma dayanımı, ΦRn = {Rn * .75}")









