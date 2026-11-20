# AgentLab

**Language:** [Türkçe](README.md) | English

AgentLab is an educational repository introducing Agentic AI concepts through hands-on sessions, explanations, and interactive Colab notebooks, designed with beginners in mind.

> Lesson notes, glossaries, conceptual exercises, and self-contained Google Colab notebooks for sessions one through four are provided here. Materials for later sessions will be added as they become ready.

## Sessions

1. [LLM Fundamentals](sessions/01-llm-fundamentals/README.en.md)
2. [Agent Architecture, Context and Memory](sessions/02-agent-core-and-state/README.en.md)
3. [Modern Agent Stack](sessions/03-modern-agent-stack/README.en.md)
4. [Security & Execution](sessions/04-security-and-execution/README.en.md)

## Get started

- [General glossary](docs/en/glossary.md)
- [Session 1 Colab playground](sessions/01-llm-fundamentals/demos/llm-playground/README.en.md)
- [Session 2 G4 Colab demos](sessions/02-agent-core-and-state/demos/README.en.md)
- [Session 3 G4 / L4 / T4 Colab demos](sessions/03-modern-agent-stack/demos/README.en.md)
- [Session 4 G4 / L4 / T4 Colab demos](sessions/04-security-and-execution/demos/README.en.md)

All four sessions run directly in Google Colab without installing Python or setting up a local environment. Session one's [Colab notebook](sessions/01-llm-fundamentals/demos/llm-playground/AgentLab-Colab.ipynb) observes tokens, next-token probabilities, sampling, and tool calling with Qwen3.5-0.8B. Session two's self-contained [G4 Colab notebook](sessions/02-agent-core-and-state/demos/agent-core/AgentLab-Session02-G4.ipynb) pairs a model-free `ScriptedModel` preview with Google's Gemma 4 12B QAT model, matching MTP assistant, and pinned llama.cpp CUDA runtime (262,144 default context capacity) for harness, context, memory, and RAG experiments. Session three's **7-cell `#@title` Studio v2** [G4 Colab notebook](sessions/03-modern-agent-stack/demos/modern-agent-stack/AgentLab-Session03-G4.ipynb) launches `Qwen 3.8 27B + MTP` (`Thinking` effort `xhigh`, target+draft `f8_e4m3` FP8 KV, `--ctx-size 1048576 --parallel 4 --kv-unified --kv-unified-per-slot 262144 --ctx-checkpoints 8 --cache-reuse 0 --cache-ram 8192`, `262,144` active context / `1,048,576` GPU KV pool), while [pro_AgentLab-Session03-L4.ipynb](sessions/03-modern-agent-stack/demos/modern-agent-stack/pro_AgentLab-Session03-L4.ipynb) and [plus_AgentLab-Session03-T4.ipynb](sessions/03-modern-agent-stack/demos/modern-agent-stack/plus_AgentLab-Session03-T4.ipynb) launch natively multimodal `Gemma 4 12B QAT + MTP` (`--reasoning on`, `f8_e4m3` FP8 KV, `524,288` GPU-resident KV + host RAM = `1,048,576` KV pool, strict fail-closed `ALAB-E02` tier guard, and shared `MyDrive/AgentLab-Agent-Runtime` Drive cache), providing independent `Deney 1`–`Deney 3` cells (`MCP`, `StructuredHandoff`, `System1DecisionGate` / `Jev` & `Laya`, `DualLayerSessionStore`) and a portless `google.colab.output` JS RPC **Live Studio** WebUI with a clickable `💭 Thinking` CoT cloud and Antigravity-style FIFO prompt queue. Session four's **7-cell `#@title` Studio v2** [G4 Colab notebook](sessions/04-security-and-execution/demos/security-and-execution/AgentLab-Session04-G4.ipynb) (`Qwen 3.8 27B + MTP` `xhigh`), [pro_AgentLab-Session04-L4.ipynb](sessions/04-security-and-execution/demos/security-and-execution/pro_AgentLab-Session04-L4.ipynb), and [plus_AgentLab-Session04-T4.ipynb](sessions/04-security-and-execution/demos/security-and-execution/plus_AgentLab-Session04-T4.ipynb) (`Gemma 4 12B + MTP`) open with a 5-minute Days 1–3 Bridge Summary and demonstrate **Guardrails**, **Prompt Injection** defense, isolated **Sandbox** Python/Bash execution (`outside_workdir` & timeout), **Trust Boundaries**, policy-gated **`[Approve]` / `[Reject]` HITL** pausing, **Durable Execution** (`checkpoint`/`resume`), and fixed two-line **`ALAB-Exx`** diagnostics with clickable CoT Thinking and the FIFO-queued portless **Live Studio**.
