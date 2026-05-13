# PowerPoint Slide Content

## Slide 1. 설계

**제목:** Multi-Agent Research Automation 설계

**핵심 메시지:**  
단일 LLM 호출이 아니라, 연구 주제 입력부터 논문 검증, 아이디어 생성, 실험 설계, 리뷰-수정, 최종 research brief 작성까지 이어지는 재현 가능한 multi-agent workflow를 설계했다.

**슬라이드 본문:**
- 입력: 사용자가 자연어 연구 주제를 입력
  - 예시 topic: `vision-language models for robot manipulation under distribution shift`
- 목표:
  - 관련 논문 탐색 및 citation 검증
  - 검증 논문 요약 및 related work table 생성
  - 최소 3개 연구 아이디어 생성
  - 선택 아이디어에 대한 dataset, baseline, metric, ablation, risk 포함 실험 계획 생성
  - Critic/Reviewer의 지적을 Revision Agent가 실제 반영
  - 최종 `research_brief.md`, 실행 로그, 비용 요약, 중간 JSON artifact 저장
- 설계 원칙:
  - Agent별 책임 분리
  - Pydantic schema 기반 구조화된 입출력
  - Citation hallucination 방지를 위한 verifier 단계
  - 최대 반복 횟수, timeout, retry, fallback으로 무한 루프 방지

**발표 포인트:**
- `assignment5/docs/design.md`의 표현처럼 이 시스템은 “manager-worker 구조와 critic-reviser loop”를 결합한다.
- 모든 중간 결과를 `artifacts/`, 최종 문서를 `outputs/`, 실행 이벤트를 `logs/`에 저장해 결과를 추적할 수 있다.

---

## Slide 2. 아키텍처

**제목:** Agent Pipeline 및 데이터 흐름

**핵심 메시지:**  
전체 시스템은 Research Manager가 계획을 세우고, Literature/Verifier/Summarizer/Idea/Experiment/Critic/Reviser/Writer agent가 순차적으로 artifact를 생성하는 구조다.

**슬라이드 본문:**
- 실행 흐름:
  1. `Research Manager`: 검색 query, workflow, stopping rule 생성
  2. `Literature Agent`: arXiv, OpenAlex, Semantic Scholar, offline seed에서 논문 후보 수집
  3. `Citation Verifier`: metadata 검증, 중복 제거, rejected paper 분리
  4. `Paper Summarizer`: 검증 논문별 핵심 주장, 방법, 실험, 한계 요약
  5. `Idea Generator`: 연구 gap 기반 candidate idea 생성
  6. `Experiment Designer`: 선택 idea의 실험 계획 작성
  7. `Critic Reviewer`: reviewer-style critique 수행
  8. `Revision Agent`: critique 반영
  9. `Writer Agent`: 최종 research brief 작성
- Critic loop stopping rule:
  - `score >= 4`이면 조기 종료
  - 아니면 `max_revision_iter`까지 수정 반복
- 저장 구조:
  - `artifacts/*.json`: 구조화된 중간 결과
  - `artifacts/llm/*.json`: 실제 Qwen raw output
  - `outputs/*.md`: 최종 제출용 Markdown
  - `logs/*.jsonl`, `logs/cost_summary.json`: 실행 추적 및 비용 요약

**도식 추천:**
```text
User Topic
  -> Manager
  -> Literature Search
  -> Citation Verifier
  -> Paper Summarizer
  -> Idea Generator
  -> Experiment Designer
  -> Critic Reviewer
  -> Revision Agent, if needed
  -> Writer
  -> Research Brief
```

**발표 포인트:**
- 구현 기준 핵심 파일은 `assignment5/research_agents/workflow.py`, `run.py`, `config.py`, `schemas.py`이다.
- `workflow.py`에서 실제 agent 객체를 생성하고, 각 단계 결과를 다음 agent 입력으로 넘긴다.

---

## Slide 3. 실행 환경 및 실험 세팅

**제목:** Local Open-Source LLM 기반 실행 환경

**핵심 메시지:**  
유료 API 없이 `Qwen/Qwen3-4B-Instruct-2507`을 로컬 Hugging Face inference로 실행했으며, GPU 2, 3만 사용하도록 고정했다.

**슬라이드 본문:**
- 실제 run directory:
  - `assignment5/runs/qwen3_vlm_robotics_actual/`
- 실행 topic:
  - `vision-language models for robot manipulation under distribution shift`
- 모델 라우팅:
  - Manager/Critic/Writer: `Qwen/Qwen3-4B-Instruct-2507`
  - Idea/Experiment roles: `Qwen/Qwen3-4B-Instruct-2507`
  - Lightweight summarization: `Qwen/Qwen3-4B-Instruct-2507`
  - fallback: `deterministic-local-rules`
- Runtime config:
  - `max_papers = 8`
  - `min_verified_papers = 5`
  - `max_revision_iter = 2`
  - `request_timeout_sec = 8.0`
  - `temperature = 0.2`
  - `max_new_tokens = 768`
- Resource controls:
  - `CUDA_VISIBLE_DEVICES=2,3`
  - Hugging Face cache: repository-local `.hf_cache/`
  - Conda environment: `.conda/envs/stcv_hoeun`
- 실행 명령 요약:
```bash
python -m assignment5.research_agents.run \
  --topic "vision-language models for robot manipulation under distribution shift" \
  --max-papers 8 \
  --min-verified-papers 5 \
  --max-revision-iter 2 \
  --use-local-llm \
  --output assignment5/runs/qwen3_vlm_robotics_actual
```

**결과 파일 직접 인용:**
- `outputs/execution_report.md`: “Local LLM enabled: True”
- `outputs/execution_report.md`: “Paid API usage: none”
- `outputs/execution_report.md`: “Runtime sets `CUDA_VISIBLE_DEVICES=2,3`.”
- `outputs/execution_report.md`: “LLM artifacts: 8”

---

## Slide 4. 결과

**제목:** 실제 산출물 기반 결과 요약

**핵심 메시지:**  
실제 실행은 검증 논문 5편, 연구 아이디어 3개, critic review 2회를 생성했고, 최종적으로 `Counterfactual Prompt Stress Tests for Robot Policies`를 제안 아이디어로 선택했다.

**슬라이드 본문:**
- Run summary:
  - Verified or partially verified papers used: `5`
  - Generated research ideas: `3`
  - Critic review rounds: `2`
  - Paid API cost: `$0.00`
  - Total measured agent time: `156.03 sec`
  - Prompt tokens: `330`
  - Completion tokens: `5147`
- 검증된 reference 5편:
  - RT-2, 2023, CoRL
  - Do As I Can / SayCan, 2022, arXiv
  - PaLM-E, 2023, ICML
  - VIMA, 2022, ICML
  - Perceiver-Actor, 2022, CoRL
- 생성된 아이디어:
  - `Shift-Aware VLA Policy Auditing` - novelty 4, feasibility 4
  - `Counterfactual Prompt Stress Tests for Robot Policies` - novelty 4, feasibility 5
  - `Reviewer-in-the-Loop Robot Experiment Planner` - novelty 3, feasibility 5
- 최종 선택 아이디어:
  - `Counterfactual Prompt Stress Tests for Robot Policies`
  - 가설: “Counterfactual edits to language and image prompts reveal brittle shortcuts in multimodal robot policies under object, lighting, and instruction shift.”
- 실험 계획:
  - Datasets: Open X-Embodiment, DROID, Ravens/Transporter-style simulated manipulation tasks
  - Baselines: RT-2-style VLA policy, SayCan-style LLM plus affordance scorer, Octo generalist robot policy
  - Metrics: task success rate, shift detection AUROC, false intervention rate, language-goal consistency score
  - Ablations: intent consistency 제거, visual corruption detector 제거, affordance confidence 대체, single embodiment training
- Critic 및 revision 결과:
  - Iteration 0: score `3/5`
  - 지적: “Real robot validation may be too expensive; define an offline-first validation path.”
  - Revision 반영: offline dataset replay 및 simulation stress test를 먼저 수행하는 검증 경로 추가
  - Iteration 1: score `4/5`, `stop: true`

**결과 파일 직접 인용/근거:**
- `outputs/research_brief.md`: “The system decomposes research automation into manager-worker steps plus a critic-reviser loop.”
- `outputs/research_brief.md`: “The revised scope starts with offline dataset replay and simulator stress tests before any real-robot run.”
- `artifacts/experiment_plan.json`: “Use physical GPUs 2 and 3 only through CUDA_VISIBLE_DEVICES=2,3.”
- `artifacts/review_report_iter_1.json`: `overall_score = 4`, `stop = true`
- `outputs/related_work_table.md`: 기존 VLA/robotics 연구의 공통 한계로 “Robustness under distribution shift and transparent failure diagnosis remain hard.”가 반복적으로 정리됨

**시각 자료 추천:**
- 왼쪽: 5개 verified paper 표
- 가운데: 3개 candidate idea 점수표
- 오른쪽: critic iteration 변화 `3/5 -> 4/5`와 최종 선택 아이디어
