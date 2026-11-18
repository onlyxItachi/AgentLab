# 02 — Agent Architecture, Context and Memory

[Home](../../README.en.md) | [Türkçe](README.md)

**Duration:** Approximately 90 minutes. Before starting, recall the distinction between models, tokens and tools from [session one](../01-llm-fundamentals/README.en.md).

We will observe a small course assistant one step at a time. The model proposes a tool, the harness validates that proposal, and a Python function returns a result to the model. We will vary context selection, conversation state, memory preferences and retrieval while keeping the task comparable.

## Learning goals

- Distinguish a proposed model action from an action executed by the application.
- Explain the agent loop, ReAct and Plan-and-Solve through an execution trace.
- Identify which information enters the model context and which information stays outside it.
- Distinguish conversation state, runtime memory and persistent memory.
- Assess a retrieval, vector search and RAG workflow using its sources.

## Lesson sequence

| Minutes | Topic / observation |
| --- | --- |
| 0-10 | Connection to session one and the model / application distinction |
| 10-25 | Harness, agent loop and Experiment A (`4F` / `A1`) |
| 25-40 | Context engineering and Experiment B (`B1`–`B3`) |
| 40-55 | State / memory and Experiment C (`C1`–`C4`) |
| 55-75 | Retrieval, vector search, RAG and Experiment D (`D1`–`D3`) |
| 75-87 | Small-group exercise and comparison of results |
| 87-90 | Understanding check and wrap-up |

## Materials

[Lesson notes](lesson-notes.md) | [Session glossary](glossary.md) | [Demos](demos/README.en.md) | [Exercises](exercises/README.en.md)

The live-demo path is the self-contained, syntax-highlighted, cell-by-cell modular [G4 Colab notebook](demos/agent-core/AgentLab-Session02-G4.ipynb). Download it from GitHub (or use your Google Drive copy), open it in Colab via **File → Upload notebook**, and select a **G4 / RTX PRO 6000 Blackwell** runtime. Opening cells initialize the workspace and verify GPU hardware (`1A`–`1B`), prepare pinned artifacts (`2A`–`2C`), manage the loopback server client (`3A`–`3D`), and build the agent components (`4A`–`4F`); after `1A`, running `4A`–`4F` yields a deterministic `ScriptedModel` preview even without GPU or model downloads. Gemma 4 12B QAT with matching MTP assistant defaults to a **262,144**-token context capacity (`3D`). At the end, run `9A` model stop and `9B` VM release separately; participants must check G4 access and CU consumption in their own accounts.

> **Colab Plan & GPU Access Note:** The **G4 (`RTX PRO 6000 Blackwell`)** accelerator is only available on the **Colab Ultra** plan; **Colab Pro** accounts typically receive **A100** (or L4), while **Colab Plus / Free** accounts get at most **T4 (~15 GB VRAM)**. If you do not have G4 access: (1) run `1A` followed by `4A`–`4F` to try the deterministic `ScriptedModel` preview anywhere with no GPU or download required; (2) if shared by the instructor during the live workshop, use the plan-matched (`pro_...` A100 or `plus_...` T4) notebook.

[Previous: LLM Fundamentals](../01-llm-fundamentals/README.en.md) | [Next: Modern Agent Stack](../03-modern-agent-stack/README.en.md)
