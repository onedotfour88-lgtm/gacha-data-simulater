# 가챠 게임 천장 시스템 및 픽뚫 메커니즘 검증 재현 패키지

본 패키지는 게임물관리위원회 모니터링 공시 규정 및 한국소비자원 실태 조사 자료를 기준 파라미터로 활용하여 가챠 게임의 '픽뚫' 및 '2단계 천장 구조'가 유저 지출 변동성에 미치는 영향을 분석하는 재현 패키지입니다.

## 구성 파일
- `scripts/run_simulation.py`: 파이썬 재현 실행 코드
- `raw_data/gacha_simulation_raw_data.csv`: 시뮬레이션 원자료 (20,000건)
- `raw_data/public_data_references.csv`: 활용한 공공 데이터 기관 및 공시 자료 출처 목록

## 실행 방법
1. VS Code에서 `reproduction_package` 폴더를 엽니다.
2. 터미널에서 `python scripts/run_simulation.py`를 실행합니다.
