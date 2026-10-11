# Session 01 Report

- 점수: **13/15** (87%)
- 도메인 비중 가중 추정치: **846 / 1000** (합격선 720, 참고용)

## 도메인별

| 도메인 | 정답률 | 비중 |
|---|---|---|
| D3 Claude Code Configuration & Workflows | 50% (1/2) | 20% |
| D1 Agentic Architecture & Orchestration | 80% (4/5) | 27% |
| D2 Tool Design & MCP Integration | 100% (5/5) | 18% |
| D4 Prompt Engineering & Structured Output | 100% (2/2) | 20% |
| D5 Context Management & Reliability | 100% (1/1) | 15% |

## 확신했는데 틀림 (최우선 복습 — 오개념)

- Q10 `D1.pattern` 내 답 BC → 정답 AD: multi-agent는 (1) 독립 작업 + context 격리 이득, (2) 전문화·권한 분리가 필요할 때 정당화된다. 고정 순서는 workflow, 단순 질의는 단일 호출.

## 맞았지만 찍음 (복습 필요)

- Q5 `D2.builtin`: 플랫폼이 이미 제공하는 기능은 다시 만들지 않는다. custom tool/MCP는 사내 시스템·비즈니스 로직처럼 built-in이 닿지 않는 곳에.
- Q6 `D1.loop`: 한 응답의 모든 tool_use에 대한 tool_result를 하나의 user 메시지에 담아 보낸다. 각 결과는 tool_use_id로 짝지어진다. 나눠 보내면 병렬 tool use 흐름이 깨진다.
- Q7 `D1.loop, D2.error`: 종료 조건(최대 반복)은 loop 설계의 필수 안전장치. 구조화된 non-retryable 오류를 주면 agent가 중단·에스컬레이션을 판단할 수 있다. 프롬프트 당부는 강제가 아니다.
- Q8 `D1.hooks`: Stop hook은 Claude가 턴을 끝내려 할 때 실행되고, block 결정과 이유를 돌려주면 멈추지 못하고 계속 작업한다. CLAUDE.md는 부탁일 뿐 강제가 아니다.
- Q13 `D4.structured`: tool_choice로 특정 tool을 강제하면 응답이 반드시 그 tool 호출(=schema 형식)이 된다. 대문자 당부·regex·무한 재시도는 증상 처리.
- Q14 `D4.validation`: schema는 형식만 보장하고 필드 간 산술 같은 비즈니스 규칙은 못 잡는다 → 코드 검증 + 구체적 오류를 담은 targeted retry + 횟수 제한·사람 검토.

## 전체 문항

| Q | 개념 | 내 답 | 정답 | 확신 | 결과 |
|---|---|---|---|---|---|
| Q1 | D2.tool-desc | C | C | 4 | O |
| Q2 | D2.error | A | A | 4 | O |
| Q3 | D2.mcp | D | D | 3 | O |
| Q4 | D2.surface | B | B | 3 | O |
| Q5 | D2.builtin | C | C | 1 | O |
| Q6 | D1.loop | A | A | 2 | O |
| Q7 | D1.loop, D2.error | D | D | 2 | O |
| Q8 | D1.hooks | B | B | 2 | O |
| Q9 | D1.handoff | C | C | 3 | O |
| Q10 | D1.pattern | BC | AD | 5 | X |
| Q11 | D3.extensions | D | A | 1 | X |
| Q12 | D3.claude-md | D | D | 3 | O |
| Q13 | D4.structured | B | B | 2 | O |
| Q14 | D4.validation | C | C | 1 | O |
| Q15 | D5.ambiguity | A | A | 3 | O |

## 오답 해설

- **Q10** (AD) multi-agent는 (1) 독립 작업 + context 격리 이득, (2) 전문화·권한 분리가 필요할 때 정당화된다. 고정 순서는 workflow, 단순 질의는 단일 호출.
- **Q11** (A) 독립 context + 도구 제한 + 위임해서 결과를 받음 = subagent(.claude/agents/). CLAUDE.md는 상시 지침, hook은 이벤트 강제, permission은 허용 범위.

## 메모

- Q10: 문제를 반대로 읽음(개념 오류 아님). 독해 실수 보정 시 14/15.
