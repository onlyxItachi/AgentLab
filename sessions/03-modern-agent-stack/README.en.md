# 03 — Modern Agent Stack

[Home](../../README.en.md) | [Türkçe](README.md)

**Duration:** Approximately 90 minutes. Before starting, recall harness validation, context budgeting, and memory boundaries from [session two](../02-agent-core-and-state/README.en.md).

In this session we scale session two's single-agent harness into a modular, production-style architecture. Instead of a hard-coded flat tool list, we discover `campus_kb`, `ops_desk`, and `media_world` dynamically at runtime (`tools/list`) over `MCP` (`JSON-RPC 2.0`, `InProcessMCPServer`), separate `Plugin` capabilities from `Skill` workflows using `Progressive Disclosure`, resolve deterministic requests (`TR-204`, CU math) at `0` tokens in `deterministic_gate`, enforce `StructuredHandoff` between least-privilege specialists, and bring together `System1DecisionGate` (`Jev` and open-weight ~100M Apache-2.0 `Laya` decision primitives: `Choice`/`Score`/`Noul`), `SLM`, `System 2` (**`Qwen 3.8 27B + MTP`** with `xhigh` Thinking on `G4`; natively multimodal **`Gemma 4 12B QAT + MTP`** with `--reasoning on` on `L4`/`T4`), `World Model` (`media_world` mockup), and dual-layer persistence (`DualLayerSessionStore`) inside a portless **Studio v2** experience.

> **Recommended pre-read:** Spend 5 minutes skimming the key terms in the [session glossary](glossary.md) before class so every live demo step is immediately familiar.

## Learning goals

- Separate `MCP`, `JSON-RPC 2.0`, `Plugin` (`campus_kb`, `ops_desk`, `media_world`), and `Skill` layers, and demonstrate runtime `tools/list` discovery on `InProcessMCPServer` alongside `Progressive Disclosure` context savings.
- Decide when an LLM is unnecessary, applying `deterministic_gate` (`0` tokens) and hybrid LLM-extraction + Python-validation workflows.
- Prevent `context loss` and privilege escalation (`admin_agent`) in multi-agent orchestration using scoped specialists, `StructuredHandoff`, and `max_handoffs=2`.
- Distinguish `System 1` decision primitives (`Jev` and open-weight ~100M Apache-2.0 `Laya`: `Choice`/`Score`/`Noul`, `RLCD`), `SLM`s, `System 2` (`G4`: `Qwen 3.8 27B + MTP` `xhigh` Thinking, target+draft `f8_e4m3` FP8 KV, `1,048,576` `1M` GPU KV pool; `L4`/`T4`: natively multimodal `Gemma 4 12B + MTP`, `llama.cpp v1.0.0 b12359`, `--reasoning on`, `f8_e4m3` FP8 KV, `524,288` `512K` GPU-resident KV; `262,144` max active context across tiers), T4-compatible `media_world` / `World Model` mockup orchestration, and `DualLayerSessionStore` (`binary_kv_hit` + `text_replay_fallback`), and verify `escalated_to_system2=True` escalation when `noul_confidence < 0.75` or payloads are malformed.

## Lesson sequence

| Minutes | Topic / observation |
| --- | --- |
| 0-8 | Bridge from session two harness and one-click setup (`Cell 1`: `Qwen 3.8 27B servinge hazır!` on G4 / `Gemma 4 servinge hazır!` on L4-T4) |
| 8-24 | Tool ecosystem: `MCP` (`tools/list`), `Plugin`, `Skill`, `Progressive Disclosure`, and **Deney 1** (`Cell 2`) |
| 24-44 | Deterministic rule gate (`0` tokens), multi-agent `StructuredHandoff`, `System1DecisionGate`, and **Deney 2** (`Cell 3`) |
| 44-66 | `System 1 -> System 2` escalation, `DualLayerSessionStore` + `f8_e4m3` FP8 KV cache, Thinking & live code execution, and **Deney 3** (`Cell 4`) |
| 66-85 | **Live Studio (`Canlı Stüdyo`)** (`Cell 5` portless JS RPC WebUI, `💭 Thinking` + `🔧 Tool Call` + KV save/restore) and small-group practice |
| 85-90 | `2. Safe Shutdown` (`Cell 6`: Drive flush + VM release) and transition to Session 04 |

## Materials

[Lesson notes](lesson-notes.md) | [Session glossary](glossary.md) | [Demos](demos/README.en.md) | [Exercises](exercises/README.en.md)

## 7-Cell One-Click `#@title` Form Architecture (Studio v2) & Hardware Lineup

Participants never hunt for hidden `True`/`False` flags inside code cells. Each Colab notebook uses **1 intro markdown cell + 6 hidden-code `#@title` form cells (`cellView: "form"`)**, exposing only a clear title and a **`▶`** run button (`Deney 1`–`Deney 3` are independent and run in any order after Cell 1):

1. **Cell 0 (Intro Markdown):** 5-minute summary, Studio v2 quick flow, hardware tier alignment, and `ALAB-Exx` error guide reference.
2. **Cell 1 — `🚀 1. Tek Tuş Kurulum ve Model Motor Başlatma (Sadece ▶ Butonuna Bas)` (One-Click Setup & Launch):** Enforces strict tier matching on the connected GPU (`G4` accepts only RTX PRO 6000 Blackwell; mismatches fail closed with `ALAB-E02`), mounts **`MyDrive/AgentLab-Agent-Runtime`** (`setup` shared + `day-03-modern-stack` daily state), and launches pinned `llama.cpp v1.0.0` (`b12359`, `timeout=None`): on **`G4`**, **`Qwen 3.8 27B + MTP`** (target+draft `f8_e4m3` FP8 KV, `reasoning_effort="xhigh"`, `1.0/0.95/20`, `--ctx-size 1048576 --parallel 4 --kv-unified --kv-unified-per-slot 262144 --ctx-checkpoints 8 --cache-reuse 0 --cache-ram 8192`, `draft_max=3`, `262,144` active context / `1,048,576` GPU KV pool); on **`L4`/`T4`**, **`Gemma 4 12B QAT + MTP`** (`--reasoning on --reasoning-budget -1 --reasoning-preserve`, `enable_thinking=True`, `preserve_thinking=True`, `1.0/0.95/64`, target+draft `f8_e4m3` FP8 KV, `--spec-draft-p-min 0.75`, `draft_max`: T4 `2`, L4 `3`, `524,288` GPU KV + RAM = `1,048,576` total pool), printing **`Qwen 3.8 27B servinge hazır!`** (`G4`) or **`Gemma 4 servinge hazır!`** (`L4`/`T4`) with exact elapsed seconds (`X.Y sn`).
3. **Cell 2 — `🔍 Deney 1 — MCP Araç Keşfi ve Progressive Disclosure Becerileri`:** Demonstrates `Progressive Disclosure` (`SKILL_LIBRARY`, `policy-qa`, `incident-triage`, `saved_chars`) and live `MCP` (`InProcessMCPServer`, `tools/list`, `campus_kb`, `ops_desk`, `media_world`, `olmayan-belge` fail-closed) tool calls alongside deterministic boundaries.
4. **Cell 3 — `⚡ Deney 2 — Deterministik Kural Kapısı (0 Token) ve StructuredHandoff`:** Verifies the `0`-token `deterministic_gate` (`TR-204` lookup and `6 saat * 8.88 CU` math), constraint-preserving multi-agent `StructuredHandoff` (`["T4", "14:00"]`, `max_handoffs=2`, rejecting `admin_agent` and `untrusted-ticket` injections), and the `System1DecisionGate` (`Jev` / open-weight ~100M Apache-2.0 `Laya`: `Choice`/`Score`/`Noul`) contract.
5. **Cell 4 — `🧠 Deney 3 — System 1 -> System 2 Kademesi, Thinking ve Gerçek Kod Yürütme`:** Creates an isolated `ExperimentSession` showcasing low-confidence `System 1` escalation (`Noul=0.48 < 0.75` -> `escalated_to_system2=True`) to System 2 (`Qwen 3.8 27B + MTP` `xhigh` on G4 / `Gemma 4 12B + MTP` `--reasoning on` on L4/T4), live sandboxed Python execution (`calc.py`), and `DualLayerSessionStore` + KV caching.
6. **Cell 5 — `🖥️ Canlı Ajan Stüdyosu (Tam Ekran + Thinking + Kod Yürütme + KV)` (`Canlı Stüdyo` / Live Studio):** Native **`google.colab.output`** JS RPC WebUI (`register_callback` + `invokeFunction`) with zero external ports or third-party cookies. Includes a collapsible clickable **`💭 Düşünce Akışı (Thinking)`** CoT cloud, **`🔧 Tool Call`** / output streaming, Antigravity-style **FIFO prompt queue (`[✕ Sıradan Çıkar]`)**, `[KV Kaydet]` / `[Yükle]` (`DualLayerSessionStore` `binary_kv_hit` + `text_replay_fallback` + `self.hist` sync), preset chips, **`[⛶ Tam Ekran]`** (`ESC` exits), **`[⏹ Durdur]`**, and **`[🔌 Arayüzü Kapat]`** (Kill Switch -> `ALAB-E07`).
7. **Cell 6 — `🛑 2. Güvenli Kapanış, Drive Kaydı ve GPU Bırakma (Tek Tık)` (Safe Shutdown):** Cleanly stops the WebUI and `llama-server`, flushes Google Drive (`drive.flush_and_unmount()`), and releases the VM (`runtime.unassign()`) with zero traceback even if Cell 1 was never run (`ALAB-E10` armor).

> **Colab Plan & GPU Lineup (`G4` / `L4` / `T4` — Strict Fail-Closed `ALAB-E02`):** Session 03 supports three plan-matched tiers:
> - **[AgentLab-Session03-G4.ipynb](demos/modern-agent-stack/AgentLab-Session03-G4.ipynb)** — Colab **Ultra / Pro** (`RTX PRO 6000 Blackwell`, `Qwen 3.8 27B + MTP`, `Thinking: xhigh`, target+draft `f8_e4m3` FP8 KV, `1M` / `1,048,576` GPU KV + `8 GiB` RAM, `262,144` active context, `draft_max=3`; fails closed with `ALAB-E02` if run on L4/T4)
> - **[pro_AgentLab-Session03-L4.ipynb](demos/modern-agent-stack/pro_AgentLab-Session03-L4.ipynb)** — Colab **Pro / Plus** (`NVIDIA L4`, `>= 20,000 MiB` VRAM, `512K` / `524,288` GPU KV + `8 GiB` host RAM cache, `draft_max=3`)
> - **[plus_AgentLab-Session03-T4.ipynb](demos/modern-agent-stack/plus_AgentLab-Session03-T4.ipynb)** — Colab **Plus / Free** (`Tesla T4`, `~15 GB VRAM`, `512K` / `524,288` GPU KV + `3,072–6,144 MiB` host RAM cache, `draft_max=2`; `b12359` T4 baseline: `14,047 MiB` VRAM, `cached_tokens=182`, `324.07 tok/s` prefill, `41.69 tok/s` decode)

> **Fixed 2-Line `ALAB-Exx` Error Armor:** Instead of raw Python stack traces, every cell renders a crisp 2-line diagnostic box (`🚨 [HATA KODU: ALAB-Exx] <Durum açıklaması>` followed by `İlgili dosyanın hata koduna bakın! Ve çözemezseniz yardım isteyin!`) covering `ALAB-E01`–`ALAB-E10` and `ALAB-E99`. Step-by-step solutions are documented in Drive's `error-guide.pdf` and `hata-cozum-rehberi.pdf`.

Printable Turkish (`oturum-03.pdf`) and English (`session-03.pdf`) student workbooks are distributed in the Google Drive workshop folder.

[Previous: Agent Architecture, Context and Memory](../02-agent-core-and-state/README.en.md) | [Next: Security & Execution](../04-security-and-execution/README.en.md)
