# ==============================================================================
# 가챠 천장 시스템 및 픽뚫 메커니즘 검증 스크립트 (공공데이터 및 공시 확률 기준)
# ==============================================================================
import os
import numpy as np
import pandas as pd

def run_experiment(n_trials=10000, seed=42):
    np.random.seed(seed)
    
    print("[*] 공공기관 공시 확률 기준 가챠 천장 시뮬레이션 시작...")
    
    # System A: 단일 천장 (기본 1.5%, 80회 확정)
    results_a = []
    for _ in range(n_trials):
        pulls = 0
        while True:
            pulls += 1
            if pulls == 80 or np.random.random() < 0.015:
                results_a.append(pulls)
                break
                
    # System B: 2단계 픽뚫 천장 (기본 0.6%, 74회 보정, 90회 50% 픽뚫, 최대 180회)
    results_b = []
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
                        results_b.append(total_pulls)
                        break
                    else:
                        guaranteed = True
                        break
                        
    df_a = pd.DataFrame({"trial_id": range(1, n_trials + 1), "system": "System_A", "pulls_required": results_a})
    df_b = pd.DataFrame({"trial_id": range(1, n_trials + 1), "system": "System_B", "pulls_required": results_b})
    df_all = pd.concat([df_a, df_b], ignore_index=True)
    
    print("
[+] 시뮬레이션 완료:")
    print(f"System A 평균: {np.mean(results_a):.2f}회 | 표준편차: {np.std(results_a):.2f}")
    print(f"System B 평균: {np.mean(results_b):.2f}회 | 표준편차: {np.std(results_b):.2f}")
    
    return df_all

if __name__ == "__main__":
    df = run_experiment(10000)
    os.makedirs("raw_data", exist_ok=True)
    df.to_csv("raw_data/gacha_simulation_raw_data.csv", index=False, encoding="utf-8-sig")
    print("[+] 원자료 저장 완료: raw_data/gacha_simulation_raw_data.csv")
