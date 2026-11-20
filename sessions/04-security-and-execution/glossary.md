# Session glossary: Security, Execution & Human Oversight

[Back to session](README.en.md) | [Türkçe](kavram-sozlugu.md) | [General glossary](../../docs/en/glossary.md)

> **5-minute pre-read before the live workshop:** Skim these terms before class. As we pair `Qwen 3.8 27B + MTP` (`G4`, `xhigh`) or `Gemma 4 12B QAT + MTP` (`L4`/`T4`, `--reasoning on`) with real Python/Bash execution, this glossary maps the **Guardrails**, **Sandbox** isolation, **Trust Boundaries**, **Human-in-the-Loop (HITL)** intervention, and **Durable Execution** primitives you will observe on screen.

| Term | Meaning in this session and role in the lesson |
| --- | --- |
| `Guardrail` | Deterministic safety and validation control running before model inference (input) or before displaying/acting on output (`Deney 1`, `4.1`). |
| `Input guardrail` | Pre-inference filter rejecting oversized inputs, malformed schemas, disallowed patterns, or explicit override prompts before calling the LLM (`4.1`). |
| `Output guardrail` | Post-inference filter redacting leaked secrets, blocking unauthorized tool proposals, and catching ungrounded claims before side effects occur (`4.1`). |
| `Prompt injection` | Malicious instructions crafted to override system rules and hijack tool or code execution (`Deney 1`, `4.1`). |
| `Indirect prompt injection` | Hidden instructions embedded inside untrusted files, web pages, or support tickets read by the agent rather than typed directly by the user (`Deney 1`, `4.1`). |
| `Untrusted evidence` | Treating external documents/web/tickets strictly as passive data—tagged `"untrusted evidence, never instructions"`—never as executable commands (`4.1`). |
| `Runtime` | The execution environment where agent-proposed Python scripts and Bash shell commands actually run (`Deney 2`, `4.2`). |
| `Sandbox` | An isolated execution container confining real code/shell execution to an allowed directory, timeout, CPU/memory budget, and network policy (`Deney 2`, `4.2`). |
| `outside_workdir` | Sandbox path-enforcement block rejecting attempts to access parent directories (`../`), absolute host paths, or escaping symlinks (`Deney 2`, `ALAB-E08`). |
| `Execution timeout` | Hard time limit terminating runaway or infinite-loop Python/Bash subprocesses cleanly without hanging the runtime (`Deney 2`, `ALAB-E08`). |
| `Resource & network limits` | Process CPU/memory bounds paired with blocking outbound network egress outside local `127.0.0.1` loopback inference (`4.2`). |
| `Trust boundary` | The architectural dividing line between untrusted input/model text, the trusted harness policy engine, and privileged OS/filesystem resources (`4.3`). |
| `Least privilege` | Granting an agent or subprocess only the narrowest `read`, `write`, or `exec` permissions required for its scoped task (`4.3`). |
| `Permission tiers (read / write / exec)` | Separating read-only inspection (`read`), file modification (`write`), and command execution (`exec`) into distinct policy tiers (`4.3`). |
| `Allow / deny rules` | Explicit policy rules specifying which paths, commands, and actions are permitted (`allow`) or forbidden (`deny`) (`4.3`). |
| `Secret stripping` | Removing `AGENTLAB_LLAMA_KEY` and sensitive environment tokens from child subprocess environments and redacting secrets from logs and Drive exports (`Deney 2`–`3`, `4.3`). |
| `Risk gate` | Policy risk classifier deciding whether a proposed action auto-runs (low risk) or pauses for human intervention (`Deney 3`, `4.4`). |
| `Human-in-the-Loop (HITL)` | Pausing execution ahead of destructive or external side-effect actions to require explicit human inspection and approval (`Deney 3`, `4.4`). |
| `[Onayla] / [Reddet]` | Interactive `[Approve]` / `[Reject]` controls presented during an HITL pause alongside the model's `Thinking` trace and exact proposed command (`Deney 3`, `Canlı Stüdyo`). |
| `Pause-and-resume` | Halting execution cleanly at a risk boundary (`pause`) and continuing from the exact saved step (`resume`) once approved (`4.4`–`4.5`). |
| `Background agent` | An agent workflow capable of running long or approval-gated tasks asynchronously without locking a single synchronous turn (`4.5`). |
| `Durable execution` | Execution architecture preserving progress across disconnects, tab reloads, or multi-minute HITL pauses without losing state (`Deney 3`, `4.5`). |
| `Checkpoint & resume` | Saving full step state (`checkpoint_id`) before critical boundaries and recovering cleanly via `resume` rather than restarting from step 0 (`Deney 3`, `4.5`). |
| `ExperimentSession` | Independent isolated workspace and context created per experiment (`Deney 1`, `Deney 2`, `Deney 3`) so cells run cleanly in any order after Cell 1. |
| `MyDrive/AgentLab-Agent-Runtime` | Person-agnostic Google Drive layout separating shared multi-day `setup` (`Qwen 3.8 27B` / `Gemma 4` + `llama.cpp`) from Session 04's `day-04-security-execution` state (`Cell 1`, `Cell 6`). |
| `Thinking Mode (G4 xhigh / L4-T4 --reasoning on)` | Per-tier reasoning setup on `llama.cpp v1.0.0 b12359` (`max_tokens=262144`, `timeout=None`): `Qwen 3.8 27B + MTP` with `reasoning_effort="xhigh"` (`1.0/0.95/20`) on `G4`, and `Gemma 4 12B + MTP` with binary `--reasoning on --reasoning-budget -1 --reasoning-preserve` (`1.0/0.95/64`) on `L4`/`T4`. |
| `Live Studio (Canlı Stüdyo)` | Portless, cookieless Colab WebSocket WebUI (`Cell 5`: `register_callback` + `invokeFunction`) with **Fullscreen (`ESC`)**, **Stop (`Durdur`)**, **Kill Switch (`Arayüzü Kapat`)**, clickable `💭 Düşünce Akışı` CoT cards, **FIFO prompt queuing** (`[✕ Sıradan Çıkar]`), and collapsible `🔧 Araç & Komut`, `🛡️ HITL`, and `💻 Terminal` cards. |
| `Kill Switch (Arayüzü Kapat)` | Emergency UI control shutting down the `Canlı Stüdyo` WebUI background listener cleanly; re-run `Cell 5` to reopen (`ALAB-E07`). |
| `ALAB-Exx Error Armor` | Standardized 2-line error card (`🚨 [HATA KODU: ALAB-Exx] <Durum açıklaması>` + `İlgili dosyanın hata koduna bakın! Ve çözemezseniz yardım isteyin!`) replacing raw Python tracebacks (`ALAB-E01`–`ALAB-E99`). |
