import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="주요 게임별 가챠 천장 및 픽뚫 비교 시뮬레이터", layout="wide")

st.title("🎲 주요 게임별 가챠 천장 메커니즘 비교 시뮬레이터")
st.markdown("다양한 게임의 천장/픽뚫 방식(원신/스타레일형, 블루 아카이브형, 단일 천장형 등)에 따른 **유저 지출 변동성(표준편차)과 실제 체감 확률**을 시뮬레이션합니다.")

st.sidebar.header("⚙️ 시뮬레이션 설정")
n_trials = st.sidebar.slider("시뮬레이션 유저 수 (N명)", min_value=1000, max_value=30000, value=10000, step=1000)

st.sidebar.subheader("🎮 비교 대상 게임 모델 선택")
game_a_type = st.sidebar.selectbox("게임 A 유형", ["원신/스타레일형 (2단계 픽뚫+보정)", "블루 아카이브형 (200천장 마일리지)", "단일 천장형 (80회 확정)"], index=0)
game_b_type = st.sidebar.selectbox("게임 B 유형", ["블루 아카이브형 (200천장 마일리지)", "원신/스타레일형 (2단계 픽뚫+보정)", "단일 천장형 (80회 확정)"], index=1)

def simulate_genshin(n_trials):
    # 기본 0.6%, 74회부터 보정(Soft Pity), 90회 천장, 50% 픽뚫, 180회 확정
    results = []
    for _ in range(n_trials):
        total_pulls = 0
        guaranteed = False
        target = False
        while not target:
            pulls_in_banner = 0
            while True:
                pulls_in_banner += 1
                total_pulls += 1
                prob = 0.006 + max(0, (pulls_in_banner - 73) * 0.06)
                if np.random.random() < min(prob, 1.0) or pulls_in_banner == 90:
                    if guaranteed or np.random.random() < 0.5:
                        target = True
                        results.append(total_pulls)
                        break
                    else:
                        guaranteed = True
                        break
    return results

def simulate_blue_archive(n_trials):
    # 픽업 확률 0.7%, 보정 없음, 200회 교환소 확정 천장
    results = []
    for _ in range(n_trials):
        pulls = 0
        target = False
        while not target:
            pulls += 1
            if pulls == 200:
                target = True
                results.append(200)
                break
            if np.random.random() < 0.007:
                target = True
                results.append(pulls)
                break
    return results

def simulate_single_pity(n_trials):
    # 기본 1.5%, 80회 확정 천장
    results = []
    for _ in range(n_trials):
        pulls = 0
        while True:
            pulls += 1
            if pulls == 80 or np.random.random() < 0.015:
                results.append(pulls)
                break
    return results

def run_sim(game_type, n):
    if "원신" in game_type:
        return simulate_genshin(n)
    elif "블루 아카이브" in game_type:
        return simulate_blue_archive(n)
    else:
        return simulate_single_pity(n)

if st.sidebar.button("🚀 시뮬레이션 실행"):
    np.random.seed(42)
    
    with st.spinner("시뮬레이션 계산 중..."):
        res_a = run_sim(game_a_type, n_trials)
        res_b = run_sim(game_b_type, n_trials)
        
    st.subheader("📊 핵심 지표 비교")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(f"[{game_a_type.split()[0]}] 평균 획득", f"{np.mean(res_a):.1f}회")
    c2.metric(f"[{game_a_type.split()[0]}] 상위 10% 최악(비용 위험도)", f"{np.percentile(res_a, 90):.0f}회")
    c3.metric(f"[{game_b_type.split()[0]}] 평균 획득", f"{np.mean(res_b):.1f}회")
    c4.metric(f"[{game_b_type.split()[0]}] 상위 10% 최악(비용 위험도)", f"{np.percentile(res_b, 90):.0f}회")
    
    st.markdown("---")
    
    st.subheader("📈 유저 뽑기 횟수 분포 비교 (히스토그램)")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.hist(res_a, bins=40, alpha=0.5, label=game_a_type.split()[0], color="crimson")
    ax.hist(res_b, bins=40, alpha=0.5, label=game_b_type.split()[0], color="royalblue")
    ax.set_xlabel("Required Pulls (획득까지 필요한 뽑기 횟수)")
    ax.set_ylabel("User Count (유저 수)")
    ax.set_title("Distribution of Required Pulls")
    ax.legend()
    st.pyplot(fig)
    
    st.subheader("📋 상세 통계 데이터")
    summary_df = pd.DataFrame({
        "구분": [game_a_type.split()[0], game_b_type.split()[0]],
        "평균 획득 횟수": [f"{np.mean(res_a):.2f}회", f"{np.mean(res_b):.2f}회"],
        "중앙값(50%)": [f"{np.median(res_a):.0f}회", f"{np.median(res_b):.0f}회"],
        "표준편차(변동성)": [f"{np.std(res_a):.2f}", f"{np.std(res_b):.2f}"],
        "상위 10% 최악의 경우": [f"{np.percentile(res_a, 90):.0f}회", f"{np.percentile(res_b):.0f}회"],
        "최대 뽑기 횟수": [f"{np.max(res_a)}회", f"{np.max(res_b)}회"]
    })
    st.table(summary_df)