# CCAR-F Study

Claude Certified Architect – Foundations (CCAR-F / CCA-F) 합격을 위한 학습 저장소.
진단평가 → 도메인별 강약 파악 → 약한 영역 위주 회차 생성의 피드백 루프로 운영한다.

## 시험 요약

| 항목 | 내용 |
|---|---|
| 문항/시간 | 60문항 / 120분, 영어, 시나리오 기반 MC/MR |
| 합격점 | 720 / 1000 (scaled) |
| D1 Agentic Architecture & Orchestration | 27% |
| D2 Tool Design & MCP Integration | 18% |
| D3 Claude Code Configuration & Workflows | 20% |
| D4 Prompt Engineering & Structured Output | 20% |
| D5 Context Management & Reliability | 15% |

## 구조

```
materials/      학습자료 (가이드 PDF, 참고 링크)
concepts.yaml   도메인 → 개념 태그 목록 (모든 문제는 개념 태그를 가짐)
exercises/      회차별 문제지 (session-NN-*/quiz.md)
keys/           회차별 정답·해설 (풀기 전에는 열지 않기)
results/        회차별 내 답안 (session-NN.yaml)
scripts/        채점·숙련도 갱신 스크립트
mastery.json    개념/도메인별 누적 숙련도 (score.py가 갱신)
```

## 학습 루프

1. `exercises/session-NN-*/quiz.md` 를 풀고 `results/session-NN.yaml` 에 답과 확신도(1~5)를 적는다.
2. 채점: `python scripts/score.py NN` → `results/session-NN-report.md`, `mastery.json` 갱신
3. 리포트의 **약한 도메인 / 확신했는데 틀린 문항**을 보고 다음 회차 구성
   (다음 회차 출제 비중 = 약점 50% · 신규/미출제 개념 30% · 복습 20%)

## 일정

- 2026-10-12부터 오전 출근 · 오후 재택 병행, 하루 45~60분 기준
- 1회차 = 진단평가(session-00), 이후 회차는 결과에 따라 생성
