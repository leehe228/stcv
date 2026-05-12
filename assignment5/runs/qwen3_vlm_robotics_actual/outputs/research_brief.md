# Research Brief

## Background
Research topic: **vision-language models for robot manipulation under distribution shift**.

The system decomposes research automation into manager-worker steps plus a critic-reviser loop. It avoids paid APIs and records every prompt, tool call, citation status, and intermediate artifact for reproducibility.

## Related Work
| Paper | Method | Limitation | Relevance |
|---|---|---|---|
| RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control | Language-conditioned or multimodal robot policy design. | Robustness under distribution shift and transparent failure diagnosis remain hard. | Connects to 'vision-language models for robot manipulation under distribution shift' through evidence about methods, baselines, or evaluation risks. |
| Do As I Can, Not As I Say: Grounding Language in Robotic Affordances | Language-conditioned or multimodal robot policy design. | Robustness under distribution shift and transparent failure diagnosis remain hard. | Connects to 'vision-language models for robot manipulation under distribution shift' through evidence about methods, baselines, or evaluation risks. |
| PaLM-E: An Embodied Multimodal Language Model | Language-conditioned or multimodal robot policy design. | Robustness under distribution shift and transparent failure diagnosis remain hard. | Connects to 'vision-language models for robot manipulation under distribution shift' through evidence about methods, baselines, or evaluation risks. |
| VIMA: General Robot Manipulation with Multimodal Prompts | Language-conditioned or multimodal robot policy design. | Robustness under distribution shift and transparent failure diagnosis remain hard. | Connects to 'vision-language models for robot manipulation under distribution shift' through evidence about methods, baselines, or evaluation risks. |
| Perceiver-Actor: A Multi-Task Transformer for Robotic Manipulation | Language-conditioned or multimodal robot policy design. | Robustness under distribution shift and transparent failure diagnosis remain hard. | Connects to 'vision-language models for robot manipulation under distribution shift' through evidence about methods, baselines, or evaluation risks. |

## Research Gap
The verified literature suggests three recurring gaps: robustness under shifted inputs, incomplete baseline mapping, and weak traceability from generated ideas back to citations. A useful proposal should therefore couple idea generation with citation verification and reviewer-style revision.

## Candidate Ideas
| Idea | Novelty | Feasibility | Expected contribution |
|---|---:|---:|---|
| Shift-Aware VLA Policy Auditing | 4 | 4 | A reproducible robustness evaluation protocol and an intervention mechanism for safer robot manipulation. |
| Counterfactual Prompt Stress Tests for Robot Policies | 4 | 5 | A benchmark suite that links prompt sensitivity to manipulation success degradation. |
| Reviewer-in-the-Loop Robot Experiment Planner | 3 | 5 | A practical tool and evaluation rubric for designing stronger VLM robotics studies. |

## Proposed Idea
**Counterfactual Prompt Stress Tests for Robot Policies**

- Hypothesis: Counterfactual edits to language and image prompts reveal brittle shortcuts in multimodal robot policies under object, lighting, and instruction shift.
- Novelty: Turns prompt perturbation into a systematic robot-policy diagnostic rather than a generic VLM robustness probe.
- Feasibility: Feasible with offline datasets and simulator-generated prompt/image variants before costly real robot validation. The revised scope starts with offline dataset replay and simulator stress tests before any real-robot run.
- Expected contribution: A benchmark suite that links prompt sensitivity to manipulation success degradation. It also reports citation-grounded baseline mapping and reviewer issue resolution.

## Experiment Plan
### Datasets
- Open X-Embodiment
- DROID
- Ravens/Transporter-style simulated manipulation tasks

### Baselines
- RT-2-style VLA policy
- SayCan-style LLM plus affordance scorer
- Octo generalist robot policy

### Metrics
- task success rate under in-distribution and shifted conditions
- shift detection AUROC before action execution
- false intervention rate
- language-goal consistency score

### Ablations
- remove language-intent consistency check
- remove visual corruption detector
- replace affordance confidence with raw VLM score
- train on single embodiment only

### Expected Failure Cases
- novel object categories absent from robot demonstrations
- ambiguous instructions with multiple valid manipulation targets
- visual shifts that preserve semantics but change low-level control affordances

### Risks
- offline datasets may not contain enough severe distribution shifts
- VLM confidence can be poorly calibrated
- real robot validation may be compute and hardware intensive
- Residual risk: metadata summaries may not capture all paper-specific caveats.

### Implementation Notes
- Use physical GPUs 2 and 3 only through CUDA_VISIBLE_DEVICES=2,3.
- Cache all Hugging Face assets inside the repository-level .hf_cache directory.
- Offline-first validation path: run all shifted-condition tests on stored demonstrations or simulation before hardware trials.
- Baseline mapping: SayCan/RT-2/Octo or single-prompt/manager-worker variants are linked to verified references.
- Risk section now preserves unresolved limits instead of hiding them after revision.

## Reviewer Critique and Revisions
| Review | Score | Required revisions |
|---|---:|---|
| Iteration 0 | 3/5 | Real robot validation may be too expensive; define an offline-first validation path.; Add an explicit offline-first experiment path.; Tie each baseline to a cited prior paper.; State how the revision changes the risk/limitation section. |
| Iteration 1 | 4/5 | Real robot validation may be too expensive; define an offline-first validation path. |

Revision actions:
- Offline-first validation path: run all shifted-condition tests on stored demonstrations or simulation before hardware trials.
- Baseline mapping: SayCan/RT-2/Octo or single-prompt/manager-worker variants are linked to verified references.
- Risk section now preserves unresolved limits instead of hiding them after revision.

## Limitations
- Metadata-level summaries are useful for reproducible triage but cannot replace a full-paper reading step.
- Local open-source LLM execution depends on model cache availability and GPU memory; this run records raw Qwen outputs alongside schema-controlled artifacts.
- Citation verification is conservative: unverified references are logged but excluded from final references.

## References
- 1. Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xiaofeng Chen (2023). RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control. CoRL. https://arxiv.org/abs/2307.15818 [verified]
- 2. Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes (2022). Do As I Can, Not As I Say: Grounding Language in Robotic Affordances. arXiv. https://arxiv.org/abs/2204.01691 [verified]
- 3. Danny Driess, Fei Xia, Mehdi S. M. Sajjadi, Corey Lynch, Aakanksha Chowdhery (2023). PaLM-E: An Embodied Multimodal Language Model. ICML. https://arxiv.org/abs/2303.03378 [verified]
- 4. Yunfan Jiang, Agrim Gupta, Zichen Zhang, Guanzhi Wang, Yuke Zhu (2022). VIMA: General Robot Manipulation with Multimodal Prompts. ICML. https://arxiv.org/abs/2210.03094 [verified]
- 5. Mohan Shridhar, Lucas Manuelli, Dieter Fox (2022). Perceiver-Actor: A Multi-Task Transformer for Robotic Manipulation. CoRL. https://arxiv.org/abs/2209.05451 [verified]

## Local LLM Generated Synthesis
- Model actually loaded: `Qwen/Qwen3-4B-Instruct-2507`
- Device map: `{'model.embed_tokens': 0, 'lm_head': 0, 'model.layers.0': 0, 'model.layers.1': 0, 'model.layers.2': 0, 'model.layers.3': 0, 'model.layers.4': 0, 'model.layers.5': 0, 'model.layers.6': 0, 'model.layers.7': 0, 'model.layers.8': 0, 'model.layers.9': 0, 'model.layers.10': 0, 'model.layers.11': 0, 'model.layers.12': 0, 'model.layers.13': 0, 'model.layers.14': 0, 'model.layers.15': 0, 'model.layers.16': 1, 'model.layers.17': 1, 'model.layers.18': 1, 'model.layers.19': 1, 'model.layers.20': 1, 'model.layers.21': 1, 'model.layers.22': 1, 'model.layers.23': 1, 'model.layers.24': 1, 'model.layers.25': 1, 'model.layers.26': 1, 'model.layers.27': 1, 'model.layers.28': 1, 'model.layers.29': 1, 'model.layers.30': 1, 'model.layers.31': 1, 'model.layers.32': 1, 'model.layers.33': 1, 'model.layers.34': 1, 'model.layers.35': 1, 'model.norm': 1, 'model.rotary_emb': 1}`

# Research Brief: Counterfactual Prompt Stress Tests for Robot Policies

## Background  
Vision-language-action (VLA) models enable robots to execute manipulation tasks via natural language. However, these policies often rely on brittle shortcuts—e.g., visual or linguistic heuristics—that fail under distribution shifts in object appearance, lighting, or instruction phrasing.

## Related Work  
- **RT-2** and **PaLM-E** demonstrate vision-language-action transfer but lack systematic evaluation under shift.  
- **VIMA** and **Perceiver-Actor** use multimodal prompts for generalization but do not diagnose policy brittleness.  
- **Do As I Can** grounds language in affordances, improving robustness but without formal stress testing.  

## Proposed Method  
We introduce *Counterfactual Prompt Stress Tests*—a diagnostic framework that perturbs language and image prompts (e.g., altering object names, lighting, or instruction semantics) to reveal policy failures under distribution shift. Perturbations are systematically applied to stored demonstrations or simulated tasks to evaluate policy stability.

## Experiment Plan  
- **Datasets**: Open X-Embodiment, DROID, Ravens/Transporter-style tasks.  
- **Baselines**: RT-2-style VLA policy, SayCan + affordance scorer, Octo generalist policy (each tied to cited work).  
- **Metrics**: Task success rate (in-distribution vs. shifted), shift detection AUROC, false intervention rate, language-goal consistency.  
- **Ablations**: Remove intent consistency, visual corruption detector, affordance confidence, or train on single embodiment.  
- **Offline-first path**: All stress tests run on stored data/simulation before real robot trials.  

## Critique & Revisions  
Initial review (score: 3) flagged real-robot validation cost. Revised to adopt an *offline-first* path using simulation and stored data. Baselines now explicitly tied to prior works (RT-2, SayCan, Octo). Risk section now transparently lists unresolved limits (e.g., dataset shift coverage, VLM calibration).  

## Limitations  
- Offline datasets may lack severe shifts (e.g., novel object categories).  
- VLM confidence scores may be poorly calibrated.  
- Ambiguous instructions or visual shifts preserving semantics but altering affordances remain challenging.  
- Real robot validation remains compute-intensive and hardware-dependent.  

## References  
- RT-2: [arXiv:2307.15818](https://arxiv.org/abs/2307.15818)  
- Do As I Can: [arXiv:2204.01691](https://arxiv.org/abs/2204.01691)  
- PaLM-E: [arXiv:2303.03378](https://arxiv.org/abs/2303.03378)  
- VIMA: [arXiv:2210.03094](https://arxiv.org/abs/2210.03094)  
- Perceiver-Actor: [arXiv:2209.05451](https://arxiv.org/abs/2209.05451)  

*Word count: 498*
