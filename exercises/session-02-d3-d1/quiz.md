# Session 02 — D3·D1 Consolidation (16 questions, 32 min)

1회차 결과(13/15, 추정 846)를 반영했습니다. D3 5 · D1 5 · D2 2 · D4 2 · D5 2.
초점: **Claude Code 확장 기능 구분(skill·subagent·hook·settings)**, 1회차에 확신도 1~2로 맞힌 개념 재확인, 한 번만 나온 D5 개념 보강.
**NOT** 이 들어간 문항이 2개 있습니다. 질문을 끝까지 읽고 고르세요.

**풀이 방법**: 답과 확신도(1=찍음 … 5=확실)를 답안표에 표시. 다 풀 때까지 `keys/` 는 열지 않는다.

---

### Q1
A team wants a `/deploy-check` workflow that developers invoke by name before a release. It needs a 25-item checklist plus a helper script that validates environment variables. It should not consume context in sessions where nobody is deploying. What is the best fit?

- A. A `PreToolUse` hook that runs the checklist on every command
- B. A subagent that runs automatically at the start of every session
- C. A skill in `.claude/skills/deploy-check/` with a `SKILL.md` and the helper script bundled alongside it
- D. The checklist and script contents pasted into `CLAUDE.md`

### Q2
Which of the following is **NOT** a good use of a Claude Code hook?

- A. Blocking any write to `config/production.yaml` with a `PreToolUse` hook
- B. Running the code formatter after Claude edits a file
- C. Injecting the current branch and open issue number into context when a session starts
- D. Teaching Claude the team's architectural conventions for designing new services

### Q3
During a large refactor, Claude needs to find out how a deprecated library is used across 500 files. Reading them all in the main session would flood its context. What is the best approach?

- A. Read all 500 files in the main session, then compact
- B. Delegate the investigation to a subagent that explores in its own context and returns a concise summary of usage patterns
- C. Create a skill that lists the 500 files
- D. Switch to plan mode so the files are not modified

### Q4
A developer wants Claude Code to run `npm run lint` without asking, but only for themselves and only in this project. Teammates should not be affected. Where should the allow rule go?

- A. `.claude/settings.local.json` in the project
- B. `.claude/settings.json` in the project
- C. `~/.claude/settings.json`
- D. A line in `CLAUDE.md` saying lint may be run freely

### Q5
A CI job runs Claude Code and a downstream step must parse a result that conforms to a specific JSON Schema. Which invocation is most appropriate?

- A. `claude "<prompt>"` interactively, then copy the output
- B. `claude -p "<prompt>"` and parse the plain text with regex
- C. `claude -p "<prompt>" --output-format json --json-schema '<schema>'`, then read the `structured_output` field
- D. `claude -p "<prompt>" --output-format stream-json` and take the first line

---

### Q6
Which of the following is **NOT** a good reason to introduce subagents?

- A. Isolating a large exploration so its raw material does not fill the main context
- B. Making a simple, fixed three-step sequential pipeline more robust
- C. Running independent research tasks in parallel
- D. Giving different roles different, narrower tool permissions

### Q7
Incoming documents must first be identified as a contract, an invoice, or a resume. Each type then goes through its own fixed sequence of processing steps, which never vary. What design fits best?

- A. One autonomous agent with every tool for all three types
- B. A coordinator agent that improvises a new plan for each document
- C. Three agents that each process every document and vote on the result
- D. A routing workflow: a classification step, then a fixed, specialized pipeline for each document type

### Q8
In Claude Code you want the project's code formatter to run automatically on every file Claude edits or creates. What is the right mechanism?

- A. A `PostToolUse` hook matching `Edit|Write` that runs the formatter on the changed file
- B. A `PreToolUse` hook matching `Edit|Write` that runs the formatter
- C. A `Stop` hook that formats the entire repository
- D. An instruction in `CLAUDE.md` to always format files

### Q9
In a Messages API agentic loop, the model returns a response with `stop_reason: "tool_use"`. Before sending the tool results, what must the conversation history contain?

- A. Only the original user message; the tool results replace the assistant turn
- B. A system-prompt update describing which tool was called
- C. The assistant's response appended as-is (including its `tool_use` blocks), followed by a new user message with the matching `tool_result` blocks
- D. A summary of the assistant's response in place of the original blocks

### Q10
A coordinator delegates a task to a subagent. The subagent starts with a fresh context and does not see the coordinator's conversation. What should the delegation message contain?

- A. Only a short task title; the subagent will ask follow-up questions
- B. A self-contained brief: the goal, the specific inputs and constraints it needs, and the expected output format
- C. The coordinator's entire conversation history
- D. Nothing beyond the tool list, since the subagent can discover everything itself

---

### Q11
Which capability is the best candidate for a custom MCP server?

- A. The company's internal pricing engine, which applies contract-specific discount rules
- B. Reading files in the local repository
- C. Running shell commands in the project
- D. A general web search that the platform already provides

### Q12
A `schedule_meeting` tool takes a `start_time` string. The model often passes values like `"next Friday afternoon"`, which the backend rejects. What is the best first fix?

- A. Add an NLP service to parse natural-language dates before the backend
- B. Switch to a larger model
- C. Let the backend accept any string and guess the date
- D. In the input schema and description, specify ISO 8601 format with an example and state that relative dates must be resolved first (e.g., using a provided current date)

---

### Q13
A summarizer's prompt includes three few-shot examples, all of short news articles with one-sentence summaries. On long technical reports, it now produces summaries that are far too short. What is the most likely cause and fix?

- A. The model is too small; upgrade it
- B. The examples are not representative; add examples covering varied lengths and document types, including long reports with appropriately longer summaries
- C. Temperature is too low; raise it
- D. Remove all examples and rely on instructions alone

### Q14
A prompt says "NEVER use ellipses." The model still uses them occasionally. According to Anthropic's prompting guidance, which change is most likely to help?

- A. Repeat the rule three times in capital letters
- B. Move the rule to the very end of the conversation
- C. Explain why: the output will be read aloud by a text-to-speech engine that cannot pronounce ellipses
- D. Add a reviewer model that strips ellipses

---

### Q15
A team enabled prompt caching on a large, unchanging system prompt, but the cache hit rate is near zero. The system prompt starts with `Current time: 2026-10-11T17:57:03Z`. What is the fix?

- A. Move the timestamp out of the cached prefix (after the cache breakpoint, e.g., into the user message) so the stable prefix is identical across requests
- B. Switch to the 1-hour cache TTL
- C. Add more cache breakpoints inside the system prompt
- D. Cache the user message instead

### Q16
A support agent handles conversations of 200+ turns. Key facts given early (the customer's account ID, the agreed refund amount, a promised deadline) get lost or distorted after the history is summarized. What is the best fix?

- A. Disable summarization and keep the full history
- B. Switch to a model with a larger context window
- C. Ask the customer to repeat key facts every 20 turns
- D. Maintain a structured "case facts" record outside the transcript, update it as facts are confirmed, and include it in every request
