# 04 — Security, Execution & Human Oversight

[Home](../../README.en.md) | [Türkçe](README.md)

**Duration:** Approximately 90 minutes. Instead of spending lecture time re-teaching earlier days, read the **5-minute bridge summary from Days 1–3** below; full prior-day materials ([01](../01-llm-fundamentals/README.en.md), [02](../02-agent-core-and-state/README.en.md), [03](../03-modern-agent-stack/README.en.md)) stay available as self-study references.

In this session, we surround an agent that can now **write and execute real Python and Bash commands** with production-grade safety boundaries. First, we enforce input/output **Guardrails** and block direct and indirect **Prompt Injection** coming from untrusted files, web pages, or tickets (`4.1`); next, we isolate real execution inside a **`Sandbox`** (`outside_workdir` path containment, timeouts, resource and network limits) (`4.2`); then we separate **Permissions and Trust Boundaries** (`read` vs `write` vs `exec`, `allow`/`deny` rules, and **secret stripping**) (`4.3`); pause risky or destructive operations at a live **Human-in-the-Loop (HITL)** gate with **`[Onayla]` / `[Reddet]`** (`[Approve]` / `[Reject]`) controls (`4.4`); and sustain long-running tasks with **Background Agents & Durable Execution** (`checkpoint` / `resume` and Google Drive state persistence) (`4.5`).

> **Recommended pre-read:** Before class, spend 5 minutes reviewing the [5-Minute Bridge from Days 1–3](lesson-notes.md#5-minute-bridge-from-days-13) and the [session glossary](glossary.md).

## Learning goals

- `4.1` Build input/output **Guardrails** and detect or block direct and **indirect Prompt Injection** embedded inside untrusted files, web pages, or tickets (`untrusted evidence, never instructions`).
- `4.2` Confine real Python/Bash execution environments (**Runtime**) inside a **Sandbox** with directory/path isolation (`outside_workdir`), traversal rejection, execution timeouts, CPU/memory limits, and network controls.
- `4.3` Apply **Trust Boundaries** and **Least Privilege** across `read`, `write`, and `exec` tiers with explicit `allow`/`deny` policies, and scrub API keys or environment secrets via **secret stripping**.
- `4.4` Place a policy risk gate ahead of destructive or external actions for **Human-in-the-Loop (HITL)** pause-and-resume intervention using interactive **`[Onayla]` / `[Reddet]`** (`[Approve]` / `[Reject]`) controls.
- `4.5` Support asynchronous **Background Agents** and **Durable Execution** using step **checkpoints**, crash recovery / **`resume`** state, and Google Drive persistence.

## Lesson sequence

| Minutes | Topic / observation |
| --- | --- |
| 0-5 | **5-Minute Bridge from Days 1–3** (4 prerequisites) and one-click setup (`Cell 1`) |
| 5-22 | `4.1` Input/output **Guardrails**, direct/indirect **Prompt Injection**, and **Experiment 1** |
| 22-40 | `4.2` Unprotected vs **Sandboxed** real Python/Bash execution, `outside_workdir`, and **Experiment 2** |
| 40-56 | `4.3` **Trust Boundaries**, `read`/`write`/`exec` `allow`/`deny` tiers, and **secret stripping** |
| 56-74 | `4.4` & `4.5` Live risk gate, **`[Onayla]` / `[Reddet]`** **HITL**, **Durable Execution** (`checkpoint`/`resume`), and **Experiment 3** |
| 74-87 | **Live Studio** (`Cell 5` portless WebUI, `💭 Thinking` + `🛡️ HITL` + `💻 Live Terminal`) and small-group practice |
| 87-90 | `2. Safe Shutdown` (`Cell 6`), Drive flush, VM release, and transition to Session 05 |

## Materials

[Lesson notes](lesson-notes.md) | [Session glossary](glossary.md) | [Demos](demos/README.en.md) | [Exercises](exercises/README.en.md)

## 7-Cell One-Click `#@title` Form UX and Hardware Lineup

Participants never hunt for hidden `True`/`False` flags inside code cells. Each Colab notebook uses **1 intro markdown cell + 6 hidden-code `#@title` form cells (`cellView: "form"`)**, exposing only a clear title and a **`▶`** run button:

1. **Cell 0 (Intro Markdown):** 5-minute Days 1–3 bridge summary, tier alignment, and one-click workflow overview.
2. **Cell 1 — `1. Tek Tuş Kurulum ve Model Motor Başlatma` (One-Click Setup & Engine Launch):** Enforces strict tier verification on the connected GPU (`G4` requires RTX PRO 6000 Blackwell; mismatches fail closed with `ALAB-E02`), mounts **`MyDrive/AgentLab-Agent-Runtime`** (`setup` shared + `day-04-security-execution` daily state), and launches pinned `llama.cpp v1.0.0` (`b12359`, `timeout=None`, `id_slot=0`, `max_tokens=262144`) with streaming SSE: **`Qwen 3.8 27B + MTP`** on `G4` (`reasoning_effort="xhigh"`, `enable_thinking=True`, `1.0/0.95/20`, target+draft `f8_e4m3` FP8 KV, `--ctx-size 1048576 --parallel 4 --kv-unified --kv-unified-per-slot 262144 --ctx-checkpoints 8 --cache-reuse 0 --cache-ram 8192`, `draft_max=3`, `262,144` active context / `1,048,576` GPU KV pool) and **`Gemma 4 12B QAT + MTP`** on `L4`/`T4` (binary `--reasoning on --reasoning-budget -1 --reasoning-preserve`, `enable_thinking=True`, `preserve_thinking=True`, `1.0/0.95/64`, `f8_e4m3` FP8 KV).
3. **Cell 2 — `Deney 1` (`Experiment 1`):** Input/output **Guardrails** and direct/indirect **Prompt Injection** defense (`4.1`).
4. **Cell 3 — `Deney 2` (`Experiment 2`):** Unprotected vs **Sandboxed** real Python and Bash execution (`4.2` & `4.3` — `outside_workdir`, timeouts, resource/network limits, secret stripping).
5. **Cell 4 — `Deney 3` (`Experiment 3`):** **Trust Boundaries**, live policy risk gate + **`[Onayla]` / `[Reddet]`** **HITL** pause-and-resume, and **Durable Execution** `checkpoint`/`resume` (`4.3`–`4.5`).
6. **Cell 5 — `Canlı Stüdyo` (`Live Studio`):** Portless, third-party-cookieless local Colab WebSocket WebUI (`google.colab.output.register_callback` + `google.colab.kernel.invokeFunction`). Features top controls for **Fullscreen** (`ESC` exits), **Stop (`Durdur`)**, and **Close UI (`Arayüzü Kapat` Kill Switch)**, clickable **`💭 Düşünce Akışı`** CoT cards, Antigravity-style **FIFO prompt queue** (subsequent prompts wait cleanly during streaming or an active `[✅ Onayla]`/`[🛑 Reddet]` HITL gate, with `[✕ Sıradan Çıkar]`), plus collapsible **`🔧 Araç & Komut`**, **`🛡️ HITL Onay/Red`**, and **`💻 Canlı Terminal`** cards (external CLI setup is unnecessary and removed).
7. **Cell 6 — `2. Güvenli Kapanış, Drive Kaydı ve GPU Bırakma` (Safe Shutdown, Drive Save & GPU Release):** Stops WebUI tasks, flushes session/checkpoint logs (`drive.flush_and_unmount()`), shuts down `llama-server`, and unassigns the Colab VM cleanly.

> **Colab Plan & GPU Lineup (`G4` / `L4` / `T4` — Strict Fail-Closed `ALAB-E02`):** Session 04 targets three tiers with zero silent fallback on hardware mismatches (`ALAB-E02`):
> - **[AgentLab-Session04-G4.ipynb](demos/security-and-execution/AgentLab-Session04-G4.ipynb)** — Colab **Ultra** & **Pro** (`RTX PRO 6000 Blackwell`, `Qwen 3.8 27B + MTP`, `Thinking: xhigh`, target+draft `f8_e4m3` FP8 KV, `1M` / `1,048,576` GPU KV + `8 GiB` host RAM, `262,144` active context, `draft_max=3`)
> - **[pro_AgentLab-Session04-L4.ipynb](demos/security-and-execution/pro_AgentLab-Session04-L4.ipynb)** — Colab **Pro / Plus** (`NVIDIA L4`, `23 GB VRAM`, `512K` / `524,288` GPU KV + `8 GiB` host RAM cache)
> - **[plus_AgentLab-Session04-T4.ipynb](demos/security-and-execution/plus_AgentLab-Session04-T4.ipynb)** — Colab **Plus / Free** (`Tesla T4`, `15 GB VRAM`, fallback `512K` / `524,288` GPU KV + `3 GiB` host RAM cache)

> **Fixed 2-Line `ALAB-Exx` Error Armor:** Instead of raw Python stack traces, every failure prints a crisp two-line box (`🚨 [HATA KODU: ALAB-Exx] <Durum açıklaması>` followed by `İlgili dosyanın hata koduna bakın! Ve çözemezseniz yardım isteyin!`). Step-by-step fixes for students and staff are included in the shared Google Drive resources `hata-cozum-rehberi.pdf` (TR) and `error-guide.pdf` (EN).

Printable student workbooks (`oturum-04.pdf` / `session-04.pdf`) and `ALAB-Exx` error guides (`hata-cozum-rehberi.pdf` / `error-guide.pdf`) are shared in the Google Drive workshop folder.

[Previous: Modern Agent Stack](../03-modern-agent-stack/README.en.md) | [Next: Infrastructure, Performance & Evals](../05-infrastructure-and-evals/README.en.md)
