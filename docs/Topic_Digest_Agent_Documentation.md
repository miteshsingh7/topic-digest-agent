# Topic Digest Agent

## Project Abstract

Topic Digest Agent is an AI-powered research assistant built on the ReAct (Reason + Act) framework using the smolagents library. Given a topic, the agent autonomously searches the web, visits and reads full source pages, extracts key facts, checks source credibility, and compiles a structured, cited research digest — without any hardcoded pipeline. At each step, the agent reasons about what it has learned so far and decides which tool to call next, looping until it has enough coverage to produce a final answer. The project demonstrates practical application of agentic reasoning loops, custom tool design, and multi-step autonomous decision-making using a code-executing LLM agent.

## Domain

Agentic AI — ReAct Framework (Curriculum Section 25.1)

## Problem Statement

Manually researching a topic means opening multiple search results, skimming pages, judging which sources are trustworthy, and piecing together a summary by hand. This is slow and repetitive for anything beyond a single quick search. Topic Digest Agent automates this loop — it doesn't just return search results, it actively reasons about what it's found, digs deeper when needed, filters for credibility, and hands back an organized, source-backed digest.

## Tech Stack

- Python
- smolagents (CodeAgent)
- Groq API (LLM backend)
- Streamlit (UI)

## Tools Used by the Agent

| Tool | Type | Purpose |
|---|---|---|
| `web_search` | Built-in (DuckDuckGoSearchTool) | Searches the web for a given query |
| `visit_webpage` | Built-in (VisitWebpageTool) | Fetches full page content from a URL, not just the search snippet |
| `extract_key_facts` | Custom | Condenses raw page text into structured bullet points |
| `check_source_credibility` | Custom | Flags source reliability (e.g. .gov/.edu/known outlets vs. unverified sites) |
| `save_note` | Custom | Logs findings into a running research log as the agent works through sources |
| `generate_citations` | Custom | Formats the collected sources into a clean references block |

## How It Maps to the ReAct Framework

The agent runs a continuous **Reason → Act → Observe** loop:

1. **Thought** — the model decides what it needs next
2. **Action** — it calls a tool (e.g. `web_search`, `visit_webpage`, `extract_key_facts`)
3. **Observation** — the tool's return value is fed back into context
4. This repeats — searching new angles, visiting more sources, logging notes — until the model decides it has enough to answer
5. **Final Answer** — a compiled digest with citations

Because the project uses smolagents' `CodeAgent`, each "Action" is executed as a Python code snippet rather than a JSON blob — the agent writes and runs code to call its tools, and the code's output becomes the next observation. This is the same ReAct loop, expressed through code execution instead of fixed JSON actions.

## Core Features

- Autonomous multi-step research — not a single search-and-answer, the agent adaptively searches multiple angles
- Visible reasoning trace shown in the UI (proves genuine step-by-step decision-making, not a scripted pipeline)
- Source credibility filtering
- Running research log built up across the session
- Auto-generated citations for every digest

## Architecture / Flow

```
User enters topic
      ↓
CodeAgent (Groq LLM) reasons about next step
      ↓
Calls web_search → gets result links
      ↓
Calls visit_webpage on promising links → gets full content
      ↓
Calls extract_key_facts → structures findings
      ↓
Calls check_source_credibility → flags reliability
      ↓
Calls save_note → logs to research log
      ↓
Loop continues until agent decides coverage is sufficient
      ↓
Calls generate_citations → compiles sources
      ↓
Final structured digest returned to user via Streamlit
```

## Submission Checklist (matches SmartBridge project tracker requirements)

- [ ] Project Document (this file, exported to PDF/DOCX)
- [ ] GitHub repository link
- [ ] Demo video (1–2 min, screen recording showing a live query end to end, including the visible reasoning trace)
- [ ] Project Drive folder (code + document + video)
- [ ] Code screenshots included in the document (commonly flagged as missing in reviewer comments — include at least the tool definitions and the agent setup)
