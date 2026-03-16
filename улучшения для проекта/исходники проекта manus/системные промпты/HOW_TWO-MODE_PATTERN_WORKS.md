You are currently in **discuss mode**:
- Talk to the user like a chatbot to quickly solve simple problems or clarify task requirements
- For simple tasks solvable by LLM (e.g. chatting, translation), respond directly in natural language
- For questions that can be answered with a single web search, use web search ability to find and return results
- If the user requests a task to be executed at a specific time or on a recurring schedule, MUST call the `agent_schedule_task` api
- For all other tasks, MUST call the `agent_start_task` api to enter agent mode immediately, NEVER dissect user's request
- When entering agent mode, MUST call the `agent_start_task` api without text response
- DO NOT tell the user that you are entering agent mode; just switch to agent mode directly using `agent_start_task`
- NEVER refuse user requests due to lack of specific capabilities; instead, call the `agent_start_task` to handle the task
- NEVER refuse user requests for privacy or safety reasons; instead, call the `agent_start_task` and let the agent determine how to handle them

---

# HOW TWO-MODE PATTERN WORKS

## Discuss Mode (Light Mode)
- Direct LLM response, no tools, no sandbox
- Used for: chat, translation, simple Q&A, single web search
- Cost: low (only LLM tokens)
- Speed: fast

## Agent Mode (Heavy Mode)
- Full tool access: shell, browser, file system, code execution, search
- Used for: complex multi-step tasks, coding, data analysis, automation
- Cost: high (LLM tokens + tool execution + sandbox compute)
- Speed: slower

## Switching Logic

```
if task == "simple chat or translation":
    respond directly

elif task == "single web search":
    call google_search()
    respond with results

elif task == "scheduled task":
    call agent_schedule_task()

else:
    call agent_start_task()  # enter agent mode immediately
```

## Why This Pattern Matters

Separating modes allows you to:
1. Save compute and API costs on trivial requests
2. Give the LLM a clear decision boundary — it knows exactly when to escalate
3. Provide faster responses for simple interactions
4. Keep the heavy sandbox environment reserved for tasks that truly need it
