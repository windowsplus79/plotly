import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="데이터 분석",
    page_icon="📊",
    layout="wide"
)

# 제목
st.title("데이터 분석 대시보드")

# 사이드바
st.sidebar.title("설정")
st.sidebar.write("여기에 설정 옵션을 추가할 수 있습니다.")

# 메인 영역
st.write("데이터를 업로드하고 분석을 시작하세요.") 