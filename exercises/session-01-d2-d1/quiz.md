# Session 01 — D2·D1 Focus (15 questions, 30 min)

진단평가 결과(D2 25%, D1 50%)에 맞춰 구성했습니다. D2 5 · D1 5 · D3 2 · D4 2 · D5 1.
진단에서 보인 경향("구조를 고치는 대신 덧붙이거나 프롬프트로 부탁하기")을 겨냥한 선택지가 섞여 있습니다. 고르기 전에 **"이게 근본 원인을 고치는 가장 작은 구조적 수정인가?"**를 자문하세요.

**풀이 방법**: 답과 확신도(1=찍음 … 5=확실)를 답안표에 표시. 다 풀 때까지 `keys/` 는 열지 않는다.

---

### Q1
An agent has a single tool named `query` with the description "Queries data." It is used for both the customer CRM database and the analytics warehouse, and the model frequently sends CRM-style queries to the warehouse and vice versa. What is the best fix?

- A. Add a router model that decides which data source each query targets
- B. Add a sentence to the system prompt asking the model to be careful about data sources
- C. Split it into two tools with descriptive names (e.g., `query_crm`, `query_analytics`), each with a description of what data it covers and when to use it
- D. Lower the temperature so tool selection is more deterministic

### Q2
A `create_ticket` tool accepts `priority` with the enum `low | medium | high`. The model sends `"urgent"`. What should the application return?

- A. A `tool_result` with `is_error: true`, marked as a non-retryable validation error, stating the invalid field and the allowed values
- B. A `tool_result` saying the call failed, marked retryable, so the model tries the same call again
- C. Silently map `"urgent"` to `"high"` and report success
- D. Terminate the agent loop and alert the on-call engineer

### Q3
Your team's project-scoped `.mcp.json` connects to an internal API that requires a personal access token. How should the token be handled?

- A. Commit the token in `.mcp.json` so everyone can connect immediately
- B. Put the token in `CLAUDE.md` so Claude can pass it when needed
- C. Ask Claude to prompt each developer for the token at the start of every session
- D. Reference an environment variable (e.g., `${INTERNAL_API_TOKEN}`) in `.mcp.json`, and have each developer set it locally

### Q4
A read-only reporting agent is connected to a GitHub MCP server that exposes tools to read issues and PRs but also to merge PRs, delete branches, and change repository settings. What is the best approach?

- A. Add "Never merge or delete anything" to the agent's system prompt
- B. Expose only the read tools to this agent (tool allowlist / deny rules) and use a credential scoped to read access
- C. Add a reviewer subagent that checks the transcript for write operations after each run
- D. Keep all tools but log every call for auditing

### Q5
A team wants an agent in Claude Code to read files in the repository and search for symbols. An engineer proposes writing a custom MCP server that wraps the filesystem. What is the best response?

- A. Build the MCP server so the team controls the implementation
- B. Build the MCP server but also keep the built-in tools as a fallback
- C. Use Claude Code's built-in file read and search tools; reserve custom tools/MCP for internal systems or business logic the built-ins cannot reach
- D. Paste the relevant files into `CLAUDE.md` instead

---

### Q6
You are implementing an agentic loop with the Messages API. The model's response contains **two** `tool_use` blocks (it requested two tools at once). How should you send the results back?

- A. Execute both tools, then send one user message containing both `tool_result` blocks, each referencing its matching `tool_use_id`
- B. Send the first result, wait for the model's reply, then send the second result
- C. Combine both results into a single text block without IDs
- D. Put the results into the system prompt on the next request

### Q7
An agent keeps calling the same tool, which fails every time because a downstream service is down, until the run consumes its entire budget. What is the best fix?

- A. Switch to a larger model that will notice the repetition
- B. Add "do not repeat failing calls" to the system prompt
- C. Remove the tool from the agent
- D. Enforce a maximum iteration/turn limit in the loop, and return structured errors indicating the failure is not retryable so the agent can stop or escalate

### Q8
Requirement in Claude Code: Claude must not end its turn until the project's test suite passes. What is the most reliable way to enforce this?

- A. Write "Always run tests before finishing" in `CLAUDE.md`
- B. Configure a `Stop` hook that runs the tests and blocks stopping (with the failure as the reason) when they fail
- C. Configure a `SessionStart` hook that reminds Claude about the tests
- D. Ask the user to run the tests manually after every turn

### Q9
A coordinator dispatches a research subagent. The subagent returns its full 40,000-token working transcript, and after a few such tasks the coordinator's context fills up and its quality drops. What is the best fix?

- A. Give the coordinator a larger context window model
- B. Have the coordinator re-summarize each transcript after receiving it
- C. Instruct the subagent to return a concise, structured result (findings, sources, confidence, open questions) instead of its transcript
- D. Stop using subagents and run all research in the coordinator

### Q10 (Choose TWO)
In which TWO situations is a coordinator with subagents most justified over a single agent or fixed workflow?

- A. Many independent subtasks, each needing to read large amounts of material that would otherwise flood a single context (e.g., auditing 30 separate repositories)
- B. A fixed three-step pipeline whose order never changes
- C. Answering short FAQ questions from a small knowledge base
- D. Subtasks needing different specializations and different tool permissions (e.g., a read-only analyst and a separate writer with limited write access)
- E. The team wants the architecture to look more advanced to stakeholders

---

### Q11
You want a code-review helper in Claude Code that runs in its own context window, can only use read and search tools, and returns findings to the main session when delegated to. What is the best fit?

- A. A subagent defined in `.claude/agents/` with its tools restricted to read/search
- B. A section in `CLAUDE.md` describing how to review code
- C. A `PostToolUse` hook that reviews every edit
- D. A permission rule in `settings.json`

### Q12
A project's `CLAUDE.md` has grown to 400 lines covering frontend, backend, and test conventions, and much of it is irrelevant to whatever Claude is working on. What is the best restructuring?

- A. Move everything into a hook that prints the conventions at session start
- B. Delete the conventions and rely on Claude to infer them from the code
- C. Move it all to `~/.claude/CLAUDE.md` so it applies to every project
- D. Keep core project context in `CLAUDE.md` and split topic-specific conventions into `.claude/rules/` files, scoped by path where possible

---

### Q13
An API pipeline must always return invoice extraction through a `record_invoice` tool whose `input_schema` defines the fields. Occasionally the model answers in prose instead of calling the tool. What is the most direct fix?

- A. Add "You must always call the tool" in capital letters to the prompt
- B. Set `tool_choice` to force that specific tool (`{"type": "tool", "name": "record_invoice"}`)
- C. Parse the prose answer with regex when the tool isn't called
- D. Retry the request until the model calls the tool

### Q14
Extraction output now always passes JSON schema validation, but sometimes the line-item amounts do not add up to `total_amount`. What is the best next step?

- A. Add a second model to review every invoice
- B. Make the schema stricter by marking more fields as required
- C. Add a programmatic business-rule check after schema validation; on failure, retry with the specific discrepancy in the feedback, with a retry limit and human review fallback
- D. Accept it, since the output is schema-valid

---

### Q15
A user tells an agent with production database access: "Clean up the customer table." This could mean removing duplicates, deleting inactive customers, or normalizing formats. What should the agent do?

- A. Ask a clarifying question about the intended operation before taking any action, since the request is ambiguous and the possible actions are destructive
- B. Pick the most likely interpretation (removing duplicates) and run it
- C. Perform all three operations to be thorough
- D. Refuse the task because it involves a production database
