# Demos: Security, Execution & Human Oversight

[Back to session](../README.en.md) | [Türkçe](README.md) | [Lesson notes](../lesson-notes.md) | [Glossary](../glossary.md) | [Exercises](../exercises/README.en.md)

The Session 04 live notebooks use a **7-cell `#@title` form layout (`1` markdown intro + `6` hidden-code form cells with `cellView: "form"`)**. Participants never hunt inside raw code for `True`/`False` switches; every step runs with a single **`▶`** click.

> **Hardware Lineup Matching (`G4` / `L4` / `T4` — Strict Fail-Closed `ALAB-E02`):**
> - **[AgentLab-Session04-G4.ipynb](security-and-execution/AgentLab-Session04-G4.ipynb)** — Colab **Ultra / Pro** (`RTX PRO 6000 Blackwell`, `Qwen 3.8 27B + MTP`, `Thinking: xhigh`, target+draft `f8_e4m3` FP8 KV, `1M` / `1,048,576` GPU KV + `8 GiB` host RAM, `262,144` active context, `draft_max=3`; rejects L4/T4 with `ALAB-E02`)
> - **[pro_AgentLab-Session04-L4.ipynb](security-and-execution/pro_AgentLab-Session04-L4.ipynb)** — Colab **Pro / Plus** (`NVIDIA L4`, `Gemma 4 12B QAT + MTP`, `--reasoning on`, `512K` / `524,288` GPU KV + `8 GiB` host RAM cache)
> - **[plus_AgentLab-Session04-T4.ipynb](security-and-execution/plus_AgentLab-Session04-T4.ipynb)** — Colab **Plus / Free** (`Tesla T4`, `Gemma 4 12B QAT + MTP`, `--reasoning on`, `512K` / `524,288` GPU KV + `3 GiB` host RAM cache)
>
> If the connected GPU does not match the notebook tier, execution fails closed without silent fallback and displays a 2-line `ALAB-E02` card.

## 7-Cell Form Architecture

| Cell | `#@title` Heading / Role | What to Observe on Screen |
| --- | --- | --- |
| **Cell 0** | Intro Markdown card | 5-minute Days 1–3 bridge summary and hardware tier notes (`G4` / `L4` / `T4`) |
| **Cell 1** | `1. Tek Tuş Kurulum ve Model Motor Başlatma` (One-Click Setup & Launch) | Step-by-step emoji progress (`🔍 GPU doğrulanıyor...`, `📂 Drive önbelleği bağlanıyor...`, `🧠 Model GPU'ya yükleniyor...`, `🩺 Canlı çıkarım testi yapılıyor...`) and timed `<Qwen 3.8 27B | Gemma 4> servinge hazır!` banner |
| **Cell 2** | `Deney 1` — Guardrails & Prompt Injection (`4.1`) | Input/output guardrail checks plus blocking direct injection and indirect injection from untrusted files/web/tickets (`untrusted evidence, never instructions`) |
| **Cell 3** | `Deney 2` — Unprotected vs Sandboxed Execution (`4.2` & `4.3`) | Real Python and Bash execution, `outside_workdir` containment, `timeout`, resource/network limits, and secret stripping |
| **Cell 4** | `Deney 3` — Trust Boundaries, Live HITL & Durable Execution (`4.3`–`4.5`) | `read`/`write`/`exec` tiers, risk gate, interactive **`[Onayla]` / `[Reddet]`** (`[Approve]` / `[Reject]`) pause-and-resume controls, `checkpoint`/`resume`, and Drive state |
| **Cell 5** | `Canlı Stüdyo` — Portless, Cookieless Colab WebUI | Top bar with **Fullscreen** (`ESC` to exit), **Stop (`Durdur`)**, and **Close UI (`Arayüzü Kapat` Kill Switch)** plus clickable **`💭 Düşünce Akışı`** CoT cards, **FIFO prompt queue** (`[✕ Sıradan Çıkar]`), **`🔧 Araç & Komut`**, **`🛡️ HITL Onay/Red`**, and **`💻 Canlı Terminal`** cards (no external CLI needed) |
| **Cell 6** | `2. Güvenli Kapanış, Drive Kaydı ve GPU Bırakma` (Safe Shutdown) | Stops WebUI background tasks, flushes `MyDrive/AgentLab-Agent-Runtime/day-04-security-execution` state (`drive.flush_and_unmount()`), shuts down `llama-server`, and releases the VM (`unassign`) |

## Runtime Configuration (Cell 1)

- **Tier-specific infrastructure (`llama.cpp v1.0.0 b12359`):** **`G4`** serves `Qwen 3.8 27B + MTP` (target+draft `f8_e4m3` FP8 KV, `--ctx-size 1048576 --parallel 4 --kv-unified --kv-unified-per-slot 262144 --ctx-checkpoints 8 --cache-reuse 0 --cache-ram 8192`, `draft_max=3`, `262,144` active context / `1,048,576` GPU KV pool); **`L4`/`T4`** serve `Gemma 4 12B QAT + MTP` (`f8_e4m3` FP8 KV), backed by person-agnostic **`MyDrive/AgentLab-Agent-Runtime`** (`setup` shared across days + `day-04-security-execution` per-day state).
- **Thinking mode & sampling:** `G4` (`Qwen 3.8 27B`) sets `enable_thinking=True` + `reasoning_effort="xhigh"` (`temperature=1.0`, `top_p=0.95`, `top_k=20`); `L4`/`T4` (`Gemma 4 12B`) sets binary `--reasoning on --reasoning-budget -1 --reasoning-preserve`, `enable_thinking=True`, `preserve_thinking=True`, and official Gemma 4 sampling (`temperature=1.0`, `top_p=0.95`, `top_k=64`); all tiers use streaming SSE, `id_slot=0`, `max_tokens=262144`, and `timeout=None`.
- **Exact readiness banners:**
  - `🆕 İlk kurulum tamamlandı ve Drive'a yedeklendi (X.Y sn) — <Qwen 3.8 27B | Gemma 4> servinge hazır!`
  - `⚡ Drive önbelleğinden X.Y sn'de yüklendi — <Qwen 3.8 27B | Gemma 4> servinge hazır!`
  - `♻️ Açık sunucu algılandı (X.Y sn) — <Qwen 3.8 27B | Gemma 4> servinge hazır!`

## Live Studio WebUI & Independent Experiments

- **Isolated `ExperimentSession` runs:** After Cell 1 completes, `Deney 1`, `Deney 2`, and `Deney 3` each open their own clean workspace and context; they do not depend on one another and can be re-run in any order.
- **Portless local WebSocket transport:** `Canlı Stüdyo` (`Cell 5`) avoids third-party cookie port tunnels and communicates via `google.colab.output.register_callback` + `google.colab.kernel.invokeFunction` without locking Colab cell execution.
- **Error armor (`ALAB-E01` – `ALAB-E99`):** Instead of raw tracebacks, every error renders a fixed 2-line `ALAB-Exx` card. Step-by-step fixes appear in `error-guide.pdf` / `hata-cozum-rehberi.pdf` inside the shared Google Drive folder alongside `session-04.pdf`.
