import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(
    page_title="인구 현황 분석",
    page_icon="📊",
    layout="wide"
)

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 제목
st.title("2025년 4월 인구 현황 분석")

# 데이터 로드
@st.cache_data
def load_data():
    df_total = pd.read_csv('202504_202504_연령별인구현황_월간_남녀합계.csv', encoding='cp949')
    df_gender = pd.read_csv('202504_202504_연령별인구현황_월간_남녀구분.csv', encoding='cp949')
    return df_total, df_gender

try:
    df_total, df_gender = load_data()
    
    # 두 개의 컬럼 생성
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("연령대별 전체 인구 분포")
        
        # 전체 인구 막대 그래프
        fig_total = px.bar(
            df_total,
            x='연령',
            y='인구수',
            title='연령대별 전체 인구 분포',
            labels={'연령': '연령대', '인구수': '인구 수'},
            color_discrete_sequence=['#1f77b4']
        )
        
        # 그래프 스타일 설정
        fig_total.update_layout(
            xaxis_title="연령대",
            yaxis_title="인구 수",
            showlegend=False,
            height=600
        )
        
        st.plotly_chart(fig_total, use_container_width=True)
    
    with col2:
        st.subheader("인구 피라미드")
        
        # 남성 데이터는 음수로 변환
        df_gender['인구수_조정'] = df_gender.apply(
            lambda x: -x['인구수'] if x['성별'] == '남' else x['인구수'], 
            axis=1
        )
        
        # 인구 피라미드 생성
        fig_pyramid = px.bar(
            df_gender,
            x='인구수_조정',
            y='연령',
            color='성별',
            orientation='h',
            title='인구 피라미드',
            labels={'인구수_조정': '인구 수', '연령': '연령대'},
            color_discrete_map={'남': '#1f77b4', '여': '#ff7f0e'}
        )
        
        # x축 레이블 포맷팅
        fig_pyramid.update_xaxes(
            tickformat=',.0f',
            tickprefix='',
            ticksuffix='명'
        )
        
        # 그래프 스타일 설정
        fig_pyramid.update_layout(
            xaxis_title="인구 수",
            yaxis_title="연령대",
            height=600,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            )
        )
        
        st.plotly_chart(fig_pyramid, use_container_width=True)
    
    # 요약 통계
    st.subheader("요약 통계")
    col3, col4 = st.columns(2)
    
    with col3:
        st.write("전체 인구 요약")
        st.dataframe(
            df_total.groupby('연령')['인구수'].agg(['sum', 'mean']).round(2)
        )
    
    with col4:
        st.write("성별 인구 요약")
        st.dataframe(
            df_gender.groupby('성별')['인구수'].agg(['sum', 'mean']).round(2)
        )

except Exception as e:
    st.error(f"데이터 로드 중 오류가 발생했습니다: {str(e)}")
    st.info("CSV 파일이 올바른 위치에 있는지 확인해주세요.")

st.title("🗺️ 클릭해서 지명을 직접 입력하고 마커 찍기")

# 지도 초기 설정
map_center = [37.5665, 126.9780]  # 서울 기준
m = folium.Map(location=map_center, zoom_start=6)

# 클릭 위치 수신
click_result = st_folium(m, width=700, height=500, returned_objects=["last_clicked"], key="input_map")

# 세션 상태에 위치 목록 저장
if "locations" not in st.session_state:
    st.session_state.locations = []

# 클릭하면 위치 입력 필드 표시
if click_result and click_result["last_clicked"]:
    lat = click_result["last_clicked"]["lat"]
    lon = click_result["last_clicked"]["lng"]
    st.success(f"선택된 위치: 위도 {lat:.5f}, 경도 {lon:.5f}")
    
    with st.form("label_form", clear_on_submit=True):
        label = st.text_input("지명 또는 장소 이름 입력", value=f"마커 {len(st.session_state.locations)+1}")
        submitted = st.form_submit_button("마커 저장")
        if submitted:
            st.session_state.locations.append({
                "label": label,
                "lat": lat,
                "lon": lon
            })
            st.toast(f"📍 '{label}' 위치가 저장되었습니다.", icon="📌")

# 저장된 마커들을 지도에 다시 표시
m2 = folium.Map(location=map_center, zoom_start=6)
for loc in st.session_state.locations:
    folium.Marker([loc["lat"], loc["lon"]], tooltip=loc["label"]).add_to(m2)

st.subheader("🗺️ 마커가 표시된 지도")
st_folium(m2, width=700, height=500, key="result_map")  # ❗ 고유 key 추가

# 목록도 텍스트로 출력
if st.session_state.locations:
    st.subheader("📋 저장된 위치 목록")
    for i, loc in enumerate(st.session_state.locations, 1):
        st.markdown(f"{i}. **{loc['label']}** - 위도: `{loc['lat']:.5f}`, 경도: `{loc['lon']:.5f}`")
else:
    st.info("아직 저장된 위치가 없습니다.") 