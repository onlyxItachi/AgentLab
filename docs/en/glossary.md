# General glossary

[Home](../../README.en.md) | [Türkçe](../tr/kavram-sozlugu.md)

This starter glossary is not a complete reference for the course. Session-specific glossaries are linked from each session page.

| Term | Short explanation |
|---|---|
| LLM | A large language model that generates text by predicting subsequent text pieces in context using patterns learned from data. |
| Token | A unit of text processed by a model; it does not always correspond to a whole word. |
| Embedding | A way to represent an item as a vector of numbers. |
| API | An interface through which software requests functions or data according to specified rules. |
| Tool | A function or capability that an application makes available to a model under controlled conditions. |
| Schema | A definition of a data structure and applicable constraints. |
| Agent loop | A repeated process involving model proposals, tool results, and application control steps. |
| State | Information used by an application during its operation that can change over time. |
| Guardrail | A control used to limit or detect unwanted behavior. |
| Eval | A systematic evaluation of a system against defined criteria. |
| MCP | An open integration protocol (Model Context Protocol) that lets agent applications discover and invoke tools and resources in a standard format. |
| Skill | A procedural instruction bundle describing how to carry out a specific workflow, loaded into context only when needed. |
| Routing | Directing an incoming request to the right handler among a rule gate, a decision layer, a small model, or specialist agents. |
| Handoff | Transferring task control, along with the goal and constraints, from one agent or component to another. |
| SLM | A small autoregressive language model suited to fast, low-cost text drafts or straightforward responses. |
| System 1 decision model | A fast non-autoregressive reflex model—such as closed-source `Jev` or open-weight (~100M, Apache-2.0) `Laya`—returning typed primitives (`Choice`, `Score`, `Noul`) in a single forward pass without syntax hallucination. |
| Multimodal LLM | A model class able to perceive visual, document, or audio inputs directly alongside text and invoke tools (`Gemma 4 12B` is natively multimodal). |
| World model | A specialist model or simulator that predicts how a physical, spatial, or operational environment changes after an action. |
| Agentic CLI | A terminal-native agent harness—such as `mistral-vibe` inside an isolated `uv` + Python `3.14` workspace (or `hermes-agent`)—combining local `127.0.0.1` `llama-server` inference, `MCP` discovery, `SKILL.md` / `AGENTS.md` progressive disclosure, and real file/shell tools. |
| KV cache & 1M+ prompt pool | Pairing `f8_e4m3` (FP8) KV quantization on `llama.cpp v1.0.0`, `--kv-unified` shared slot buffers (`524,288` `512K` GPU KV on T4/L4, `1,048,576` on G4/A100), `--cache-reuse`, and `--cache-ram` to sustain a model's `262,144` (`256K`) max active context inside a `1M+` total KV pool. |

The glossary will grow alongside the session materials.
