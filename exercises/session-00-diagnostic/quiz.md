# Session 00 — Diagnostic (21 questions, 40 min)

목적: 도메인별 현재 수준 파악. 실제 시험처럼 영어 시나리오형으로 구성했고, 가이드 PDF의 연습문제와 겹치지 않는다.
문항 수는 도메인 비중에 맞춤 (D1 6 · D2 4 · D3 4 · D4 4 · D5 3).

**풀이 방법**: 답과 확신도(1=찍음 … 5=확실)를 `results/session-00.yaml` 에 적는다. 모르면 비워두지 말고 찍고 확신도 1.
`keys/` 폴더는 다 풀 때까지 열지 않는다.

---

### Q1
A refund-handling system always runs the same four steps in the same order: classify the request, look up the order, apply the refund policy, draft a reply. The team proposes an autonomous multi-agent system. What is the most appropriate design?

- A. A coordinator agent with four specialized subagents
- B. A fixed workflow (prompt chaining) where code defines each step and its order
- C. A single agent given all tools with `max_turns` set to 50
- D. A single model call with every order record included in the prompt

### Q2
A research task must (1) identify the top 3 competitors in a market, then (2) for each competitor gather pricing, reviews, and feature lists independently, then (3) produce a comparison. Which orchestration fits best?

- A. Run steps 1, 2 and 3 fully in parallel from the start
- B. Run everything sequentially in one agent
- C. Run step 1 first, fan out one subagent per competitor in parallel for step 2, then merge in step 3
- D. Run step 2 first for every company in the industry, then filter

### Q3
You are implementing an agentic loop directly with the Messages API. Which loop condition is correct?

- A. Continue while `stop_reason == "tool_use"`: execute the requested tools, append the results as `tool_result` blocks in a new user message, and call the API again
- B. Continue while the response contains any text block
- C. Continue while `stop_reason == "end_turn"`
- D. Always run exactly 10 iterations regardless of the response

### Q4
Policy: every file the agent writes must be recorded in an audit log, and any write outside `/src` must be blocked. What is the most reliable implementation?

- A. State both rules clearly in the system prompt
- B. Add a reviewer subagent that inspects the transcript after the run
- C. Ask the agent to report every write it made in its final answer
- D. A PreToolUse hook that validates the path and blocks violations, plus a PostToolUse hook that writes the audit record

### Q5
Halfway through a long debugging session you want to try a risky alternative hypothesis, while keeping the current session's state intact to return to. What should you do?

- A. Resume the same session and try the hypothesis there
- B. Start a brand-new session and re-explain everything
- C. Fork the session and explore the hypothesis in the fork
- D. Clear the context and continue

### Q6 (Choose TWO)
A coordinator delegates work to several subagents. Which TWO practices most improve reliability and context efficiency?

- A. Subagents return their full raw transcripts to the coordinator
- B. Subagents return a concise, structured result (findings, sources, status)
- C. The coordinator passes its entire conversation history to every subagent
- D. The coordinator passes only task-specific instructions and the inputs each subagent needs
- E. All subagents share one credential with write access so they never get blocked

---

### Q7
An agent has `search_orders` (fuzzy search by customer name/date range) and `get_order` (fetch by exact order ID). When the user provides an exact order ID, the model often calls `search_orders`. What is the best first fix?

- A. Add a separate classifier model to pick the tool
- B. Lower the temperature
- C. Remove `search_orders`
- D. Rewrite both descriptions to state when to use each (exact ID → `get_order`; partial criteria → `search_orders`) and tighten the input schemas

### Q8
A tool call fails because an upstream API rate-limited the request. How should your application return this to Claude?

- A. Return a `tool_result` with `is_error: true` and content describing the error type, whether it is retryable, and a suggested action
- B. Raise an exception and terminate the agent loop
- C. Return an empty `tool_result` so the model moves on
- D. Insert the error text into the system prompt on the next call

### Q9
Your team wants everyone who works in a repository to have the same internal Jira MCP server available in Claude Code, without each person configuring it manually. Where should it be defined?

- A. In each developer's user-scope configuration
- B. In a project-scoped `.mcp.json` committed to the repository (secrets supplied via environment variables)
- C. As a description in `CLAUDE.md`
- D. In a shell alias each developer adds to their profile

### Q10
An agent is connected to 5 MCP servers exposing about 60 tools in total. Tool-selection accuracy has dropped noticeably. What is the best first step?

- A. Switch to a larger model
- B. Add usage examples for all 60 tools to the system prompt
- C. Restrict each agent to the tools relevant to its role (split tool sets by role/task)
- D. Increase `max_tokens`

---

### Q11
A developer allows `Bash(rm:*)` in `~/.claude/settings.json`. The project's `.claude/settings.json` also allows it. The organization's enterprise managed policy denies it. What happens?

- A. Allowed — user settings reflect the developer's intent
- B. Allowed — project settings override managed policy for that project
- C. Denied — managed policy takes precedence over project and user settings
- D. Claude asks for confirmation each time, since the settings conflict

### Q12
A team has a 30-step release checklist that is needed only occasionally. They want Claude Code to apply it automatically when a release task comes up, without loading it into every session's context. What is the best fit?

- A. Paste the checklist into `CLAUDE.md`
- B. Implement it as a PreToolUse hook
- C. Encode it as permission rules in `settings.json`
- D. Package it as a Skill (`SKILL.md` with a clear description), loaded on demand

### Q13
A CI pipeline runs Claude Code to review each pull request, and the next job parses the output. Which setup is most appropriate?

- A. `claude -p "<review prompt>" --output-format json` with a turn limit and a restricted set of allowed tools
- B. Run interactive `claude` and have an engineer paste the output into the pipeline
- C. Ask in `CLAUDE.md` that all output be JSON, and run interactively
- D. Run in plan mode interactively so nothing is changed

### Q14 (Choose TWO)
Which TWO items belong in `CLAUDE.md` rather than being enforced by a hook or permission rule?

- A. "Run `pnpm test --filter api` to test the API package."
- B. Block `git push --force` for every developer in the company
- C. "Services use the repository pattern in `/services`; avoid raw SQL in handlers."
- D. Send every executed bash command to the SIEM
- E. Prevent reading `.env` files

---

### Q15
An application extracts invoice fields into a database. About 4% of outputs are missing `currency` or put a string in `total_amount`. What is the best first fix?

- A. Add regex post-processing to patch missing fields
- B. Add a reviewer agent to check every invoice
- C. Define a JSON schema (via tool `input_schema` / structured outputs) with required fields, types and enums
- D. Add a longer prose paragraph explaining the fields

### Q16
A support-ticket classifier is inconsistent on borderline cases such as "complaint about the shipping fee on my bill" (billing vs. shipping). What is the most effective improvement?

- A. Add few-shot examples that cover the borderline cases with the correct labels and brief rationale
- B. Increase `max_tokens`
- C. Switch to a larger model
- D. Remove the shipping category

### Q17
After adding a schema, 2% of outputs still fail validation. What retry policy is best?

- A. Retry the identical request until it passes
- B. Silently drop failing records
- C. Only lower the temperature and retry
- D. Retry a limited number of times, feeding back the specific validation errors, then route to a fallback or human review

### Q18
When is a separate reviewer (second-pass) step most justified?

- A. For every request, as a default best practice
- B. When errors are costly and the review criteria can be stated explicitly (e.g., extracting liability clauses from contracts)
- C. Whenever the prompt is longer than 2,000 tokens
- D. Whenever a smaller model is used

---

### Q19
Each request contains a fixed set of tool definitions, a fixed 20k-token policy document, and a varying user question. How should you structure the prompt for prompt caching?

- A. Put the stable content (tools, system/policy document) first and place the cache breakpoint at the end of that stable prefix; the user question comes after
- B. Put the user question first, then the policy document, and cache everything
- C. Cache only the user question, since it changes every time
- D. Prompt caching applies to output tokens, so prompt order does not matter

### Q20
An agent calls a payment refund API. The call times out, and it is unknown whether the refund was executed. What is the best design?

- A. Immediately retry the same call
- B. Tell the user the refund failed
- C. Use an idempotency key so retries are safe, and check the refund status before re-executing
- D. Increase the timeout and do nothing else

### Q21
An agent is migrating 200 files over several hours. As the context gets compacted, it forgets which files are done and which decisions were made, and redoes work. What is the best fix?

- A. Keep the full history in context at all times
- B. Persist progress and key decisions in an external state file (e.g., a checklist) that the agent reads and updates, and resume from it
- C. Switch to a larger model
- D. Restart from scratch whenever this happens
