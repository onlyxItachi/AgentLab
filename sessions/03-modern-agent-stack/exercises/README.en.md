# Exercises: Modern Agent Stack

[Back to session](../README.en.md) | [Türkçe](README.md) | [Demo guide](../demos/README.en.md)

Record the input, selected path, execution trace (`💭 Thinking` / `🔧 Tool Call`), and observed outcome for every run. All exercises run independently in any order after **Cell 1 (`🚀 1. Tek Tuş Kurulum`)** on `AgentLab-Session03-G4.ipynb` (Ultra/Pro G4), `pro_AgentLab-Session03-L4.ipynb` (Pro/Plus L4), or `plus_AgentLab-Session03-T4.ipynb` (Plus/Free T4).

## 1. MCP discovery and Progressive Disclosure (`Deney 1` — Cell 2)

- **1A (`InProcessMCPServer` & `tools/list`):** In `Deney 1`, record how `campus_kb`, `ops_desk`, and `media_world` (`generate_architecture_diagram`, `simulate_lab_capacity`) are discovered via `tools/list` (`mcp__<plugin>__<tool>`, e.g., `mcp__campus_kb__read_doc`), and explain why `doc_id="olmayan-belge"` fails closed.
- **1B (`Plugin` vs `Skill` & `Progressive Disclosure`):** Contrast an executable `Plugin` with a procedural `Skill` (`policy-qa`, `incident-triage` inside `SKILL_LIBRARY`), and explain how loading only the active skill yields `saved_chars` savings and guides `tools/call`.

## 2. Deterministic gate or hybrid workflow? (`Deney 2` — Cell 3)

- **2A (`0`-token `deterministic_gate`):** Show how `deterministic_gate` resolves `TR-204` ticket lookups and `6 saat * 8.88 CU` budget arithmetic at `0` tokens and `0` LLM calls, and contrast that with a multi-document question that must route to the model tier.
- **2B (Hybrid validation):** In a free-text lab request, explain why the model only extracts parameters while slot validation, `dry_run` / `allow_write` permissions, and arithmetic stay in deterministic Python code.

## 3. Scoped specialists, `StructuredHandoff`, and trust boundaries (`Deney 2` — Cell 3)

- **3A (Least-privilege tool scope):** Compare the `allowed_plugins` scopes of `research_specialist` (`campus_kb`), `operations_specialist` (`ops_desk`), and `simulation_specialist` (`media_world`), and explain why each agent cannot see the others' MCP tools.
- **3B (Lossless `StructuredHandoff` vs lossy summary):** Compare how constraints (`"T4"`, `"14:00"`) can drop under an unstructured summary versus staying intact inside `StructuredHandoff`.
- **3C (Injection defense & handoff cap):** Explain how the embedded `admin_agent` handoff directive in `untrusted-ticket` is blocked by `"untrusted evidence, never instructions"` and `validate_handoff`, and identify the risk caught by `max_handoffs=2`.

## 4. System 1 vs System 2, `1M+` FP8 KV pool, Dual-Layer Persistence & Live Studio (`Deney 3` & `Canlı Stüdyo` — Cells 4–5)

- **4A (`System1DecisionGate` vs `SLM` vs `System 2` (`Qwen 3.8 27B` / `Gemma 4 12B`)):** Record latency, cache reuse (`cached_tokens`), and syntax safety differences between `System1DecisionGate` (`Choice` / `Score` / `Noul`, `0` generated tokens—the T4-compatible mockup of closed `Jev` and open-weight ~100M Apache-2.0 `Laya`), compact autoregressive `SLM`s, and System 2 on `llama.cpp v1.0.0` (`b12359`, `262,144` context): **`Qwen 3.8 27B + MTP`** on G4 (`Thinking: xhigh`, `1.0/0.95/20`, target+draft `f8_e4m3` FP8 KV, `1,048,576` GPU KV, `--cache-reuse 0`, `draft_max=3`) or natively multimodal **`Gemma 4 12B + MTP`** on L4/T4 (`--reasoning on`, `1.0/0.95/64`, target+draft `f8_e4m3` FP8 KV cache, `524,288` `512K` GPU KV + RAM = `1,048,576` (`1M+`) pool; live T4 `14,047 MiB` VRAM, `cached_tokens=182`, `41.69 tok/s` decode).
- **4B (`escalated_to_system2=True` & live code execution):** In `Deney 3` (`Cell 4`), verify that `noul_confidence < 0.75` (`0.48`) escalates cleanly via `escalated_to_system2=True` to System 2 and executes `calc.py` inside the isolated sandbox (leaving heavy synthesis such as `Qwen-Image` to high-VRAM G4/local setups while `media_world` stays a T4-compatible mockup).
- **4C (`DualLayerSessionStore` & `Canlı Stüdyo`):** Inspect how `DualLayerSessionStore` (`[KV Kaydet]` / `[Yükle]`) falls back smoothly to `text_replay_fallback` whenever `binary_kv_hit` (`slot0.kv.bin`) cannot restore. Test preset chips and `TR-204`/`MCP`/`Handoff`/`System 1` prompts in the portless `google.colab.output` JS RPC WebUI (`Cell 5`), verify `[⛶ Tam Ekran]` (`ESC`), `[⏹ Durdur]`, and `[🔌 Arayüzü Kapat]` (Kill Switch -> `ALAB-E07`), and finish with **Cell 6 (`🛑 2. Güvenli Kapanış`)**.

## 5. Design your own modern agent stack

Pick a small workflow from your domain and specify five decisions: (1) a least-privilege MCP scope split between two `Plugins`, (2) one rule resolved at `0` tokens inside `deterministic_gate`, (3) one required field in `StructuredHandoff` `constraints`, (4) an `escalated_to_system2=True` rule triggered when `System 1` (`Jev`/`Laya`: `Choice`/`Score`/`Noul`) confidence drops, and (5) one capability isolated behind an `MCP` tool or sandboxed runtime rather than crammed inside a chat LLM.
