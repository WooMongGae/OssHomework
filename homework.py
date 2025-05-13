import streamlit as st
import pandas as pd
import plotly.express as px

# 엑셀 파일 불러오기
df = pd.read_excel("보건복지부_전국 지역보건의료기관 현황_20221231.xlsx", engine='openpyxl')

# 필터링용 주요 컬럼 이름 유지: 시도, 기관유형
df = df.rename(columns={
    "보건기관명": "기관명"
})

# --- 사이드바 입력 ---
st.sidebar.title("🔎 조건 설정")
selected_city = st.sidebar.selectbox("📍 시도 선택", sorted(df["시도"].unique()))
selected_types = st.sidebar.multiselect("🏥 기관 유형 선택", df["기관유형"].unique(), default=df["기관유형"].unique())
min_count = st.sidebar.slider("기관 수 하한선", 1, 100, 5)

# --- 필터링 ---
filtered = df[(df["시도"] == selected_city) & (df["기관유형"].isin(selected_types))]

# --- 집계 ---
grouped = filtered.groupby("기관유형").size().reset_index(name="기관 수")
grouped = grouped[grouped["기관 수"] >= min_count]

# --- 출력 영역 ---
st.title(f"🏥 {selected_city} 보건의료기관 현황")
st.markdown(f"**선택한 기관 유형:** {', '.join(selected_types)}")

# Bar Chart
fig = px.bar(grouped, x="기관유형", y="기관 수", title="기관 유형별 개수", color="기관유형", text_auto=True)
st.plotly_chart(fig)

# Pie Chart
fig2 = px.pie(grouped, values="기관 수", names="기관유형", title="기관 유형 비율")
st.plotly_chart(fig2)
