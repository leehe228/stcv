# Special Topics in Computer Vision (STCV) Assignment #5

- **제출기한:** 5/4(월) / 수업시간 전
- **주제:** Multi-agent 연구 자동화 시스템 개발

## 과제 질문

**Q:** 최신 multi-agent AI 모델 및 agent framework를 이용하여, 연구 주제 탐색·논문 조사·아이디어 생성·실험 설계·비판적 검증·보고서 작성까지 지원하는 연구 자동화 시스템을 만들 수 있는가?

## 조건

- 본 과제의 목표는 단일 LLM 호출이 아니라, 서로 다른 역할을 갖는 복수의 AI agent가 협업하여 하나의 연구 자동화 workflow를 수행하도록 설계·구현하는 데 있다.
- 학생은 연구 문제를 입력하면 관련 논문 탐색, 핵심 주장 요약, novelty 검토, 새로운 연구 아이디어 생성, 실험 계획 수립, reviewer-style critique, 최종 research brief 작성까지 이어지는 multi-agent system을 개발해야 한다.
- 구현 과정에서는 AI coding tool, LLM API, agent framework, 검색 API, 문서 처리 도구 등을 사용할 수 있으나, 각 agent의 역할·입출력·상호작용·검증 절차가 명확히 드러나야 한다.

---

## 1. 학습 목표

- Multi-agent AI system의 기본 구조(manager-worker, planner-executor, critic-reviser, debate, voting 등)를 이해하고 구현하는 능력 배양
- 연구 자동화 과정에서 필요한 역할을 agent 단위로 분해하고, 각 agent의 책임·입력·출력을 명확히 정의하는 능력 습득
- 논문 탐색, 요약, 비교, novelty 분석, 실험 설계, 비판적 검토를 하나의 workflow로 연결하는 능력 배양
- LLM의 hallucination, 근거 없는 citation, 역할 중복, 무한 반복, 비용 증가 등의 문제를 탐지하고 완화하는 방법 학습
- 프롬프트, agent 로그, 실행 결과, 실패 사례, 평가 지표를 체계적으로 기록하여 재현 가능한 연구 자동화 과정을 문서화하는 태도 경험

---

## 2. 과제 수행 원칙

- 반드시 3개 이상의 독립적 agent를 포함해야 하며, 권장 구성은 Research Manager, Literature Agent, Idea Generator, Experiment Designer, Critic/Reviewer, Writer/Presenter 중 4개 이상이다.
- 단일 프롬프트로 긴 답변을 생성하는 방식은 multi-agent 시스템으로 인정하지 않는다.
- agent 간 message passing, task decomposition, iterative revision, debate 또는 voting 중 하나 이상의 협업 메커니즘을 구현해야 한다.
- 외부 논문·자료를 사용할 경우, 논문 제목, 저자, 연도, URL 또는 DOI 등 검증 가능한 근거를 남겨야 한다.
- 존재하지 않는 논문이나 citation을 생성한 경우 감점 대상이 된다.
- 학생은 AI coding tool을 활용할 수 있으나, 최종 보고서에는 사용한 tool, 모델, prompt, agent interaction log, 오류 수정 과정이 포함되어야 한다.
- 자동화 시스템의 결과를 그대로 신뢰하지 말고, 최소 1개의 verification 또는 critique 단계를 포함해야 한다.
- 비용과 실행시간을 고려하여 고성능 모델은 manager, critic, final writer와 같은 핵심 agent에 우선 배치하고, 단순 요약·분류 agent에는 경량 모델을 사용하는 것을 권장한다.
- API key, 개인정보, 비공개 논문, 연구실 내부 자료가 외부로 노출되지 않도록 주의해야 하며, 실제 계정·파일·이메일을 연결하는 경우 sandbox 환경을 사용해야 한다.

---

## 3. 필수 기능 요구사항

| No. | 기능 항목 | 세부 요구사항 | 필수 여부 |
|---:|---|---|---|
| 1 | 연구 주제 입력 | 사용자가 자연어로 연구 분야, 문제의식, 키워드, 제약 조건을 입력할 수 있어야 한다. | 필수 |
| 2 | Agent 역할 분리 | 최소 3개 이상의 agent를 명확히 정의하고, 각 agent의 역할, 입력, 출력, 사용 모델 또는 prompt를 문서화해야 한다. JSON/Pydantic 스키마 사용을 권장한다. | 필수 |
| 3 | 논문/자료 탐색 | arXiv, Semantic Scholar, Crossref, OpenAlex, Papers with Code, web search 또는 사용자가 제공한 PDF/문서를 활용할 수 있어야 한다. API rate limit 및 할당량 관리 로직 포함을 권장한다. | 필수 |
| 4 | 논문 요약 및 비교 | 최소 5편 이상의 논문 또는 자료를 정리해야 하며, 핵심 주장, 방법, 실험, 한계, 관련성을 비교해야 한다. PDF 파싱 시 텍스트 유실 방지 대책을 고려한다. | 필수 |
| 5 | 아이디어 생성 | 차별화된 연구 아이디어를 최소 3개 이상 생성하고, 각 아이디어에 대해 novelty, feasibility, expected contribution을 설명해야 한다. | 필수 |
| 6 | 실험 설계 | 아이디어 1개 이상에 대해 dataset, baseline, metric, ablation, expected failure case, risk를 포함한 실험 계획을 제시해야 한다. | 필수 |
| 7 | Critic/Reviewer 단계 | 생성된 아이디어와 실험 계획을 비판적으로 평가하고, 약점·위험요인·개선안을 제시하는 agent 또는 단계가 포함되어야 한다. | 필수 |
| 8 | 반복 개선 루프 | critic의 지적을 바탕으로 revision step을 수행해야 한다. 무한 루프 방지를 위해 max iteration 또는 stopping rule을 명시해야 한다. | 필수 |
| 9 | 최종 산출물 생성 | 배경, 관련 연구, 제안 방법, 실험 계획, 한계, 참고문헌을 포함한 research brief 또는 mini-proposal을 생성해야 한다. | 필수 |
| 10 | 실행 로그 저장 | agent 별 입출력, 프롬프트, 모델명, 실행 순서, tool call, 오류 수정 과정을 로그 파일로 남겨야 한다. | 필수 |
| 11 | 사용자 인터페이스 | CLI, notebook, web UI 중 하나로 연구 주제 입력 및 결과 확인이 가능해야 한다. | 권장 |
| 12 | 비용/성능 분석 | token 사용량, 실행시간, 비용 추정, 사용 모델별 역할 분배의 타당성을 분석해야 한다. | 권장 |

---

## 4. 권장 기술 스택 및 기술적 주의사항

- **Agent framework:** LangGraph, AutoGen, CrewAI, OpenAI Agents SDK, LlamaIndex workflow, Semantic Kernel 등 사용 권장
- **LLM 모델:** GPT-4o/mini, Claude 3.5, Gemini 1.5 Pro/Flash 등 작업 부하에 따라 선택. Llama 계열 local/open-weight model 사용 가능
- **논문/자료 검색:** arXiv API, Semantic Scholar API, Crossref API, OpenAlex, Papers with Code, web search, 사용자가 제공한 PDF/문서 기반 RAG 등 사용 가능
- **문서 처리 및 안정성:** PyMuPDF, Marker 등을 활용한 정교한 PDF parsing, metadata extraction, citation verification 기능 권장
- **Agent 간 데이터 규격화:** Pydantic 또는 JSON Schema를 이용하여 agent 별 입력·출력 형식을 명확히 정의할 것을 권장
- **캐싱 및 비용 제어:** 중복 요청 방지를 위한 SQLite 기반 caching layer, API rate limit 처리, 최대 루프 횟수(max iterations), token limit, timeout 설정 권장
- **구현 언어:** Python을 권장하되, JavaScript/TypeScript 기반 구현도 허용한다.
- **중요:** 단순 chatbot이 아니라 agent 간 역할 분담과 상호작용이 드러나는 구조여야 한다. workflow graph, sequence diagram, message log 중 하나 이상을 제출해야 한다.
- **중요:** 검색 결과나 논문 정보를 사용할 경우 citation hallucination을 방지하기 위한 verification step을 포함해야 한다.

---

## 5. 구현 절차

1. 과제 요구사항을 기능 단위로 재정리한다. 예: 주제 입력, 논문 검색, 논문 요약, 연구 gap 분석, 아이디어 생성, 실험 설계, critic review, revision, 최종 보고서 생성.
2. 전체 agent architecture를 설계한다. 각 agent의 이름, 역할, 입력, 출력, 사용 모델, 사용 tool, 다음 agent로 전달되는 정보를 표로 정리한다.
3. 2~3개 agent 기반의 MVP(Minimum Viable Product)를 먼저 구축하여, 간단한 research topic 1개에 대해 end-to-end workflow가 실행되는지 확인한다.
4. AI coding tool 또는 agent framework에게 프로젝트 생성 프롬프트를 제공한다. 필수 agent, workflow, 외부 검색 방식, 로그 저장 방식, 최종 산출물 형식을 명확히 지시한다.
5. 논문 검색 및 파싱 파이프라인을 연결하고, 검색 결과의 제목·저자·연도·링크가 정상적으로 수집되는지 확인한다. API rate limit, network error, PDF parsing failure에 대한 에러 핸들링을 포함한다.
6. Literature Agent가 수집된 자료를 요약하고, Related Work 표를 생성하도록 구현한다.
7. Idea Generator가 여러 연구 아이디어를 생성하도록 하고, 각 아이디어의 novelty와 feasibility를 별도로 평가하도록 지시한다.
8. Experiment Designer가 선택된 아이디어에 대해 dataset, baseline, metric, ablation, expected failure case를 포함한 실험 계획을 작성하도록 한다.
9. Critic/Reviewer Agent가 아이디어와 실험 계획을 비판적으로 검토하게 하고, Revision Agent 또는 Manager Agent가 그 결과를 반영하여 개선안을 생성하도록 한다.
10. 최종 Writer Agent가 전체 결과를 research brief, mini proposal, 또는 발표자료 개요 형태로 정리하게 한다.
11. 실행 중 발생한 오류, 부정확한 citation, 중복된 agent 역할, 긴 실행시간, 비용 문제를 기록하고 개선한다.
12. 최종적으로 프롬프트 로그, agent interaction log, 실행 화면, 결과 파일, 보고서를 정리하여 제출한다.

---

## 6. AI Tool 또는 Agent에게 제공해야 할 지시문의 수준

단순히 “연구 자동화 agent를 만들어줘”와 같이 모호한 프롬프트를 쓰지 말고, 구현 가능한 수준의 구체적 요구를 AI에게 전달해야 한다. 다음 항목을 반드시 포함할 것을 권장한다.

- **시스템 목적:** 연구 주제 입력을 받아 관련 논문 탐색, 요약, gap 분석, 아이디어 생성, 실험 설계, critique, revision, 최종 보고서 작성을 수행하는 multi-agent research assistant
- **Agent 구성:** Research Manager, Literature Searcher, Paper Summarizer, Idea Generator, Experiment Designer, Critic/Reviewer, Writer 등
- **협업 방식:** 순차 workflow, manager-worker 구조, critic-revise loop, debate/voting 구조 중 사용할 방식을 명시
- **입출력 형식:** 각 agent의 입력과 출력 schema, JSON 또는 Markdown 형식, 최종 report 형식
- **자료 검증:** 논문 제목·저자·연도·링크를 확인하고, 불확실한 자료는 “unverified”로 표시하도록 지시
- **제약 조건:** 최소 검색 논문 수, 최소 생성 아이디어 수, revision 횟수, citation format, 비용 제한, 실행시간 제한
- **검증 요청:** hallucination check, duplicate paper check, novelty check, feasibility check, reviewer-style critique를 포함하도록 지시
- **재현성:** 모든 prompt, model setting, temperature, tool call, 주요 intermediate output을 저장하도록 지시

---

## 7. 테스트 및 검증 기준

- 사용자가 연구 주제를 입력하면 전체 workflow가 중단 없이 실행되는가? 예외 처리와 재시도 로직이 적절한가?
- 각 agent의 역할이 명확히 구분되어 있으며, 단일 LLM 응답을 agent 이름만 바꾸어 나열한 형태가 아닌가?
- 관련 논문 또는 자료가 실제 존재하며, 제목·저자·연도·링크가 검증 가능한가? Citation hallucination이 탐지되는가?
- 수집된 논문 요약이 원 논문의 핵심 주장과 크게 어긋나지 않는가?
- 생성된 연구 아이디어가 기존 연구와 명확히 구별되는 novelty를 갖는가?
- 실험 계획이 실제 수행 가능한 수준으로 dataset, baseline, metric, ablation, risk를 포함하는가?
- Critic/Reviewer agent가 형식적인 칭찬이 아니라 구체적인 약점과 개선안을 제시하는가?
- Critic의 지적이 revision 단계에 실제로 반영되는가?
- 최대 실행 루프 제한, token 제한, timeout, 비용 제어 로직이 작동하는가?
- 최종 research brief가 background, related work, proposed method, experiment plan, limitation, references를 포함하는가?
- 동일한 입력에 대해 여러 번 실행했을 때 결과가 지나치게 불안정하지 않은가?
- 실행 로그와 프롬프트 기록을 통해 다른 사람이 재현할 수 있는가?
- token 사용량, 실행시간, 비용이 과도하지 않은가?

---

## 8. 평가 기준

| 평가 항목 | 비중 | 세부 기준 |
|---|---:|---|
| 문제 설정 및 창의성 | 15% | 연구 자동화 문제 정의가 명확하고 흥미로운가? 입력 주제와 최종 산출물이 잘 연결되는가? |
| Agent 설계 | 20% | agent 역할, 입출력 스키마, 협업 구조, workflow가 명확하며 multi-agent 방식의 필요성이 드러나는가? |
| 구현 완성도 | 20% | end-to-end 동작 여부, 논문 검색/요약/아이디어/critique/revision/보고서 생성의 통합 수준, 에러 핸들링 안정성 |
| 검증 및 평가 | 20% | citation verification, hallucination check, novelty/feasibility 평가, critic 반영 여부, 비용 제어 로직 |
| 결과물 품질 | 15% | 최종 research brief 또는 mini-proposal의 학술적 설득력, 실험 계획의 구체성, 참고문헌의 신뢰도 |
| 문서화 및 발표 | 10% | 프롬프트 로그, agent interaction log, 아키텍처 다이어그램, 실패 사례 분석, 발표 자료의 완성도 |

---

## 9. 최종 제출물

- 실행 가능한 프로그램 또는 notebook (소스코드 포함)
- 소스코드 및 실행 방법 설명서
- Agent architecture diagram 또는 workflow graph
- 프롬프트 로그 및 agent interaction log
- 최종 research brief 또는 mini-proposal
- 비용/성능 분석 리포트 및 실패 사례 분석
- 테스트 결과 및 citation verification 결과
- 데모 영상 또는 수업시간 live demo
- 결과 보고서(PPT)

---

## 10. 예시 프로젝트 주제

주의: 본 과제의 핵심은 단순히 그럴듯한 연구 제안서를 생성하는 것이 아니라, 복수의 agent가 어떻게 역할을 분담하고, 근거를 확인하며, 서로의 결과를 비판·수정하여 더 나은 연구 산출물을 만들어내는지를 보여주는 데 있다.

아래 주제들은 단순 요약형 과제가 아니라, 여러 agent가 문헌 탐색, 아이디어 생성, 실험 설계, 비판, 수정, 최종 판단을 분담하도록 설계할 수 있는 연구자동화 프로젝트 예시이다.

| No. | 예시 프로젝트 주제 | 주요 목표 | 권장 Multi-Agent 구성 |
|---:|---|---|---|
| 1 | AI 논문 아이디어 생성 및 검증 시스템 | 특정 연구 분야를 입력하면 새로운 연구 아이디어를 생성하고, 기존 연구와의 차별성, 실현 가능성, 실험 가능성을 검토한다. | Literature Agent, Idea Generator, Feasibility Agent, Experiment Designer, Critic/Reviewer, Revision Agent |
