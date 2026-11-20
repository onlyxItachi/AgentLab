# Demos: Modern Agent Stack

[Back to session](../README.en.md) | [Türkçe](README.md) | [Lesson notes](../lesson-notes.md) | [Glossary](../glossary.md) | [Exercises](../exercises/README.en.md)

The Session 03 live notebooks follow the **Studio v2 7-cell `#@title` form layout (`1` markdown intro + `6` hidden-code form cells with `cellView: "form"`)**. Participants never hunt inside raw code for `True`/`False` switches; every step runs with a single **`▶`** click.

> **Hardware Lineup Matching (`G4` / `L4` / `T4` — Strict Fail-Closed `ALAB-E02`):**
> - **[AgentLab-Session03-G4.ipynb](modern-agent-stack/AgentLab-Session03-G4.ipynb)** — Colab **Ultra / Pro** (`RTX PRO 6000 Blackwell`, `Qwen 3.8 27B + MTP`, `Thinking: xhigh`, target+draft `f8_e4m3` FP8 KV, `1M` / `1,048,576` GPU KV + `8 GiB` host RAM, `262,144` active context, `draft_max=3`; rejects L4/T4 with `ALAB-E02`)
> - **[pro_AgentLab-Session03-L4.ipynb](modern-agent-stack/pro_AgentLab-Session03-L4.ipynb)** — Colab **Pro / Plus** (`NVIDIA L4`, `>= 20,000 MiB` VRAM, `Gemma 4 12B QAT + MTP`, `--reasoning on`, `512K` / `524,288` GPU KV + `8 GiB` host RAM cache, `draft_max=3`)
> - **[plus_AgentLab-Session03-T4.ipynb](modern-agent-stack/plus_AgentLab-Session03-T4.ipynb)** — Colab **Plus / Free** (`Tesla T4`, `~15 GB VRAM`, `Gemma 4 12B QAT + MTP`, `--reasoning on`, `512K` / `524,288` GPU KV + `3,072–6,144 MiB` host RAM cache, `draft_max=2`; `b12359` T4 baseline: `14,047 MiB` VRAM / `866 MiB` free headroom, `cached_tokens=182`, `324.07 tok/s` prefill, `41.69 tok/s` decode)
>
> If the connected GPU does not match the notebook tier, execution fails closed without silently falling back and renders a 2-line `ALAB-E02` card (`ALAB-E01` flags CPU-only runtimes).

## 7-Cell Form Architecture (Studio v2)

| Cell | `#@title` Heading / Role | What to Observe on Screen |
| --- | --- | --- |
| **Cell 0** | Intro Markdown card | 5-minute summary, Studio v2 flow, hardware lineup (`G4` / `L4` / `T4`), and `error-guide.pdf` / `hata-cozum-rehberi.pdf` note |
| **Cell 1** | `🚀 1. Tek Tuş Kurulum ve Model Motor Başlatma (Sadece ▶ Butonuna Bas)` (One-Click Setup & Launch) | Strict GPU check (`ALAB-E01`/`E02`), `MyDrive/AgentLab-Agent-Runtime` (`setup` + `day-03-modern-stack`) mount (`ALAB-E03`), `Qwen 3.8 27B + MTP` on G4 / `Gemma 4 12B QAT + MTP` on L4-T4 + `llama.cpp v1.0.0` (`b12359`, `ALAB-E04`), and timed `<Model> servinge hazır!` banner |
| **Cell 2** | `🔍 Deney 1 — MCP Araç Keşfi ve Progressive Disclosure Becerileri` | `SKILL_LIBRARY` (`policy-qa`, `incident-triage`) `saved_chars` savings and live `MCP` (`InProcessMCPServer`, `tools/list`, `campus_kb`, `ops_desk`, `media_world`, `mcp__campus_kb__read_doc`, `olmayan-belge` fail-closed) |
| **Cell 3** | `⚡ Deney 2 — Deterministik Kural Kapısı (0 Token) ve StructuredHandoff` | `0`-token `deterministic_gate` (`TR-204`, `6 saat * 8.88 CU`), constraint-preserving `StructuredHandoff` (`["T4", "14:00"]`, `max_handoffs=2`, `admin_agent` / `untrusted-ticket` rejection), and `System1DecisionGate` (`Jev`/`Laya`: `Choice`/`Score`/`Noul`) |
| **Cell 4** | `🧠 Deney 3 — System 1 -> System 2 Kademesi, Thinking ve Gerçek Kod Yürütme` | Isolated `ExperimentSession`, `Noul=0.48 < 0.75` escalation (`escalated_to_system2=True`), System 2 (`Qwen 3.8 27B` `xhigh` / `Gemma 4 12B` `--reasoning on`) running real Python code (`calc.py`), and `DualLayerSessionStore` + KV cache |
| **Cell 5** | `🖥️ Canlı Ajan Stüdyosu (Tam Ekran + Thinking + Kod Yürütme + KV)` (`Canlı Stüdyo`) | Portless, cookieless `google.colab.output` JS RPC WebUI: clickable live `💭 Thinking` CoT cloud + `🔧 Tool Call` streaming, Antigravity FIFO queue (`[✕ Sıradan Çıkar]`), `[KV Kaydet]`/`[Yükle]`, preset chips, **`[⛶ Tam Ekran]`** (`ESC`), **`[⏹ Durdur]`**, and **`[🔌 Arayüzü Kapat]`** (Kill Switch -> `ALAB-E07`) |
| **Cell 6** | `🛑 2. Güvenli Kapanış, Drive Kaydı ve GPU Bırakma (Tek Tık)` (Safe Shutdown) | Stops WebUI and `llama-server`, flushes Google Drive (`drive.flush_and_unmount()`), and releases the Colab VM (`runtime.unassign()`, zero traceback even if Cell 1 was never run) |

## Runtime & KV Pool Configuration (Cell 1)

- **Tier-specific models (`llama.cpp v1.0.0 b12359`):** **`G4`** serves `Qwen 3.8 27B + MTP` (target+draft `f8_e4m3` FP8 KV, `1,048,576` `1M` GPU KV pool / `262,144` active context); **`L4`/`T4`** serve natively multimodal `Gemma 4 12B QAT + MTP` (~`7.699 GiB` / `8,266,977,117` bytes), backed by person-agnostic **`MyDrive/AgentLab-Agent-Runtime`** (`setup` shared across days + `day-03-modern-stack` per-day state).
- **Thinking mode & sampling:** `G4` (`Qwen 3.8 27B`) uses `enable_thinking=True` + `reasoning_effort="xhigh"` (`temperature=1.0`, `top_p=0.95`, `top_k=20`); `L4`/`T4` (`Gemma 4 12B`) uses binary `--reasoning on --reasoning-budget -1 --reasoning-preserve`, `enable_thinking=True`, `preserve_thinking=True`, and official Gemma 4 sampling (`temperature=1.0`, `top_p=0.95`, `top_k=64`); all tiers use streaming SSE, `id_slot=0`, `max_tokens=262144`, and `timeout=None`.
- **KV cache pools:** All tiers apply target+draft (`-ctkd/-ctvd`) **`f8_e4m3` (FP8)** KV quantization, `--spec-draft-p-min 0.75` (`--spec-draft-n-max`: T4 `2`, L4/G4 `3`), `--kv-unified --kv-unified-per-slot 262144`, `--ctx-checkpoints 8`, and `cache_prompt=True`: `G4` allocates `1,048,576` GPU KV (`--parallel 4`, `--cache-ram 8192`, `--cache-reuse 0` for hybrid Gated DeltaNet safety), while `L4`/`T4` pair `524,288` GPU KV + host RAM (`--cache-reuse 64`) for a **`1,048,576` (`1M+`) total pool** and **`262,144` max active context**.
- **Exact readiness banners:**
  - `🆕 İlk kurulum tamamlandı ve Drive'a yedeklendi (X.Y sn) — <Qwen 3.8 27B | Gemma 4> servinge hazır!`
  - `⚡ Drive önbelleğinden X.Y sn'de yüklendi — <Qwen 3.8 27B | Gemma 4> servinge hazır!`
  - `♻️ Açık sunucu algılandı, kaldığı yerden bağlandı (X.Y sn) — <Qwen 3.8 27B | Gemma 4> servinge hazır!`

## Independent Experiments, Live Studio & Error Armor

- **Out-of-order independent experiments (`Deney 1`–`Deney 3`):** After **Cell 1** completes, `Deney 1`, `Deney 2`, and `Deney 3` do not depend on one another and can run in any order (`ALAB-E05` flags if Cell 1 was skipped). `research_specialist` (`campus_kb`), `operations_specialist` (`ops_desk`), and `simulation_specialist` (`media_world` — T4-compatible `generate_architecture_diagram` & `simulate_lab_capacity` mockup) stay strictly within their allowed tool scopes; `SLM` vs closed `Jev` / open-weight ~100M Apache-2.0 `Laya` (`System1DecisionGate`: `Choice`, `Score`, `Noul`) contrasts and `DualLayerSessionStore` (`slot0.kv.bin` `binary_kv_hit` -> automatic `text_replay_fallback` on mismatch) are demonstrated directly.
- **Portless JS RPC WebUI (`Canlı Stüdyo`, Cell 5):** Avoids external ports and third-party cookies via native **`google.colab.output.register_callback`** + **`google.colab.kernel.invokeFunction`**. Includes preset chips (`105. Fibonacci Çalıştır`, `Python Maliyet Hesabı`, `Sandbox Kaçış Testi`) plus interactive `TR-204`, `MCP`, `StructuredHandoff`, and `System 1` testing, with **Fullscreen (`ESC`)**, **Stop (`Durdur`)**, and **Kill Switch (`Arayüzü Kapat`)** always accessible.
- **Fixed 2-line `ALAB-Exx` error armor:** Instead of raw Python stack traces, errors render as 2-line `ALAB-E01`–`ALAB-E10` or `ALAB-E99` cards (`🚨 [HATA KODU: ALAB-Exx] ...`). Check Drive's `error-guide.pdf` / `hata-cozum-rehberi.pdf` for step-by-step fixes, and record notes in `session-03.pdf` / `oturum-03.pdf`.
