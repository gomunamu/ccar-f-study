# Session 00 Report

- 점수: **14/21** (67%)
- 도메인 비중 가중 추정치: **680 / 1000** (합격선 720, 참고용)

## 도메인별

| 도메인 | 정답률 | 비중 |
|---|---|---|
| D2 Tool Design & MCP Integration | 25% (1/4) | 18% |
| D1 Agentic Architecture & Orchestration | 50% (3/6) | 27% |
| D4 Prompt Engineering & Structured Output | 75% (3/4) | 20% |
| D3 Claude Code Configuration & Workflows | 100% (4/4) | 20% |
| D5 Context Management & Reliability | 100% (3/3) | 15% |

## 확신했는데 틀림 (최우선 복습 — 오개념)

- Q9 `D2.mcp` 내 답 C → 정답 B: 팀 공유는 project scope의 .mcp.json을 repo에 커밋. 비밀값은 환경변수 확장으로 분리. user scope는 개인용.
- Q15 `D4.structured` 내 답 A → 정답 C: machine consumption + 필수 필드/타입 보장 → schema 기반 structured output이 근본 해결. regex·reviewer는 증상 처리.

## 맞았지만 찍음 (복습 필요)

- Q12 `D3.extensions`: 가끔 필요한 절차적 지식 + 관련 있을 때 자동 적용 = Skill (description만 상시 노출, 본문은 필요 시 로드). CLAUDE.md는 매 세션 로드되어 context 낭비.
- Q14 `D3.claude-md`: CLAUDE.md는 작업 지침(명령어, 코딩 규칙). 반드시 막아야 하는 것(force push, .env 읽기)과 감사 로깅은 hook/permission/managed policy로 강제.

## 전체 문항

| Q | 개념 | 내 답 | 정답 | 확신 | 결과 |
|---|---|---|---|---|---|
| Q1 | D1.pattern | B | B | 4 | O |
| Q2 | D1.parallel | C | C | 4 | O |
| Q3 | D1.loop | B | A | 3 | X |
| Q4 | D1.hooks | A | D | 2 | X |
| Q5 | D1.session | C | C | 5 | O |
| Q6 | D1.handoff | AD | BD | 1 | X |
| Q7 | D2.tool-desc | A | D | 2 | X |
| Q8 | D2.error | A | A | 5 | O |
| Q9 | D2.mcp | C | B | 4 | X |
| Q10 | D2.surface | B | C | 3 | X |
| Q11 | D3.settings | C | C | 5 | O |
| Q12 | D3.extensions | D | D | 2 | O |
| Q13 | D3.headless | A | A | 5 | O |
| Q14 | D3.claude-md | AC | AC | 1 | O |
| Q15 | D4.structured | A | C | 4 | X |
| Q16 | D4.fewshot | A | A | 3 | O |
| Q17 | D4.validation | D | D | 3 | O |
| Q18 | D4.review | B | B | 3 | O |
| Q19 | D5.caching | A | A | 4 | O |
| Q20 | D5.reliability | C | C | 4 | O |
| Q21 | D5.context | B | B | 4 | O |

## 오답 해설

- **Q3** (A) stop_reason이 tool_use면 tool 실행 후 tool_result를 user 메시지로 붙여 재호출. end_turn이면 종료. 실무에선 max turn 안전장치를 함께 둔다.
- **Q4** (D) 정책·감사는 모델 판단이 아닌 deterministic enforcement. PreToolUse는 차단, PostToolUse는 기록에 적합.
- **Q6** (BD) subagent의 가치는 context 격리. 입력은 task-specific로 최소화, 출력은 압축된 structured 결과로. 공유 쓰기 자격증명은 least privilege 위반.
- **Q7** (D) tool 선택 오류는 classifier 추가 전에 description/schema로 '언제 쓰는지'를 명시하는 것이 가장 작은 수정.
- **Q9** (B) 팀 공유는 project scope의 .mcp.json을 repo에 커밋. 비밀값은 환경변수 확장으로 분리. user scope는 개인용.
- **Q10** (C) tool이 많을수록 선택 혼란·context 비용 증가. 역할별로 필요한 tool만 노출하는 것이 첫 조치.
- **Q15** (C) machine consumption + 필수 필드/타입 보장 → schema 기반 structured output이 근본 해결. regex·reviewer는 증상 처리.
