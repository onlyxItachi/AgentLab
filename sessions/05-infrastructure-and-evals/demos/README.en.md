# Demos: Infrastructure, Performance & Evals

[Back to session](../README.en.md) | [Türkçe](README.md) | [Lesson notes](../lesson-notes.md) | [2026 Hardware Reference](../hardware-reference-2026.md) | [Glossary](../glossary.md) | [Exercises](../exercises/README.en.md)

Session 05 live notebooks use a **7-cell `#@title` form layout (`1` markdown intro + `6` hidden-code form cells with `cellView: "form"`)**. Participants never hunt inside raw code for `True`/`False` flags; every step runs with a single **`▶`** click.

> **Hardware Lineup Matching (`G4 / H100` · `L4` · `T4` — All `Gemma 4 12B QAT + MTP`):**
> - **[AgentLab-Session05-G4.ipynb](infrastructure-and-evals/AgentLab-Session05-G4.ipynb)** — Colab **Ultra / Pro+** (`RTX PRO 6000 Blackwell [G4]` or `NVIDIA H100`, `1M` / `1,048,576` GPU KV pool, `262,144` active context)
> - **[pro_AgentLab-Session05-L4.ipynb](infrastructure-and-evals/pro_AgentLab-Session05-L4.ipynb)** — Colab **Pro / Plus** (`NVIDIA L4`, `512K` / `524,288` GPU KV + `8 GiB` host RAM cache)
> - **[plus_AgentLab-Session05-T4.ipynb](infrastructure-and-evals/plus_AgentLab-Session05-T4.ipynb)** — Colab **Plus / Free** (`Tesla T4`, `512K` / `524,288` GPU KV + `3 GiB` host RAM cache)
>
> If the connected GPU does not match the notebook tier (the `g4` notebook strictly accepts `G4` or `H100`), a fixed 2-line **`ALAB-E02`** card explains how to switch runtimes or pick the matching notebook.

## Interactive Offline Simulator (Zero Install)

- **[prefill-decode-kv-sim.html](inference-visualizer/prefill-decode-kv-sim.html)** ([guide](inference-visualizer/README.en.md)) — 100% self-contained 4-tab + math-drawer simulator working offline in any browser or inside Colab `IPython.display.HTML` with zero external CDNs:
  1. **Tab 1 (`🏗️ GPU Bellek Hiyerarşisi & Cerebras WSE`):** `HBM → L2 → SRAM → Tensor Cores`, live **Roofline** gauge, and 2026 hardware selector.
  2. **Tab 2 (`⚡ Chunked Prefill (ubatch) vs Decode (GEMV) vs Batching`):** Interactive `--ubatch-size` and `Concurrent Users N` sliders turning `[B × 3840]` GEMM ↔ `[1 × 3840]` GEMV ↔ `[N × 3840]` GEMM while `$/1M Token` and `Joule/Token` drop live.
  3. **Tab 3 (`🗄️ KV Cache, Prefix Caching & Mimari Sıkıştırma`):** Live KV footprint calculator (`768 KB/tok` vs. `4 KB/tok` `Gemma 4 12B` vs. `890 B/tok` `DeepSeek-V4.1-Flash`), `Cold vs Warm` timeline, and the Session 03 L4 3-way Cache Miss case study.
  4. **Tab 4 (`🚀 Saf Decode vs MTP vs DFLASH & 2026 Mimariler`):** 3-lane speculative race with acceptance-rate slider (`α`) + 2026 Frontier Pareto cards.

## 7-Cell Form Architecture

| Cell | `#@title` Heading / Role | What to Observe on Screen |
| --- | --- | --- |
| **Cell 0** | Intro Markdown card | 5-minute Day 1–4 bridge summary and apples-to-apples `Gemma 4 12B QAT + MTP` tier notes |
| **Cell 1** | `1. Tek Tuş Kurulum ve Gemma 4 Motor Başlatma` (One-Click Setup & Launch) | Step-by-step emoji progress and timed ready banner for `Gemma 4 12B QAT + MTP` (`f8_e4m3` FP8 KV, `--cache-reuse 64`, `Thinking` on) |
| **Cell 2** | `Deney 1` — Prefill (`ubatch`) vs. Decode (`GEMV`), KV Math & Mini Simulator | `Gemma 4 12B` `config.json` dimensions, KV bytes/tok comparison, mini shape/cache demo, and live short vs. long prompt `TTFT (ms)`, `Prefill tok/s`, and `Decode tok/s` |
| **Cell 3** | `Deney 2` — Caching (`Cold vs Warm`), Cost (`CU/1M Token`), & Energy (`Joule/Token`) | Identical long prompt `Cold Prefill` vs. `Warm Prefix Cache` (`cached_tokens`, `prompt_ms`, speedup), live `nvidia-smi` `Watt` → **`Joule/Token`** & **`CU/1M Token`** + 2026 hardware reference rows |
| **Cell 4** | `Deney 3` — Observability Span Trace, Mini Agent Eval Suite & 2026 Architectures | Multi-step agent JSON span traces (`llm_prefill`, `llm_decode`, `tool_exec` saved under `day-05-infra-evals`), 3-check Mini Eval Suite (deterministic + trajectory + LLM-as-a-Judge), and 2026 Frontier Architectures table |
| **Cell 5** | `Canlı Stüdyo` — Portless, Cookieless Colab WebUI (+ Live Telemetry) | **Fullscreen (`ESC`)**, **Stop (`Durdur`)**, **Kill Switch (`Arayüzü Kapat`)**, FIFO queue, Day 5 preset chips (`⚡ Prefill/Decode & KV Hesapla`, `📊 3 Adımlı Traced Python Analizi`, `🏆 2026 Mimarileri Karşılaştır`), and per-turn **`Cached \| New`**, **`Output`**, and **`tok/s`** telemetry |
| **Cell 6** | `2. Güvenli Kapanış, Drive Kaydı ve GPU Bırakma` (Safe Shutdown) | Stops WebUI tasks, flushes `MyDrive/AgentLab-Agent-Runtime/day-05-infra-evals` state (`drive.flush_and_unmount()`), shuts down `llama-server`, and releases the VM (`unassign`) |

## Runtime Configuration (Cell 1)

- **Shared apples-to-apples model (`Gemma 4 12B QAT + MTP`):** Every tier runs `gemma-4-12B-it-Q4_0.gguf` + `mtp-gemma-4-12B-it-Q4_0.gguf` (`1.0/0.95/64`, **`f8_e4m3` FP8 KV**, `--cache-reuse 64`, `draft_max=3`, `--reasoning on --reasoning-budget -1 --reasoning-preserve`, `enable_thinking=True`, `preserve_thinking=True`); only hardware bandwidth and GPU KV pool capacity scale across tiers (`G4/H100`: `1M` / `1,048,576`, `L4`: `512K` + `8 GiB` host RAM, `T4`: `512K` + `3 GiB` host RAM).
- **Exact readiness banners:**
  - `🆕 İlk kurulum tamamlandı ve Drive'a yedeklendi (X.Y sn) — Gemma 4 12B QAT + MTP servinge hazır!`
  - `⚡ Drive önbelleğinden X.Y sn'de yüklendi — Gemma 4 12B QAT + MTP servinge hazır!`
  - `♻️ Açık sunucu algılandı (X.Y sn) — Gemma 4 12B QAT + MTP servinge hazır!`

## Live Studio WebUI & Independent Experiments

- **Isolated `ExperimentSession` runs:** After Cell 1 finishes, `Deney 1`, `Deney 2`, and `Deney 3` each run in an isolated workspace and can be re-executed in any order.
- **Portless local WebSocket transport:** `Canlı Stüdyo` (`Cell 5`) uses `google.colab.output.register_callback` + `google.colab.kernel.invokeFunction` with no third-party cookie port tunnels and without locking the Colab cell.
- **Error armor (`ALAB-E01` – `ALAB-E99`):** Errors render a 2-line `ALAB-Exx` box. Step-by-step fixes appear in `error-guide.pdf` / `hata-cozum-rehberi.pdf` inside the shared Google Drive folder alongside `session-05.pdf`.
