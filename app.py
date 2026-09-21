import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------
# 1. 페이지 및 기본 스타일 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="가챠 천장 메커니즘 비교 시뮬레이터",
    page_icon="🎲",
    layout="wide"
)

# ---------------------------------------------------------
# 2. 시뮬레이션 핵심 로직 함수 정의
# ---------------------------------------------------------
def simulate_genshin_style(n_sim=10000):
    """원신/스타레일형: 기본 0.6%, 74회부터 Soft Pity (+6%), 90회 Hard Pity, 50% 픽뚫"""
    results = []
    for _ in range(n_sim):
        pulls = 0
        pity_count = 0
        guaranteed = False
        
        while True:
            pulls += 1
            pity_count += 1
            
            # 확률 계산 (Soft Pity 적용)
            if pity_count < 74:
                prob = 0.006
            else:
                prob = 0.006 + (pity_count - 73) * 0.06
                
            if pity_count >= 90:
                prob = 1.0
                
            # 뽑기 시도
            if np.random.rand() < prob:
                if guaranteed:
                    results.append(pulls)
                    break
                else:
                    if np.random.rand() < 0.5:
                        results.append(pulls)
                        break
                    else:
                        guaranteed = True
                        pity_count = 0
            
    return np.array(results)

def simulate_blue_archive_style(n_sim=10000):
    """블루아카/마일리지형: 기본 0.7%, 200회 천장 마일리지 교환"""
    results = []
    for _ in range(n_sim):
        pulls = 0
        got_target = False
        
        for p in range(1, 201):
            pulls = p
            if np.random.rand() < 0.007:
                got_target = True
                break
                
        results.append(pulls)
        
    return np.array(results)

def simulate_single_pity_style(n_sim=10000):
    """단일 천장형: 기본 1.5%, 80회 단일 확정 천장"""
    results = []
    for _ in range(n_sim):
        pulls = 0
        for p in range(1, 81):
            pulls = p
            if np.random.rand() < 0.015:
                break
        results.append(pulls)
        
    return np.array(results)

# ---------------------------------------------------------
# 3. 사이드바 컨트롤러 구성
# ---------------------------------------------------------
st.sidebar.title("⚙️ 시뮬레이션 설정")
n_users = st.sidebar.slider("시뮬레이션 유저 수 (N명)", min_value=1000, max_value=20000, value=10000, step=1000)

st.sidebar.subheader("🎮 비교 대상 게임 모델 선택")
model_a_name = st.sidebar.selectbox("게임 A 유형", ["원신/스타레일형 (2단계 픽뚫+보정)", "블루아카이브형 (마일리지)", "단일 천장형"], index=0)
model_b_name = st.sidebar.selectbox("게임 B 유형", ["원신/스타레일형 (2단계 픽뚫+보정)", "블루아카이브형 (마일리지)", "단일 천장형"], index=1)

# ---------------------------------------------------------
# 4. 메인 대시보드 화면 구성
# ---------------------------------------------------------
st.title("🎲 주요 게임별 가챠 천장 메커니즘 비교 시뮬레이터")
st.markdown("다양한 게임의 천장/픽뚫 방식에 따른 **유저 지출 변동성(표준편차)**과 실제 체감 확률을 시뮬레이션합니다.")

def run_selected_sim(model_name, n):
    if "원신" in model_name:
        return simulate_genshin_style(n)
    elif "블루아카" in model_name:
        return simulate_blue_archive_style(n)
    else:
        return simulate_single_pity_style(n)

# 시뮬레이션 데이터 실행
res_a = run_selected_sim(model_a_name, n_users)
res_b = run_selected_sim(model_b_name, n_users)

# ---------------------------------------------------------
# 5. 결과 시각화 및 통계 출력
# ---------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label=f"[{model_a_name}] 평균 획득 횟수", 
        value=f"{np.mean(res_a):.1f}회", 
        delta=f"표준편차: {np.std(res_a):.1f}"
    )

with col2:
    st.metric(
        label=f"[{model_b_name}] 평균 획득 횟수", 
        value=f"{np.mean(res_b):.1f}회", 
        delta=f"표준편차: {np.std(res_b):.1f}"
    )

st.divider()

# 시뮬레이션 분포 그래프 (범례 한글 깨짐 방지를 위해 깔끔한 영문 라벨 적용)
st.subheader("📊 획득 시도 횟수 분포 비교 (지출 변동성)")
fig, ax = plt.subplots(figsize=(10, 4))
sns.kdeplot(res_a, label=f"Model A ({model_a_name.split(' ')[0]})", fill=True, alpha=0.4, ax=ax)
sns.kdeplot(res_b, label=f"Model B ({model_b_name.split(' ')[0]})", fill=True, alpha=0.4, ax=ax)
ax.set_xlabel("Target Item Acquisition Pulls")
ax.set_ylabel("Density")
ax.legend()
st.pyplot(fig)

st.divider()

# 상세 통계 데이터표
st.subheader("📋 상세 통계 데이터")

stats_data = {
    "분석 지표": [
        "평균 획득 횟수 (기대값)",
        "표준편차 (지출 변동성)",
        "최소 획득 횟수",
        "최대 획득 횟수",
        "상위 10% 최악의 지출 (회)"
    ],
    f"{model_a_name}": [
        f"{np.mean(res_a):.1f}회",
        f"{np.std(res_a):.1f}",
        f"{int(np.min(res_a))}회",
        f"{int(np.max(res_a))}회",
        f"{int(np.percentile(res_a, 90))}회"
    ],
    f"{model_b_name}": [
        f"{np.mean(res_b):.1f}회",
        f"{np.std(res_b):.1f}",
        f"{int(np.min(res_b))}회",
        f"{int(np.max(res_b))}회",
        f"{int(np.percentile(res_b, 90))}회"
    ]
}

df_stats = pd.DataFrame(stats_data)
st.dataframe(df_stats, use_container_width=True)