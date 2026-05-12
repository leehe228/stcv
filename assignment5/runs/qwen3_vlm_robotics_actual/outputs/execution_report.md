# Execution Report

## Run Summary
- Topic: vision-language models for robot manipulation under distribution shift
- Output directory: assignment5/runs/qwen3_vlm_robotics_actual
- Verified or partially verified papers used: 5
- Generated research ideas: 3
- Critic review rounds: 2
- Offline mode: False
- Local LLM enabled: True
- Paid API usage: none

## Model Routing
- Manager/Critic/Writer: Qwen/Qwen3-4B-Instruct-2507
- Idea/Experiment roles: Qwen/Qwen3-4B-Instruct-2507
- Lightweight summarization role: Qwen/Qwen3-4B-Instruct-2507
- Reproducible fallback: deterministic-local-rules

## Local LLM Evidence
- Actual local Hugging Face generation was enabled. Raw model outputs are stored under `artifacts/llm/`.
- LLM artifacts: 8
- LLM artifact files: ['artifacts/llm/critic_iter_0_raw.json', 'artifacts/llm/critic_iter_1_raw.json', 'artifacts/llm/experiment_designer_raw.json', 'artifacts/llm/idea_generator_raw.json', 'artifacts/llm/manager_plan_raw.json', 'artifacts/llm/reviser_iter_0_raw.json', 'artifacts/llm/summarizer_related_work_raw.json', 'artifacts/llm/writer_research_brief_raw.json']

## Resource Controls
- Physical GPUs allowed by assignment: 2 and 3.
- Runtime sets `CUDA_VISIBLE_DEVICES=2,3`.
- Hugging Face cache root: `.hf_cache/` inside the repository.
- Conda environment target: `.conda/envs/stcv_hoeun` inside the repository.
- Max revision iterations: 2
- Request timeout: 8.0 seconds

## Cost and Time
```json
{
  "by_agent": {
    "Research Manager": {
      "prompt_tokens": 38,
      "completion_tokens": 216,
      "elapsed_sec": 32.33814454078674,
      "cost_usd": 0.0
    },
    "Literature Agent": {
      "prompt_tokens": 37,
      "completion_tokens": 3,
      "elapsed_sec": 10.068336009979248,
      "cost_usd": 0.0
    },
    "Citation Verifier": {
      "prompt_tokens": 31,
      "completion_tokens": 3,
      "elapsed_sec": 0.006193876266479492,
      "cost_usd": 0.0
    },
    "Paper Summarizer": {
      "prompt_tokens": 28,
      "completion_tokens": 873,
      "elapsed_sec": 14.191197633743286,
      "cost_usd": 0.0
    },
    "Idea Generator": {
      "prompt_tokens": 35,
      "completion_tokens": 365,
      "elapsed_sec": 16.939605474472046,
      "cost_usd": 0.0
    },
    "Experiment Designer": {
      "prompt_tokens": 28,
      "completion_tokens": 487,
      "elapsed_sec": 16.1347713470459,
      "cost_usd": 0.0
    },
    "Critic Reviewer": {
      "prompt_tokens": 70,
      "completion_tokens": 683,
      "elapsed_sec": 28.20471715927124,
      "cost_usd": 0.0
    },
    "Revision Agent": {
      "prompt_tokens": 31,
      "completion_tokens": 706,
      "elapsed_sec": 14.656571388244629,
      "cost_usd": 0.0
    },
    "Writer Agent": {
      "prompt_tokens": 32,
      "completion_tokens": 1811,
      "elapsed_sec": 23.49061369895935,
      "cost_usd": 0.0
    }
  },
  "total": {
    "prompt_tokens": 330,
    "completion_tokens": 5147,
    "elapsed_sec": 156.03015112876892,
    "cost_usd": 0.0
  },
  "billing_note": "No paid API was used."
}
```

## Failure Handling Notes
- Network search failures fall back to the manually curated offline seed catalog.
- Unverified or duplicate citations are written to `artifacts/rejected_papers.json`.
- If a local open-source model cannot be loaded, the event is recorded in `logs/agent_events.jsonl` with the error message.
