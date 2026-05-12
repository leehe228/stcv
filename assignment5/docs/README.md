# Assignment 5 실행 방법

## 환경 구성

모든 환경과 캐시는 repository 내부에 둔다.

```bash
cd /dataset/hoeun/stcv
CONDA_ENVS_PATH=/dataset/hoeun/stcv/.conda/envs \
CONDA_PKGS_DIRS=/dataset/hoeun/stcv/.conda/pkgs \
conda env create -f assignment5/environment.yml
```

이미 환경이 있으면 다음 명령으로 패키지를 보강할 수 있다.

```bash
CONDA_ENVS_PATH=/dataset/hoeun/stcv/.conda/envs \
CONDA_PKGS_DIRS=/dataset/hoeun/stcv/.conda/pkgs \
PIP_CACHE_DIR=/dataset/hoeun/stcv/.pip_cache \
conda run -n stcv_hoeun python -m pip install -r assignment5/requirements.txt
```

## 실행

```bash
cd /dataset/hoeun/stcv
CONDA_ENVS_PATH=/dataset/hoeun/stcv/.conda/envs \
CONDA_PKGS_DIRS=/dataset/hoeun/stcv/.conda/pkgs \
HF_HOME=/dataset/hoeun/stcv/.hf_cache \
HF_HUB_CACHE=/dataset/hoeun/stcv/.hf_cache/hub \
TRANSFORMERS_CACHE=/dataset/hoeun/stcv/.hf_cache/hub \
HF_DATASETS_CACHE=/dataset/hoeun/stcv/.hf_cache/datasets \
CUDA_VISIBLE_DEVICES=2,3 \
conda run -n stcv_hoeun python -m assignment5.research_agents.run \
  --topic "vision-language models for robot manipulation under distribution shift" \
  --max-papers 8 \
  --min-verified-papers 5 \
  --max-revision-iter 2 \
  --offline \
  --use-local-llm \
  --output assignment5/runs/qwen3_vlm_robotics_actual
```

`--use-local-llm`은 실제 Hugging Face model weight를 `.hf_cache`에 다운로드/로드한 뒤 GPU 2,3에서 generation을 수행한다. 유료 API는 사용하지 않는다.

## 테스트

```bash
cd /dataset/hoeun/stcv
CONDA_ENVS_PATH=/dataset/hoeun/stcv/.conda/envs \
CONDA_PKGS_DIRS=/dataset/hoeun/stcv/.conda/pkgs \
CUDA_VISIBLE_DEVICES=2,3 \
conda run -n stcv_hoeun pytest assignment5/tests -q
```

## 주요 산출물

- `assignment5/runs/<run_id>/outputs/research_brief.md`
- `assignment5/runs/<run_id>/outputs/execution_report.md`
- `assignment5/runs/<run_id>/logs/agent_events.jsonl`
- `assignment5/runs/<run_id>/logs/cost_summary.json`
- `assignment5/runs/<run_id>/artifacts/verified_papers.json`
