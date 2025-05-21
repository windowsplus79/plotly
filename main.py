import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import koreanize_matplotlib
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(
    page_title="인구 현황 분석",
    page_icon="📊",
    layout="wide"
)

# 한글 폰트 설정
plt.rcParams['font.family'] = 'NanumGothic'
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