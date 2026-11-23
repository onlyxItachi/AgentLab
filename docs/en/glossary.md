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
| Guardrails | Deterministic safety and validation controls running before model inference (input) and before displaying or acting on output (output) to stop policy violations or secret leaks. |
| Eval | A systematic evaluation of a system against defined criteria. |
| MCP | An open integration protocol (Model Context Protocol) that lets agent applications discover and invoke tools and resources in a standard format. |
| Skill | A procedural instruction bundle describing how to carry out a specific workflow, loaded into context only when needed. |
| Routing | Directing an incoming request to the right handler among a rule gate, a decision layer, a small model, or specialist agents. |
| Handoff | Transferring task control, along with the goal and constraints, from one agent or component to another. |
| SLM | A small autoregressive language model suited to fast, low-cost text drafts or straightforward responses. |
| System 1 decision model | A fast non-autoregressive reflex model—such as closed-source `Jev` or open-weight (~100M, Apache-2.0) `Laya`—returning typed primitives (`Choice`, `Score`, `Noul`) in a single forward pass without syntax hallucination. |
| Multimodal LLM | A model class able to perceive visual, document, or audio inputs directly alongside text and invoke tools (`Gemma 4 12B` is natively multimodal). |
| World model | A specialist model or simulator that predicts how a physical, spatial, or operational environment changes after an action. |
| Agentic CLI | A terminal-native agent harness combining local `127.0.0.1` `llama-server` inference, `MCP` discovery, `SKILL.md` / `AGENTS.md` progressive disclosure, and real file/shell tools. |
| KV cache & 1M+ prompt pool | Pairing `f8_e4m3` (FP8) KV quantization on `llama.cpp v1.0.0`, `--kv-unified` shared slot buffers (`524,288` `512K` GPU KV on T4/L4, `1,048,576` on G4), `--cache-reuse`, and `--cache-ram` to sustain a model's `262,144` (`256K`) max active context inside a `1M+` total KV pool. |
| Prompt Injection | Malicious instructions crafted to override system rules or hijack tool calls; indirect attacks embedded inside files, web pages, or tickets are quarantined as `"untrusted evidence, never instructions"`. |
| Sandbox | An isolated execution container confining agent-written Python and Bash execution with `outside_workdir` path containment, hard `timeout`, CPU/memory caps, and disabled outbound networking. |
| Trust Boundary | The boundary separating untrusted inputs/LLM proposals, the trusted harness policy gate, and privileged OS resources—enforced via least-privilege `read`/`write`/`exec` `allow`/`deny` rules and `secret stripping`. |
| Human-in-the-Loop (HITL) | An approval gate pausing risky, destructive, or external actions to display the model's `Thinking` trace and exact command for explicit `[Onayla]` / `[Reddet]` (`[Approve]` / `[Reject]`) human intervention. |
| Durable Execution | Execution architecture saving step `checkpoint` state and Google Drive persistence so long-running or HITL-paused workflows recover cleanly via `resume` across disconnects. |
| Studio v2 | The zero-flag-hunting **7-cell `#@title` form** UX in Session 03–05 notebooks, combining one-click setup, independent experiments, the portless `google.colab.output` JS RPC `Canlı Stüdyo` WebUI, `DualLayerSessionStore`, and safe VM teardown. |
| ALAB-Exx | Standardized 2-line error card (`ALAB-E01`–`ALAB-E99`) replacing raw Python tracebacks across AgentLab Colab notebooks, mapped to step-by-step fixes in `error-guide.pdf`. |
| Roofline & Memory Wall | The performance model distinguishing memory-bandwidth-limited single-stream decode (`GEMV`) from compute-bound prefill or batched matrix multiplications (`GEMM`). |
| Chunked Prefill & Continuous Batching | Serving technique that splits prompt ingestion (`--ubatch-size` `GEMM` chunks) and schedules active slot iterations together to saturate `Tensor Cores` without stalling running requests. |
| Prefix Caching | Reusing cached KV blocks (`cache_prompt=True`) for unchanged system prompts and tool schemas so repeated turns skip redundant prefill work and slash `TTFT`. |
| Speculative Decoding (MTP & DFLASH) | Lossless decoding acceleration where lightweight multi-token heads (`MTP`) or parallel block diffusion (`DFLASH`) propose multiple draft tokens verified in one target-model pass. |
| Joule/Token & $/1M Token | Production energy efficiency (`Watt / tok_s`) and per-million-token inference economics measuring how batching and hardware bandwidth reduce per-token cost. |
| Observability & Span Tracing | Telemetry discipline combining server `/metrics` and `timings` with structured `llm_prefill`, `llm_decode`, and `tool_exec` spans to pinpoint latency bottlenecks. |
| Trajectory Eval & LLM-as-a-Judge | Multi-layer evaluation verifying deterministic tool/step trajectories alongside rubric-based `LLM-as-a-Judge` scoring for open-ended reasoning quality. |

The glossary will grow alongside the session materials.
