# 05 — Infrastructure, Performance & Evals

[Home](../../README.en.md) | [Türkçe](README.md)

**Duration:** Approximately 90 minutes. Instead of spending lecture time re-teaching earlier days, read the **5-minute Day 1–4 bridge summary** below; full prior-day materials ([01](../01-llm-fundamentals/README.en.md), [02](../02-agent-core-and-state/README.en.md), [03](../03-modern-agent-stack/README.en.md), [04](../04-security-and-execution/README.en.md)) stay available as offline references.

In this session, we turn a working agent into a **measurable, fast, energy/cost-efficient, and verifiable production system**. First, we unpack the GPU memory hierarchy (`HBM → L2 → SRAM → Tensor Cores`), the **Roofline / Memory Wall**, **Chunked Prefill (`GEMM`)** vs. **Pure Decode (`GEMV`)**, **Continuous Batching**, quantization (`FP16/FP8/NVFP4/Q4_0`), **Speculative Decoding (`MTP` & `DFLASH`)**, and wafer-scale hardware (`Cerebras WSE-3 / WSE-3T`) (`5.1`). Next, we engineer **KV Cache & Prefix Caching** (`768 KB/tok` vs. `4 KB/tok` vs. `890 B/tok`) and diagnose the real Session 03 L4 three-way cache-miss case study (`5.2`), quantify AI Factory economics via **`$/1M Token` and `Joule/Token`** (`5.3`), instrument `/metrics` and **Span Tree Tracing** (`5.4`), and close with **Evals**, **Artificial Analysis Pareto** frontiers, and the **2026 Frontier Architecture Finale** (`5.5`).

> **Recommended pre-read:** Before class, spend 5 minutes reviewing the [5-Minute Day 1–4 Bridge Summary](lesson-notes.md#5-minute-day-14-bridge-summary), the [2026 AI Hardware Reference](hardware-reference-2026.md), and the [session glossary](glossary.md).

## Learning goals

- `5.1` Explain the GPU memory hierarchy, *memory-bound decode* (`GEMV`) vs. *compute-bound prefill/batch* (`GEMM`) on the **Roofline**, **Chunked Prefill (`--ubatch-size`)**, **Continuous Batching**, quantization, and **`MTP` / `DFLASH`** speculative decoding.
- `5.2` Compute **KV Cache** footprints from layer/head geometry (`768 KB/tok` → `4 KB/tok` → `890 B/tok`), measure **Prefix Caching (`cache_prompt=True`)** speedups, and diagnose cache misses caused by template token shifts, `SWA 1024`, and slot routing.
- `5.3` Use `$/1M Token` and `Joule/Token = Watt / tok_s` to compare single-stream (`batch=1`) vs. concurrent batching economics and energy (`T4 ~2.33 J/tok` vs. `G4 8-slot ~0.46 J/tok`).
- `5.4` Monitor production agent runs with server `/metrics`, `timings`, and structured **Span Trees** (`llm_prefill`, `llm_decode`, `tool_exec`).
- `5.5` Evaluate agent quality with deterministic checks, **Trajectory Evals**, **LLM-as-a-Judge** (and bias pitfalls), quantization accuracy comparisons, and **Artificial Analysis Pareto** frontiers across 2026 architectures.

## Lesson sequence

| Minutes | Topic / observation |
| --- | --- |
| 0-5 | **5-Minute Day 1–4 Bridge Summary** and one-click setup (`Cell 1`: `Gemma 4 12B QAT + MTP` across `G4/H100`, `L4`, `T4`) |
| 5-25 | `5.1` Memory hierarchy (`HBM → SRAM`), Roofline, `Cerebras WSE-3T`, `Chunked Prefill` vs. `Decode (GEMV)`, `MTP`/`DFLASH` + [Interactive Simulator](demos/inference-visualizer/prefill-decode-kv-sim.html) and **Experiment 1** |
| 25-44 | `5.2` KV Cache math, **Prefix Caching** (`Cold vs Warm`), L4 3-way Cache Miss case study, `5.3` **`$/1M Token` & `Joule/Token`**, and **Experiment 2** |
| 44-58 | `5.4` **Observability & Tracing** (`/metrics`, `timings`, `llm_prefill`/`llm_decode`/`tool_exec` span tree) |
| 58-74 | `5.5` **Evals** (Deterministic, Trajectory, LLM-as-a-Judge, Quantization Evals), **Artificial Analysis**, **2026 Frontier Finale**, and **Experiment 3** |
| 74-87 | **Live Studio** (`Cell 5` live telemetry: `Cached \| New`, `Output`, `tok/s` + `💭 Thinking` + code execution) and small-group practice |
| 87-90 | `2. Safe Shutdown` (`Cell 6`), Drive flush, VM release, and wrap-up for upcoming capstone practice |

> **Extracurricular Bonus:** See the closing [`Code Mode` (`Cloudflare & Anthropic Programmatic Tool Calling`)](lesson-notes.md#extracurricular-bonus-code-mode--batched-tool-calling--sandboxed-orchestration) section for how batched sandbox scripts cut MCP schema bloat and `N+1` tool round-trips by `90–99%`.

## Materials

[Lesson notes](lesson-notes.md) | [2026 Hardware Reference](hardware-reference-2026.md) | [Session glossary](glossary.md) | [Demos](demos/README.en.md) | [Exercises](exercises/README.en.md) | [Interactive Inference Simulator](demos/inference-visualizer/README.en.md)

## 7-Cell One-Click `#@title` Form UX and Hardware Lineup

Session 05 notebooks keep the **1 markdown intro cell + 6 hidden-code `#@title` form cells (`cellView: "form"`)** layout. For an **apples-to-apples** hardware comparison on Day 5, **all three tiers** run the same pinned **`Gemma 4 12B QAT + MTP`** model:

1. **Cell 0 (Intro Markdown):** 5-minute Day 1–4 bridge summary, hardware tier alignment, and simulator link.
2. **Cell 1 — `1. Tek Tuş Kurulum ve Gemma 4 Motor Başlatma` (One-Click Setup & Launch):** Enforces strict tier-matched GPU checks (`ALAB-E02`), mounts **`MyDrive/AgentLab-Agent-Runtime`** (`setup` shared + `day-05-infra-evals` daily state), and launches **`Gemma 4 12B QAT + MTP`** (`f8_e4m3` FP8 KV, `--cache-reuse 64`, `Thinking` enabled, streaming SSE, `id_slot=0`, `max_tokens=262144`, `timeout=None`).
3. **Cell 2 — `Deney 1` (`Experiment 1`):** `Gemma 4 12B` `config.json` tensor dimensions & KV math (`768 KB/tok` vs. `4 KB/tok` vs. `890 B/tok`), mini shape/cache demo, and live short vs. long prompt benchmark reporting `TTFT (ms)`, `Prefill tok/s`, and `Decode tok/s` (`5.1`).
4. **Cell 3 — `Deney 2` (`Experiment 2`):** `Cold Prefill` vs. `Warm Prefix Cache` (`cache_prompt=True`, `cached_tokens`, `prompt_ms` speedup), single-user (`1`) vs. Continuous Batching (`8` slots G4/H100, `2` L4/T4) integrated `nvidia-smi` power → **`Total Energy / Total Tokens` (`Joule/Token`)** & **`CU / 1M Token`** reduction, plus verified 2026 hardware reference comparison (`5.2` & `5.3`).
5. **Cell 4 — `Deney 3` (`Experiment 3`):** Traced multi-step agent emitting JSON **Span Traces** (`llm_prefill`, `llm_decode`, `tool_exec` saved under `day-05-infra-evals`), 3-check **Mini Agent Eval Suite** (deterministic JSON/tool + trajectory + LLM-as-a-Judge), and the 2026 Frontier Architectures comparison (`5.4` & `5.5`).
6. **Cell 5 — `Canlı Stüdyo` (`Live Studio`):** Portless, cookieless local Colab WebSocket WebUI (`google.colab.output.register_callback` + `google.colab.kernel.invokeFunction`). Features **Fullscreen (`ESC`)**, **Stop (`Durdur`)**, **Kill Switch (`Arayüzü Kapat`)**, FIFO queue, Day 5 preset chips (`⚡ Prefill/Decode & KV Hesapla`, `📊 3 Adımlı Traced Python Analizi`, `🏆 2026 Mimarileri Karşılaştır`), and live per-turn **`Cached | New`**, **`Output`**, and **`tok/s`** telemetry.
7. **Cell 6 — `2. Güvenli Kapanış, Drive Kaydı ve GPU Bırakma` (Safe Shutdown):** Stops WebUI tasks, flushes `day-05-infra-evals` traces and logs (`drive.flush_and_unmount()`), shuts down `llama-server`, and releases the Colab VM (`unassign`).

> **Colab Plan & GPU Lineup (`G4 / H100` · `L4` · `T4` — All `Gemma 4 12B QAT + MTP`):**
> - **[AgentLab-Session05-G4.ipynb](demos/infrastructure-and-evals/AgentLab-Session05-G4.ipynb)** — Colab **Ultra** & **Pro+** (`RTX PRO 6000 Blackwell [G4]` or `NVIDIA H100`, `1M` / `1,048,576` GPU KV pool, `262,144` active context)
> - **[pro_AgentLab-Session05-L4.ipynb](demos/infrastructure-and-evals/pro_AgentLab-Session05-L4.ipynb)** — Colab **Pro / Plus** (`NVIDIA L4`, `23 GB VRAM`, `512K` / `524,288` GPU KV + `8 GiB` host RAM cache)
> - **[plus_AgentLab-Session05-T4.ipynb](demos/infrastructure-and-evals/plus_AgentLab-Session05-T4.ipynb)** — Colab **Plus / Free** (`Tesla T4`, `15 GB VRAM`, `512K` / `524,288` GPU KV + `3 GiB` host RAM cache)
> - **[prefill-decode-kv-sim.html](demos/inference-visualizer/prefill-decode-kv-sim.html)** — Zero-install, 100% offline 4-tab + math-drawer interactive stage simulator ([visualizer guide](demos/inference-visualizer/README.en.md))

> **Fixed 2-Line `ALAB-Exx` Error Armor:** Every failure renders a crisp 2-line diagnostic box (`🚨 [HATA KODU: ALAB-Exx] <Durum açıklaması>` followed by `İlgili dosyanın hata koduna bakın! Ve çözemezseniz yardım isteyin!`). Step-by-step fixes for students and staff are included in the shared Google Drive resources `hata-cozum-rehberi.pdf` (TR) and `error-guide.pdf` (EN).

Printable student workbooks (`oturum-05.pdf` / `session-05.pdf`) and `ALAB-Exx` error guides (`hata-cozum-rehberi.pdf` / `error-guide.pdf`) are shared in the Google Drive workshop folder.

[Previous: Security & Execution](../04-security-and-execution/README.en.md) | [Home](../../README.en.md)
